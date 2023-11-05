import sqlite3
import pandas as pd
from device_data import DeviceInspector
from directories import DB_DIR, LOGS_DIR, LOGS_DIR, REPORT_DIR, BRAND_DIR, ICONS_DIR, BASE_DIR
# Database details
DB_PATH = 'path_to_devices.db'
TABLE_NAME = 'devices'
BIT_RATE_COLUMN = 'bit_rate'

# Threshold for detecting spikes, e.g., 50% increase
SPIKE_THRESHOLD = 0.5

def load_data_from_db():
    """
    Load the bit rate data from the SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT {BIT_RATE_COLUMN} FROM {TABLE_NAME}"
    data = pd.read_sql_query(query, conn)
    conn.close()
    return data

# Load data
data = load_data_from_db()

# Now, you can use the `data` DataFrame for your analysis.
print(data.head())

def detect_spikes(data):
    """
    Detect spikes in bit rates and return flagged entries.
    """
    # Calculate the percentage change in bit rates
    data['bit_rate_change'] = data[BIT_RATE_COLUMN].pct_change()
    
    # Flag entries where the percentage change exceeds the threshold
    spikes = data[data['bit_rate_change'].abs() > SPIKE_THRESHOLD]
    
    return spikes

def analyze_bit_rates():
    # Fetch all devices from the database
    conn = sqlite3.connect(f"{DB_DIR}/devices.db")
    cursor = conn.cursor()
    for device in DeviceInspector:

        device_id = device[0]
        device_name = device[7]

        # Fetch bidirectional bit rates for the device from a table in the database
        cursor.execute("SELECT * FROM bit_rates WHERE device_id = ?", (device_id,))
        bit_rates = cursor.fetchall()

        # Analyze the bit rates for the device
        total_incoming_bits = sum(rate[1] for rate in bit_rates)
        total_outgoing_bits = sum(rate[2] for rate in bit_rates)
        average_incoming_rate = total_incoming_bits / len(bit_rates)
        average_outgoing_rate = total_outgoing_bits / len(bit_rates)

        # Print the analysis results for the device
        print("Device Name:", device_name)
        print("Total Incoming Bits:", total_incoming_bits)
        print("Total Outgoing Bits:", total_outgoing_bits)
        print("Average Incoming Bit Rate:", average_incoming_rate)
        print("Average Outgoing Bit Rate:", average_outgoing_rate)

    # Close the database connection
    conn.close()

    # Call the analyze_bit_rates function to perform the analysis
    analyze_bit_rates()

if __name__ == "__main__":
    # Load the data
    data = load_data_from_db()
    
    # Detect spikes
    spikes_detected = detect_spikes(data)
    
    # Print the flagged entries
    if not spikes_detected.empty:
        print("Spikes detected in the following entries:")
        print(spikes_detected)
    else:
        print("No spikes detected.")