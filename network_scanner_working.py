import socket
import logging
import datetime
import sqlite3
from scapy.all import ARP, Ether, srp
from directories import DB_DIR, LOGS_DIR

# Set up logging
logging.basicConfig(filename=f'{LOGS_DIR}/network_scanner.log', level=logging.INFO)

class NetworkScanner:

    def __init__(self, ip_range=None):
        # If no IP range provided, determine the default IP range
        self.ip_range = ip_range if ip_range else self.get_default_ip_range()
        logging.info(f"Using IP range: {self.ip_range}")


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

    def perform_arp_scan(self):
        # Perform ARP scan using Scapy
        arp_scan_results = []
        print(f"Scanning IP range: {self.ip_range}")  # Added this line

        # Construct the ARP request packet
        arp_request = ARP(pdst=self.ip_range)
        ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether_frame / arp_request

        print("Sending ARP requests...")
        
        try:
            # Send the ARP packet and receive the responses
            result, _ = srp(packet, timeout=10, verbose=False)  # Increased timeout
            print(f"Received {len(result)} responses.")

            # Process the responses
            for sent, received in result:
                if received and received.haslayer("ARP"):
                    ip_address = received[ARP].psrc
                    mac_address = received[Ether].src
                    
                    print(f"  {ip_address:<20} {mac_address:<20} dynamic")

                    device = {
                        "ip_address": ip_address,
                        "mac_address": mac_address,
                        "last_seen": datetime.datetime.now(),
                        "vendor": "Sample Vendor",
                        "device_name": "Sample Device Name",
                        "os": "Sample OS",
                        "users": "Sample user data",
                        "application_log": "Sample app log",
                        "timestamp": "Sample Timestamp",
                    }
                    arp_scan_results.append(device)

            # Save the discovered devices to the database
            self.save_to_database(arp_scan_results)
            
        except Exception as e:
            logging.error(f'Exception encountered during ARP scan: {e}')
            print(f'Exception encountered during ARP scan: {e}')


    def save_to_database(self, devices):
        try:
            conn = sqlite3.connect(f"{DB_DIR}/devices.db")
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS devices(
                    ip_address TEXT PRIMARY KEY,
                    mac_address TEXT,
                    last_seen TEXT,
                    vendor TEXT,
                    device_name TEXT,
                    os TEXT
                )
            ''')
            for device in devices:
                cursor.execute('''
                    INSERT OR REPLACE INTO devices(ip_address, mac_address, last_seen, vendor, device_name, os)
                    VALUES(?, ?, ?, ?, ?, ?)
                ''', (device["ip_address"], device["mac_address"], device["last_seen"], 
                      device["vendor"], device["device_name"], device["os"]))
            conn.commit()
            conn.close()
            logging.info("Devices saved to the database successfully.")
        except Exception as e:
            logging.error(f"Error saving to the database: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    scanner = NetworkScanner()
    scanner.perform_arp_scan()
    