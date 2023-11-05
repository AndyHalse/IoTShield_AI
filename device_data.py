import sqlite3
from os import getcwd, popen
from directories import DB_DIR
import datetime

DB_PATH = f"{DB_DIR}/devices.db"


class DeviceInspector:
    def __init__(self):
        self.DB_PATH = DB_DIR + "/devices.db"
        self.conn = sqlite3.connect(self.DB_PATH)
        self.cursor = self.conn.cursor()

    def OUI_lookup(self, mac):
        prefix = mac.replace(":", "").upper()[:6]
        self.cursor.execute("SELECT * FROM oui WHERE HEX=?", (prefix,))
        result = self.cursor.fetchone()
        return {
            "hex": result[0],
            "base16": result[1],
            "company": result[2],
            "addr1": result[3],
            "addr2": result[4],
            "addr3": result[5],
            "addr4": result[6]
        } if result else None


class ExtendedDeviceInspector:

    def __init__(self):
        self.conn = sqlite3.connect(DB_DIR + "/devices.db")
        self.cursor = self.conn.cursor()

    # Method to detect the device type based on MAC address
    def detect_device_type(self, mac_address):
        # Define a lookup table with known MAC address
        mac_address_lookup = {
            # Office Devices
            "00:12:34": "IP CCTV Camera",
            "AB:CD:EF": "Router",
            "11:22:33": "Printer",
            "44:55:66": "Laptop",
            "77:88:99": "Desktop Computer",
            "AA:BB:CC": "Smartphone",
            "DD:EE:FF": "Tablet",
            "GG:HH:II": "Smart TV",
            "JJ:KK:LL": "Network Attached Storage (NAS)",
            "MM:NN:OO": "Smart Speaker",
            "PP:QQ:RR": "Smart Thermostat",
            "SS:TT:UU": "Smart Doorbell",
            "VV:WW:XX": "Wireless Printer",
            "YY:ZZ:11": "Network Scanner",
            "22:33:44": "Wireless Access Point (Wi-Fi AP)",
            "55:66:77": "Smart Home Hub",
            "88:99:AA": "Smart Lighting",
            "BB:CC:DD": "Smart Plug",
            "EE:FF:GG": "Smart Lock",
            "HH:II:JJ": "Gaming Console",
            "KK:LL:MM": "Network Attached Print Server",
            "NN:OO:PP": "Voice Assistant",
            "QQ:RR:SS": "Home Security System",
            "TT:UU:VV": "Surveillance DVR/NVR",

            # Home Devices
            "11:22:33": "Smartphone",
            "AA:BB:CC": "Tablet",
            "DD:EE:FF": "Smart TV",
            "GG:HH:II": "Smart Speaker",
            "JJ:KK:LL": "Smart Thermostat",
            "MM:NN:OO": "Smart Doorbell",
            "PP:QQ:RR": "Wireless Printer",
            "SS:TT:UU": "Network Scanner",
            "VV:WW:XX": "Wireless Access Point (Wi-Fi AP)",
            "YY:ZZ:11": "Smart Home Hub",
            "22:33:44": "Smart Lighting",
            "55:66:77": "Smart Plug",
            "88:99:AA": "Smart Lock",
            "BB:CC:DD": "Gaming Console",
            "EE:FF:GG": "Voice Assistant",
            "HH:II:JJ": "Home Security System",
            "KK:LL:MM": "Surveillance DVR/NVR",

            # IP CCTV Cameras
            "00:11:22": "IP CCTV Camera Brand A",
            "33:44:55": "IP CCTV Camera Brand B",
            "66:77:88": "IP CCTV Camera Brand C",

            # IoT Devices
            "AA:11:BB": "IoT Device Type 1",
            "BB:22:CC": "IoT Device Type 2",
            "CC:33:DD": "IoT Device Type 3",

        }
        # Extract the first 8 characters of the MAC address to compare with the lookup table
        mac_prefix = mac_address.upper().replace(":", "")[:8]

        # Check if the MAC address prefix exists in the lookup table
        if mac_prefix in mac_address_lookup:
            return mac_address_lookup[mac_prefix]
        else:
            return None  # Return None for unrecognized device types

    def get_vendor(self, ip_address):
        """Get the vendor of the device using its IP address."""
        try:
            command = f'nmap -sP {ip_address} | findstr MAC'
            process = popen(command)
            result = str(process.read())
            vendor = result.split('(')[1].split(')')[0]
            return vendor
        except Exception as e:
            return f"Error fetching vendor: {str(e)}"

    def get_firmware_version(self, ip_address):
        try:
            # SNMP parameters
            snmp_community = 'public'  # Replace 'public' with the actual SNMP 
            snmp_oid_firmware = '1.3.6.1.2.1.69.1.4.3.0'
            # Build SNMP GET command
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getcwd(CommunityData(snmp_community),
                       UdpTransportTarget((ip_address, 161)),
                       ObjectType(ObjectIdentity(snmp_oid_firmware)))
            )

            if errorIndication:
                # SNMP error occurred
                logger.error(f"SNMP error {ip_address}: {errorIndication}")
                return "Unknown"  # Return "Unknown" to indicate an error

            if errorStatus:
                # Non-zero SNMP error status
                logger.error(f"Non-zero SNMP error status while fetching firmware version for {ip_address}: {errorStatus.prettyPrint()}")
                return "Unknown"  # Return "Unknown" to indicate an error

            # Extract the firmware version from the SNMP response
            firmware_version = varBinds[0][1].prettyPrint()
            return firmware_version

        except Exception as e:
            # Log the error: SNMP query failed
            logger.error(f"Error occurred while fetching firmware version for {ip_address}: {str(e)}")
            return "Unknown"  # Return "Unknown" to indicate an error

    def get_cpu_data(self, ip_address):
        try:
            # SNMP parameters
            snmp_community = 'public'  # Replace 'public' with the actual SNMP community string
            snmp_oid_cpu_load = '1.3.6.1.4.1.2021.11.11.0'  # The OID for CPU load (1-minute average)

            # Build SNMP GET command
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(CommunityData(snmp_community),
                       UdpTransportTarget((ip_address, 161)),
                       ObjectType(ObjectIdentity(snmp_oid_cpu_load)))
            )

            if errorIndication:
                # SNMP error occurred
                logger.error(f"SNMP error while fetching CPU data for {ip_address}: {errorIndication}")
                return "Unknown"  # Return "Unknown" to indicate an error

            if errorStatus:
                # Non-zero SNMP error status
                logger.error(f"Non-zero SNMP error status while fetching CPU data for {ip_address}: {errorStatus.prettyPrint()}")
                return "Unknown"  # Return "Unknown" to indicate an error

            # Extract the CPU load from the SNMP response
            cpu_load = varBinds[0][1].prettyPrint()
            return cpu_load

        except Exception as e:
            # Log the error: SNMP query failed
            logger.error(f"Error occurred while fetching CPU data for {ip_address}: {str(e)}")
            return "Unknown"  # Return "Unknown" to indicate an error

    def get_memory_data(self, ip_address):
        try:
            # SNMP parameters
            snmp_community = 'public'  # Replace 'public' with the actual SNMP community string
            snmp_oid_memory_total = '1.3.6.1.4.1.2021.4.5.0'  # The OID for total memory
            snmp_oid_memory_free = '1.3.6.1.4.1.2021.4.11.0'  # The OID for free memory

            # Build SNMP GET commands to fetch total and free memory
            errorIndication1, errorStatus1, errorIndex1, varBinds1 = next(
                getCmd(CommunityData(snmp_community),
                    UdpTransportTarget((ip_address, 161)),
                    ObjectType(ObjectIdentity(snmp_oid_memory_total)))
            )
            errorIndication2, errorStatus2, errorIndex2, varBinds2 = next(
                getCmd(CommunityData(snmp_community),
                    UdpTransportTarget((ip_address, 161)),
                    ObjectType(ObjectIdentity(snmp_oid_memory_free)))
            )

            if errorIndication1 or errorIndication2:
                # SNMP error occurred
                logger.error(f"SNMP error while fetching memory data for {ip_address}: {errorIndication1 or errorIndication2}")
                return "Unknown"  # Return "Unknown" to indicate an error

            if errorStatus1 or errorStatus2:
                # Non-zero SNMP error status
                logger.error(f"Non-zero SNMP error status while fetching memory data for {ip_address}: {errorStatus1.prettyPrint() or errorStatus2.prettyPrint()}")
                return "Unknown"  # Return "Unknown" to indicate an error

            # Extract the memory data from the SNMP responses
            total_memory = varBinds1[0][1]
            free_memory = varBinds2[0][1]

            # Convert memory values to MB (assumes the SNMP values are in kilobytes)
            total_memory_mb = int(total_memory) // 1024
            free_memory_mb = int(free_memory) // 1024

            # Calculate used memory in MB
            used_memory_mb = total_memory_mb - free_memory_mb

            # Return the memory data as a string in the format "used_memory/total_memory" (e.g., "512 MB/1024 MB")
            return f"{used_memory_mb} MB/{total_memory_mb} MB"

        except Exception as e:
            # Handle any unexpected exceptions
            logger.error(f"An error occurred while fetching memory data for {ip_address}: {e}")
            return "Unknown"  # Return "Unknown" to indicate an error

    def get_operating_system(self, ip_address):
        try:
            # TODO: Implement a method to fetch the operating system of the device
            # For simplicity, we'll use the 'platform' module for basic OS detection

            # Get the operating system name from the platform module
            os_name = platform.system()

            # Log the event: OS detection successful
            logger.info(f"Operating system detected for {ip_address}: {os_name}")

            return os_name

        except Exception as e:
            # Log the error: OS detection failed
            logger.error(f"Error occurred while fetching operating system for {ip_address}: {str(e)}")
            return "Unknown"  # If OS detection fails, return "Unknown" to indicate an error

    def get_open_ports(self, ip_address):
        try:
            nm = nmap.PortScanner()
            # Perform a TCP SYN scan on the device to detect open ports
            scan_result = nm.scan(hosts=ip_address, arguments='-sS')

            if ip_address not in scan_result['scan']:
                # Device not found or scan failed
                logger.warning(f"No scan results found for {ip_address}.")
                return "Unknown"  # Return "Unknown" to indicate an error

            # Extract the open ports from the scan result
            open_ports = scan_result['scan'][ip_address]['tcp'].keys()
            open_ports = [str(port) for port in open_ports]

            # Return the open ports as a comma-separated string
            return ", ".join(open_ports)

        except nmap.PortScannerError as e:
            logger.error(f"Error occurred during port scan for {ip_address}: {str(e)}")
            return "Unknown"  # Return "Unknown" to indicate an error

        except Exception as e:
            logger.error(f"Error occurred during port scan for {ip_address}: {str(e)}")
            return "Unknown"  # Return "Unknown" to indicate an error

    def get_installed_software(self, ip_address):
        try:
            # SNMP parameters
            snmp_community = 'public'  # Replace 'public' with the actual SNMP community string
            snmp_oid_software = '1.3.6.1.2.1.25.6.3.1.2'  # The OID for the installed software

            installed_software = []

            # Build SNMP GETNEXT command to fetch installed software information
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),  # Replace os.getcwd() with SnmpEngine()
                       CommunityData(snmp_community),
                       UdpTransportTarget((ip_address, 161)),
                       ObjectType(ObjectIdentity(snmp_oid_software)))
            )
            installed_software = ["Software A", "Software B"]  # Replace this with actual software data

            return ", ".join(installed_software)  # Return a comma-separated string of installed software

        except Exception as e:
            # Log the error: SNMP query failed or any other error occurred
            logger.error(f"Error occurred while fetching installed software for {ip_address}: {str(e)}")
            return "Unknown"  # Return "Unknown" to indicate an error

    def get_hostname_vendor(self, mac_address):
        try:
            # Extract the first 6 characters of the MAC address to use as the OUI
            oui = mac_address.upper().replace(":", "")[:6]

            # Vendor lookup API URL
            vendor_lookup_url = f"https://api.macvendors.com/{oui}"

            # Send a GET request to the vendor lookup API
            response = request.get(vendor_lookup_url)

            if response.status_code == 200:
                # Successful API response
                return response.text.strip()

            # If the API response is not successful, return "Unknown"
            logger.warning(f"Failed to fetch hostname vendor for MAC address {mac_address}. Status code: {response.status_code}")
            return "Unknown"

        except Exception as e:
            logger.error(f"Error occurred while fetching hostname vendor for MAC address {mac_address}: {str(e)}")
            return "Unknown"  # Return "Unknown" to indicate an error

    def get_bit_rate_sent(self, ip_address):
        try:
            # SNMP parameters
            snmp_community = 'public'  # Replace 'public' with the actual SNMP community string
            snmp_oid_bit_rate_sent = '1.3.6.1.2.1.2.2.1.16'  # The OID for the bit rate sent (ifOutOctets)

            # Build SNMP GETNEXT command to get the first instance of ifOutOctets (bit rate sent)
            errorIndication, errorStatus, errorIndex, varBinds = next(
                os.getcwd(SnmpEngine(),
                       CommunityData(snmp_community),
                       UdpTransportTarget((ip_address, 161)),
                       ObjectType(ObjectIdentity(snmp_oid_bit_rate_sent)))
            )
            if errorIndication:
                # SNMP error occurred
                logger.error(f"SNMP error while fetching bit rate sent for {ip_address}: {errorIndication}")
                return "Unknown"  # Return "Unknown" to indicate an error

            if errorStatus:
                # Non-zero SNMP error status
                logger.error(f"Non-zero SNMP error status while fetching bit rate sent for {ip_address}: {errorStatus.prettyPrint()}")
                return "Unknown"  # Return "Unknown" to indicate an error

            # Extract the bit rate sent from the SNMP response
            bit_rate_sent = varBinds[0][1].prettyPrint()
            return bit_rate_sent

        except Exception as e:
            # Log the error: SNMP query failed
            logger.error(f"Error occurred while fetching bit rate sent for {ip_address}: {str(e)}")
            return "Unknown"  # Return "Unknown" to indicate an error

    def get_bit_rate_received(self, ip_address):
        try:
            # SNMP parameters
            snmp_community = 'public'  # Replace 'public' with the actual SNMP community string
            snmp_oid_bit_rate_received = '1.3.6.1.2.1.2.2.1.10'  # The OID for the bit rate received (ifInOctets)

            # Build SNMP GETNEXT command to get the first instance of ifInOctets (bit rate received)
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(CommunityData(snmp_community),
                       UdpTransportTarget((ip_address, 161)),
                       ObjectType(ObjectIdentity(snmp_oid_bit_rate_received)))
            )
            if errorIndication:
                # SNMP error occurred
                logger.error(f"SNMP error while fetching bit rate received for {ip_address}: {errorIndication}")
                return "Unknown"  # Return "Unknown" to indicate an error
            if errorStatus:
                # Non-zero SNMP error status
                logger.error(f"Non-zero SNMP error status while fetching bit rate received for {ip_address}: {errorStatus.prettyPrint()}")
                return "Unknown"  # Return "Unknown" to indicate an error
            # Extract the bit rate received from the SNMP response
            bit_rate_received = varBinds[0][1].prettyPrint()
            return bit_rate_received

        except Exception as e:
            # Log the error: SNMP query failed
            logger.error(f"Error occurred while fetching bit rate received for {ip_address}: {str(e)}")
            return "Unknown"  # Return "Unknown" to indicate an error

    def get_device_name(self, ip_address):
        """Get the device name using its IP address."""
        try:
            command = f'nmap -O {ip_address} | findstr Running'
            process = popen(command)
            result = str(process.read())
            device_name = result.split(' ')[1]
            return device_name
        except Exception as e:
            return f"Error fetching device name: {str(e)}"

    def get_operating_system(self, ip_address):
        """Get the operating system of the device using its IP address."""
        try:
            command = f'nmap -O {ip_address} | findstr OS'
            process = popen(command)
            result = str(process.read())
            os = result.split(':')[1].split(',')[0]
            return os
        except Exception as e:
            return f"Error fetching operating system: {str(e)}"

    def get_all_devices(self):
        """Retrieve all devices' IP and MAC addresses from the database."""
        self.cursor.execute("SELECT ip_address, mac_address FROM devices")
        return self.cursor.fetchall()

    def update_device_info(self, ip_address, mac_address):
        vendor = self.get_vendor(ip_address)
        device_name = self.get_device_name(ip_address)
        os = self.get_operating_system(ip_address)

        self.cursor.execute("SELECT * FROM devices WHERE ip_address=?", (ip_address,))
        existing_device = self.cursor.fetchone()

        timestamp = str(datetime.datetime.now())
        data = (ip_address, mac_address, vendor, device_name, os, timestamp, "", "", "", timestamp)

        if existing_device:
            update_sql = """
            UPDATE devices SET
                mac_address=?,
                vendor=?,
                device_name=?,
                os=?,
                last_scanned=?,
                users=?,
                application_log=?,
                other_data=?,
                timestamp=?
            WHERE ip_address=?
            """
            self.cursor.execute(update_sql, data)
        else:
            insert_sql = """
            INSERT INTO devices (
                ip_address, mac_address, vendor, device_name, os,
                last_scanned, users, application_log, other_data, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(insert_sql, data)
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    inspector = ExtendedDeviceInspector()
    devices = inspector.get_all_devices()
    for device in devices:
        inspector.update_device_info(device[0], device[1])
    inspector.close()
