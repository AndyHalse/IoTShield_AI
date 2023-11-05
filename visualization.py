import datetime
import os
import sqlite3
import sys
from tkinter import Tk, Button, Label
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

from directories import DB_DIR, LOGS_DIR, LOGS_DIR, REPORT_DIR, BRAND_DIR, ICONS_DIR

print(sys.path)

# Function to refresh the device data
def refresh_devices():
    global G, canvas

    # Clear the current graph
    G.clear()

    # Read data from devices.db
    with sqlite3.connect(os.path.join(DB_DIR, "devices.db")) as conn:
        cursor = conn.cursor()

        # Fetch all devices from the database
        cursor.execute("SELECT * FROM devices")
        device_rows = cursor.fetchall()

        # Fetch all connections from the database
        cursor.execute("SELECT * FROM connections")
        connection_rows = cursor.fetchall()

    # Iterate through the devices and add nodes to the graph
    for row in device_rows:
        if len(row) == 9:
            device_id, ip_address, _, _, _, _, hostname_vendor, _, _ = row
            device_data = {
                "ip_address": ip_address,
                "hostname_vendor": hostname_vendor
            }
            G.add_node(device_id, **device_data)
        else:
            # Handle the error here, such as skipping the row or logging a message
            print(f"Skipping invalid row: {row}")

    # Iterate through the connections and add edges to the graph
    for row in connection_rows:
        device_number, connected_device_number = row
        G.add_edge(device_number, connected_device_number)

    # Clear the canvas
    canvas.get_tk_widget().destroy()

    # Create a new canvas for displaying the network topology
    canvas = FigureCanvasTkAgg(plt.figure(figsize=(8, 6)), master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Draw the updated network topology on the canvas
    nx.draw_networkx_nodes(G, pos, node_color='b', node_size=200)
    nx.draw_networkx_edges(G, pos, edge_color='r')
    nx.draw_networkx_labels(G, pos, font_color='w')
    plt.axis('off')

# Create an empty NetworkX graph
G = nx.Graph()

# Read data from devices.db
with sqlite3.connect(os.path.join(DB_DIR, "devices.db")) as conn:
    cursor = conn.cursor()

    # Fetch all devices from the database
    cursor.execute("SELECT * FROM devices")
    device_rows = cursor.fetchall()

    # Fetch all connections from the database
    cursor.execute("SELECT * FROM connections")
    connection_rows = cursor.fetchall()

# Iterate through the devices and add nodes to the graph
for row in device_rows:
    if len(row) == 9:
        device_id, ip_address, _, _, _, _, hostname_vendor, _, _ = row
        device_data = {
            "ip_address": ip_address,
            "hostname_vendor": hostname_vendor
        }
        G.add_node(device_id, **device_data)
    else:
        # Handle the error here, such as skipping the row or logging a message
        print(f"Skipping invalid row: {row}")

# Iterate through the connections and add edges to the graph
for row in connection_rows:
    device_number, connected_device_number = row
    G.add_edge(device_number, connected_device_number)

# Visualize the network topology
pos = nx.spring_layout(G)  # Define the layout for the graph

# Create the main Tkinter window
root = Tk()
root.title("IoTShield™ Network Topology")
root.geometry("1200x800")

# Load and display the company logo
logo_path = "company_logo.png"  # Replace with the path to the company logo
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((int(logo_image.width * 0.25), int(logo_image.height * 0.25)))  # Reduce the size by 75%
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(root, image=logo_photo)
logo_label.pack(padx=10, pady=10)

# Create a refresh button
refresh_button = Button(root, text="Refresh", command=refresh_devices)
refresh_button.pack(pady=10)

# Create a label for displaying the current date and time
current_time_label = Label(root, text="", font=("Microsoft JhengHei UI", 14))
current_time_label.pack(pady=10)

# Function to update the current date and time label
def update_current_time_label():
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_time_label.config(text=f"Current Time: {current_time}")
    root.after(1000, update_current_time_label)

update_current_time_label()  # Start updating the current date and time label

# Create a canvas for displaying the network topology
canvas = FigureCanvasTkAgg(plt.figure(figsize=(8, 6)), master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Draw the network topology on the canvas
nx.draw_networkx_nodes(G, pos, node_color='b', node_size=200)
nx.draw_networkx_edges(G, pos, edge_color='r')
nx.draw_networkx_labels(G, pos, font_color='w')
plt.axis('off')

# Start the Tkinter event loop
root.mainloop()
