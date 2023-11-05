import datetime
import logging
import sqlite3
import sys
import device_monitoring
import requests
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
import os

# Configure logging
logging.basicConfig(filename='device_monitoring.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def monitor_devices():
    # Connect to the SQLite database
    conn = sqlite3.connect('devices.db')
    cursor = conn.cursor()

    # Create the devices and device_logs tables if they don't exist
    create_devices_table(cursor)
    create_device_logs_table(cursor)

    # Fetch all devices from the database
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()

    # Initialize a flag to check if any issues are found
    issues_found = False

    # Perform monitoring on each device
    for device in devices:
        ip_address = device[3]
        device_name = device[7]

        # Perform vulnerability assessment on the device
        vulnerability_results = perform_vulnerability_assessment(ip_address)

        # Update the vulnerability assessment results in the database
        cursor.execute("UPDATE devices SET vulnerability_assessment_results = ? WHERE id = ?", (vulnerability_results, device[0]))
        conn.commit()

        # Check for potential vulnerabilities
        if has_potential_vulnerabilities(vulnerability_results):
            # Log the potential vulnerabilities
            log_message = f"Potential vulnerabilities detected on device '{device_name}'."
            insert_device_log(cursor, device[0], log_message)
            conn.commit()

            # Send an alert/notification
            send_alert(device_name, vulnerability_results)

            # Set the flag indicating issues were found
            issues_found = True

    # Close the database connection
    cursor.close()
    conn.close()

    # Show a message box with the appropriate message
    if issues_found:
        QMessageBox.information(None, "Device Monitoring", "Potential vulnerabilities detected!")
    else:
        QMessageBox.information(None, "Device Monitoring", "Great News No Current Issues Found.")


def create_devices_table(self):
    try:
        conn = sqlite3.connect(os.path.join(database_directory, "devices.db"))
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS devices
                          (ip_address TEXT, mac_address TEXT, ip_range TEXT,
                           operating_system TEXT, open_ports TEXT, installed_software TEXT,
                           hostname_vendor TEXT)''')

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        logger.exception("Error creating devices table:", exc_info=e)


def create_device_logs_table(cursor):
    # Create the device_logs table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS device_logs (
            id INTEGER PRIMARY KEY,
            deviceId INTEGER,
            timestamp TEXT,
            message TEXT,
            FOREIGN KEY (deviceId) REFERENCES devices (id)
        )
    """)

def perform_vulnerability_assessment(ip_address):
    # Implement your logic here to perform a vulnerability assessment on the IP address
    # You can use an API, library, or perform custom vulnerability checks
    # Return the assessment results as a string or in a suitable format
    vulnerability_results = ""

    # Example implementation using an API
    api_url = f"https://api.example.com/devices/{ip_address}/vulnerability-assessment"
    response = requests.get(api_url)
    if response.status_code == 200:
        vulnerability_results = response.text
    else:
        logging.error("Vulnerability assessment failed for IP address: %s", ip_address)

    return vulnerability_results

def has_potential_vulnerabilities(vulnerability_results):
    # Implement your logic here to determine if the vulnerability results indicate potential vulnerabilities
    # You can parse the assessment results, check for specific patterns or keywords, or use a scoring system
    # Return True if potential vulnerabilities are detected, False otherwise
    return "high" in vulnerability_results.lower()

# Function to insert a device into the database
def insert_device(device):
    conn = sqlite3.connect('devices.DB')
    c = conn.cursor()

    c.execute('''INSERT OR REPLACE INTO devices
                 (ip_address, hostname, mac_address, serial_number, type, product_number, operating_software, firmware_version)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (device['ip_address'], device['hostname'], device['mac_address'], device['serial_number'],
               device['type'], device['product_number'], device['operating_software'], device['firmware_version']))

    conn.commit()
    conn.close()

def send_alert(device_name, vulnerability_results):
    # Implement your logic here to send an alert/notification
    # You can use email, SMS, push notifications, or any other method suitable for your requirements
    # Include the device name and vulnerability results in the alert/notification message
    alert_message = f"Potential vulnerabilities detected on device '{device_name}':\n{vulnerability_results}"
    logging.info("Sending alert: %s", alert_message)
    # Add your code to send the alert/notification

if __name__ == "__main__":
    # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Call the monitor_devices function to initiate the monitoring
    monitor_devices()

    # Start the main event loop
    sys.exit(app.exec())

