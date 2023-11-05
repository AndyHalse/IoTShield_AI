import socket
import struct
import netifaces
from datetime import datetime
import nmap

def scan_network():
    network_interfaces = netifaces.interfaces()

    for interface in network_interfaces:
        if interface != "lo":
            ip_addresses = netifaces.ifaddresses(interface).get(netifaces.AF_INET)
            if ip_addresses:
                for ip in ip_addresses:
                    ip_address = ip["addr"]
                    subnet_mask = ip["netmask"]
                    network_address = get_network_address(ip_address, subnet_mask)

                    print(f"Scanning devices on network {network_address}")
                    scan_devices(network_address)

def get_network_address(ip_address, subnet_mask):
    ip_address = ip_address.split(".")
    subnet_mask = subnet_mask.split(".")

    network_address = []
    for i in range(4):
        network_address.append(str(int(ip_address[i]) & int(subnet_mask[i])))

    return ".".join(network_address)

def scan_devices(network_address):
    detected_devices = []
    
    start_time = datetime.now()  # Define the start_time variable here
    
    for i in range(1, 255):
        ip = f"{network_address}.{i}"
        
        # Implement device scanning logic here
        # Use libraries like nmap or other suitable methods to scan the devices on the network
        # You can perform port scanning, service discovery, or any other technique suitable for device identification
        # Add the detected devices to the 'detected_devices' list
        
    end_time = datetime.now()
    scan_duration = end_time - start_time
    print(f"Scanning completed in {scan_duration}")

    return detected_devices

