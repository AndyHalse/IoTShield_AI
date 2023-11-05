
import datetime
import os
import logging
import socket
import sqlite3
import subprocess
import nmap
from datetime import datetime

# Constants
DB_DIR = "./db"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

class NetworkScanner:

    def __init__(self, ip_range=None):
        self.nm = nmap.PortScanner()
        self.ip_range = ip_range or self.detect_default_ip_range()
        logging.info(f"Using IP range: {self.ip_range}")

    def detect_default_ip_range(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            s.close()
            ip_range = ".".join(ip_address.split('.')[:-1]) + ".0/24"
            logging.info(f"Detected default IP range: {ip_range}")
            return ip_range
        except Exception as e:
            logging.error(f"Error detecting default IP range: {e}")
            return None

    def arp_scan(self):
        devices = []
        try:
            result = subprocess.check_output(["arp", "-a"]).decode('utf-8').split("\n")
            for line in result:
                if self.ip_range.split(".")[2] in line:
                    ip = line.split()[0]
                    mac_address = line.split()[1]
                    devices.append({"ip": ip, "mac_address": mac_address})
        except Exception as e:
            logging.error(f"Error during ARP scan: {e}")
        return devices

    def nmap_scan(self):
        devices = []
        try:
            logging.info("Starting nmap scan with advanced options...")
            # Using advanced nmap scanning options
            self.nm.scan(hosts=self.ip_range, arguments='-sP -sV -O -T4')
            for host in self.nm.all_hosts():
                devices.append(self.parse_nmap_output(host, self.nm[host]))
        except Exception as e:
            logging.error(f"Error during nmap scan: {e}")
        return devices

    def parse_nmap_output(self, host, scan_results):
        mac_address = None
        manufacturer = None
        os_type = None
        device_type = None
        name = None
        service_details = []

        if 'addresses' in scan_results:
            mac_address = scan_results['addresses'].get('mac', None)
            manufacturer = scan_results['vendor'].get(mac_address, None)
        
        if 'osclass' in scan_results and scan_results['osclass']:
            os_type = scan_results['osclass'][0].get('osfamily', None)
            device_type = scan_results['osclass'][0].get('osgen', None)
        
        if 'hostnames' in scan_results and scan_results['hostnames']:
            name = scan_results['hostnames'][0].get('name', None)

        for proto in scan_results['tcp']:
            services = scan_results['tcp'][proto]
            service_details.extend([f"Port {proto}: {services['name']} ({services['product']})"])
        services_info = "; ".join(service_details) if service_details else "No services detected"

        try:
            hostname = socket.gethostbyaddr(host)[0]
        except socket.herror:
            hostname = "Unknown"

        return {
            'ip': host,
            'mac_address': mac_address or "Unknown",
            'manufacturer': manufacturer or "Unknown",
            'os_type': os_type or "Unknown",
            'device_type': device_type or "Unknown",
            'name': name or hostname,
            'services_info': services_info
        }

    def save_to_database(self, devices):
        try:
            conn = sqlite3.connect(f"{DB_DIR}/devices.db")
            cursor = conn.cursor()
            for device in devices:
                cursor.execute('''
                    INSERT OR REPLACE INTO devices(ip, mac, last_seen, manufacturer, device_type, os, services_info)
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                ''', (device["ip"], device["mac_address"], datetime.now(), 
                    device["manufacturer"], device["device_type"], device["os_type"], device["services_info"]))
            conn.commit()
            conn.close()
            logging.info("Devices saved to the database successfully.")
        except Exception as e:
            logging.error(f"Error saving to the database: {e}")

    def scan(self):
        logging.info("Starting network scan...")
        arp_results = self.arp_scan()
        nmap_results = self.nmap_scan()
        combined_results = arp_results + nmap_results  # Combining both ARP and nmap results
        self.save_to_database(combined_results)
        logging.info("Network scan completed.")

if __name__ == "__main__":
    scanner = NetworkScanner()
    scanner.scan()
