import logging
import os
import socket
import sqlite3
import time
from datetime import datetime, timedelta
import concurrent.futures
import nmap
from scapy.all import ARP, Ether, srp

# Importing directories for database and log paths
from directories import DB_DIR, LOGS_DIR

# Constants for the database
DB_PATH = os.path.join(DB_DIR, "devices.db")
LOG_FILE = os.path.join(LOGS_DIR, "network_scanner.log")
# Ensure the logs directory exists
logging.basicConfig(
    level=logging.DEBUG,
    filename=os.path.join(LOGS_DIR, "network_scanner.log"),
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class NetworkScanner:
    def __init__(self, ip_range=None):
        self.ip_range = ip_range if ip_range else self.get_default_ip_range()
        logging.basicConfig(
            filename='failed_devices.log',
            level=logging.ERROR,
            format='%(asctime)s [%(levelname)s]: %(message)s'
        )

    def get_default_ip_range(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            ip_range = ip_address.rsplit('.', 1)[0] + '.0/24'
            logging.info(f"Detected default IP range: {ip_range}")
            return ip_range
        except Exception as e:
            logging.error(f"Error in get_default_ip_range: {e}")
            return None

    def ensure_db_table_exists(self):
        with sqlite3.connect(DB_PATH) as conn:  # Use db_path instead of DB_DIR
            cursor = conn.cursor()

            # Check if the table exists
            cursor.execute('''SELECT name FROM sqlite_master WHERE type='table'
                AND name='devices' ''')
            if not cursor.fetchone():
                # If the table does not exist, create it
                cursor.execute('''
                    CREATE TABLE devices(
                        id INTEGER PRIMARY KEY,
                        device_number TEXT,
                        ip_address TEXT,
                        mac_address TEXT,
                        last_seen TEXT,
                        vendor TEXT,
                        device_name TEXT,
                        os TEXT,
                        users TEXT,
                        application_log TEXT,
                        timestamp TEXT,
                        bit_rate REAL,
                        device_type,
                        device_model,
                        location,
                        open_ports,
                        status,
                        network_segment,
                        customer_field,
                        os_version
                        is_cctv_camera BOOLEAN
                        )
                ''')
                logging.info("Created 'devices' table in the database.")
            conn.commit()

    def is_cctv_camera_mac(self, mac_address):
        cctv_oui_prefixes = ["00:0A:0B", "00:1C:C4", "00:0D:C5"]  # nown OUIs
        mac_prefix = mac_address[:8].upper()
        return any(prefix in mac_prefix for prefix in cctv_oui_prefixes)

    def determine_os_type(self, nm, ip_address):
        try:
            # Perform an OS detection scan using Nmap
            nm.scan(hosts=ip_address, arguments='-O')

            # Check if the OS detection results are available
            if 'osclass' in nm[ip_address]:
                # Extract and return the detected OS information
                os_info = nm[ip_address]['osclass'][0]['osfamily']
                return os_info
            else:
                return "Unknown OS"

        except Exception as e:
            # Handle any exceptions that may occur during the scan
            logging.error(f'Error determining OS for {ip_address}: {e}')
            return "Error"

    def mark_offline_devices():
        """Mark devices as offline not seen in the last 10 minutes."""
        with sqlite3.connect(DB_PATH) as conn:  # Use db_path instead of DB_DIR
            cursor = conn.cursor()

            # Fetch all devices from the database
            query = """
                SELECT device_number, mac_address, last_seen
                FROM devices
            """
            cursor.execute(query)
            all_devices = cursor.fetchall()

        ten_minutes_ago = datetime.now() - timedelta(minutes=10)

        for device in all_devices:
            device_number, mac_address, last_seen_str = device
            try:
                # Convert string date from DB to datetime object
                fmt = "%Y-%m-%d %H:%M:%S"
                device_last_seen = datetime.strptime(last_seen_str, fmt)

                # Check if device was last seen more than 10 minutes ago
                if device_last_seen < ten_minutes_ago:
                    log_msg = (
                        f"Device {device_number} (MAC: {mac_address}) "
                        f"is offline (last seen {last_seen_str})"
                    )
                    logging.warning(log_msg)
            except ValueError as e:
                log_error_msg = (
                    f"Error parsing date for device {device_number} "
                    f"(MAC: {mac_address}): {e}"
                )
                logging.error(log_error_msg)

        conn.close()

    def log_failed_devices(self, failed_devices):
        # Log information about the failed devices
        for ip_address in failed_devices:
            logging.error(f'Failed to scan IP: {ip_address}')

    def perform_arp_scan(self):
        self.ensure_db_table_exists()
        nm = nmap.PortScanner()
        arp_scan_results = []
        failed_devices = []

        print(f"Scanning IP range: {self.ip_range}")

        arp_request = ARP(pdst=self.ip_range)
        ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether_frame / arp_request

        print("Sending ARP requests...")

        result, _ = srp(packet, timeout=1, verbose=False)

        print(f"Received {len(result)} responses.")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for sent, received in result:
                if received and received.haslayer("ARP"):
                    ip_address = received[ARP].psrc
                    mac_address = received[Ether].src
                    # ... (rest of the code for processing each response)
                    # Create a function to process each response
                    futures.append(executor.submit(self.process_arp_response,
                                                   nm,
                                                   ip_address, mac_address,
                                                   arp_scan_results,
                                                   failed_devices))

            # Wait for all futures to complete
            concurrent.futures.wait(futures)

        self.save_to_database(arp_scan_results)
        self.mark_offline_devices()

        # Log the failed devices
        if failed_devices:
            self.log_failed_devices(failed_devices)

    def process_arp_response(self, nm, ip_address, mac_address,
                             arp_scan_results, failed_devices):
        try:
            device_name, _, _ = socket.gethostbyaddr(ip_address)
        except socket.herror:
            device_name = "Unknown Device"

        try:
            nm.scan(hosts=ip_address, arguments='-O -F')
            vendor_data = nm[ip_address].get('vendor', {})
            vendor = vendor_data.get(mac_address, 'Unknown')
            os_type = self.determine_os_type(nm, ip_address)

            # Check if MAC address belongs to a CCTV camera manufacturer
            is_cctv_camera = self.is_cctv_camera_mac(mac_address)

            device = {
                "ip_address": ip_address,
                "mac_address": mac_address,
                "last_seen": datetime.now(),
                "vendor": vendor,
                "device_name": device_name,
                "os": os_type,
                "users": "Sample user data",
                "application_log": "Sample app log",
                "timestamp": "Sample Timestamp",
                "bit_rate": 100.0,
                "is_cctv_camera": is_cctv_camera  # Indicator for CCTV cameras
            }

            arp_scan_results.append(device)
        except Exception as e:
            logging.error(f'Error scanning IP: {ip_address}. Error: {e}')
            failed_devices.append(ip_address)

    def save_to_database(self, devices):
        """Save device details to the database."""
        retry_count = 0
        success = False  # Initialize the success flag here

        while retry_count < 5:
            try:
                with sqlite3.connect(DB_PATH) as conn:
                    cursor = conn.cursor()
                    for device in devices:
                        try:
                            # Check if device with given MAC exists
                            cursor.execute(
                                "SELECT * FROM devices WHERE mac_address=?",
                                (device["mac_address"],)
                            )
                            existing_device = cursor.fetchone()

                            if existing_device:
                                # Update device details if it exists
                                params = (
                                    device["ip_address"],
                                    device["last_seen"],
                                    device["vendor"],
                                    device["device_name"],
                                    device["os"],
                                    device["users"],
                                    device["application_log"],
                                    device["timestamp"],
                                    device["bit_rate"],
                                    device["mac_address"],
                                    device["is_cctv_camera"]
                                )
                                update_query = """
                                    UPDATE devices
                                    SET ip_address=?, last_seen=?, vendor=?,
                                      device_name=?, os=?, users=?,
                                      application_log=?, timestamp=?,
                                      bit_rate=?, is_cctv_camera=? WHERE
                                      mac_address=?
                                """
                                cursor.execute(update_query, params)
                            else:
                                # Insert new entry if device does not exist
                                params = (
                                    device["ip_address"],
                                    device["mac_address"],
                                    device["last_seen"],
                                    device["vendor"],
                                    device["device_name"],
                                    device["os"],
                                    device["users"],
                                    device["application_log"],
                                    device["timestamp"],
                                    device["bit_rate"]
                                )
                                insert_query = """
                                    INSERT INTO devices
                                    (ip_address, mac_address, last_seen,
                                    vendor, device_name, os, users,
                                    application_log, timestamp, bit_rate)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """
                                cursor.execute(insert_query, params)
                        except Exception as e:
                            err_mac = device['mac_address']
                            err_msg = f"Error with MAC {err_mac}"
                            log_msg = f"{err_msg}: {e}"
                            logging.error(log_msg)
                            continue  # Continue with next device
                    conn.commit()
                    success = True

            except sqlite3.OperationalError as e:
                if "database is locked" in str(e):
                    log_msg = f"Database locked. Retry {retry_count + 1}."
                    logging.warning(log_msg)
                    time.sleep(1)  # Wait 1 second before retrying
                    retry_count += 1
                else:
                    logging.error(f"Database error: {e}")
            else:
                if not success:
                    logging.error("Failed to save to database after attempts.")
                    break  # Exit the outer loop if not successful


if __name__ == "__main__":
    scanner = NetworkScanner()
    scanner.perform_arp_scan()
