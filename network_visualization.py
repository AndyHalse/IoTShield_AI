import sqlite3
import networkx as nx
import matplotlib.pyplot as plt
import os
from config import DB_DIR, LOGS_DIR, REPORT_DIR, BRAND_DIR, ICONS_DIR, DB_DIR

BASE_DIR = "/Users/andyhalse/AI Cyber Solutions Projects/IotShield/data"
DB_DIR = os.path.join(BASE_DIR, "devices.db")

def generate_network_topology():
    conn = sqlite3.connect(DB_DIR)
    cursor = conn.cursor()

    # Check if the 'connected_devices' column exists in the 'devices' table
    cursor.execute("PRAGMA table_info(devices)")
    columns = cursor.fetchall()
    column_names = [column[1] for column in columns]
    if 'connected_devices' not in column_names:
        # Add the 'connected_devices' column to the 'devices' table
        cursor.execute("ALTER TABLE devices ADD COLUMN connected_devices TEXT")
        conn.commit()

    # Retrieve device information from the 'devices' table in the database
    cursor.execute("SELECT ip_address, connected_devices FROM devices")
    devices = cursor.fetchall()

    # Create a graph and add edges between devices based on connections
    G = nx.Graph()
    for device in devices:
        ip_address = device[0]
        connected_devices = device[1].split(',') if device[1] else []
        for connected_device in connected_devices:
            G.add_edge(ip_address, connected_device)

    # Visualize the network topology
    nx.draw(G, with_labels=True, node_size=500, node_color='skyblue', font_size=8, edge_color='gray')
    plt.title('Network Topology')
    plt.show()

    conn.close()

if __name__ == '__main__':
    generate_network_topology()
