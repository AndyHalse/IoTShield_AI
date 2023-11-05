import os
import scapy.all as scapy
import sqlite3
from directories import DB_DIR

DB_PATH = os.path.join(DB_DIR, "devices.db")


def list_interfaces():
    interfaces = scapy.get_if_list()
    for interface in interfaces:
        print(interface)


list_interfaces()


def get_ip_addresses_from_db():
    """Fetch IP addresses from the database."""
    ip_addresses = []
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ip_address FROM devices")
            ip_addresses = [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")
    return ip_addresses


def get_byte_rate_for_ip(ip_address, interface, duration=1):
    """Calculate byte rate for specific IP address."""
    packets = scapy.sniff(iface=interface, timeout=duration,
                          filter=f"ip host {ip_address}")

    bytes_sent = sum(len(packet) for packet in packets
                     if packet[scapy.IP].src == ip_address)
    bytes_received = sum(len(packet) for packet in packets
                         if packet[scapy.IP].dst == ip_address)

    return bytes_sent, bytes_received


def main():
    # Specify the network interface (e.g., 'eth0', 'wlan0')
    interface = 'eth0'

    # Fetch IP addresses from the database
    ip_addresses = get_ip_addresses_from_db()

    for ip_address in ip_addresses:
        # Retrieve byte rate for each IP address
        bytes_sent, bytes_received = get_byte_rate_for_ip(
            ip_address, interface)

        # Print the results
        print(f"IP Address: {ip_address}")
        print(f"Bytes Sent: {bytes_sent} bytes")
        print(f"Bytes Received: {bytes_received} bytes")
        print("-------------------------------")


if __name__ == "__main__":
    main()
