import datetime
import os
import sqlite3
from tkinter import *

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from directories import (DB_DIR)

DB_PATH = os.path.join(DB_DIR, "devices.db")


# Global variables
G = nx.Graph()
canvas = None
logo_photo = None  # Placeholder for logo_photo


# Function to refresh the devices from the SQL database
def refresh_devices():
    global G, canvas

    # Clear the current graph
    G.clear()

    # Connect to the SQLite database
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()

    # Fetch devices from the database
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()

    # Iterate through the devices and add nodes to the graph
    for device in devices:
        device_number = device[0]
        device_type = device[1]
        ip_address = device[2]
        hostname = device[3]

        # Add the device as a node to the graph
        G.add_node(device_number, device_type=device_type, 
                   ip_address=ip_address, hostname=hostname)

    # Analyze relationships and add edges based on network topology information
    cursor.execute("SELECT * FROM connections")
    connections = cursor.fetchall()
    for connection in connections:
        device_number = connection[0]
        connected_device_number = connection[1]
        # Add an edge between the devices
        G.add_edge(device_number, connected_device_number)

    # Close the database connection
    conn.close()

    if canvas:
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


# Function to save the network topology as a PDF
def save_to_pdf():
    with PdfPages('network_topology.pdf') as pdf:
        fig = plt.figure(figsize=(8, 6))
        nx.draw_networkx(G, pos, with_labels=True)
        plt.axis('off')
        pdf.savefig(fig)


# Create an empty NetworkX graph
G = nx.Graph()

# Visualize the network topology
pos = nx.spring_layout(G)  # Define the layout for the graph

# Create the main Tkinter window
root = Tk()
root.title("IoTShield™ Network Topology")
root.geometry("1500x900")

# Load and display the company logo
logo_path = "company_logo.png"  # Replace with the path to the company logo
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((int(logo_image.width * 0.25),
                                int(logo_image.height * 0.25)))
logo_photo = ImageTk.PhotoImage(logo_image)
logo_label = Label(root, image=logo_photo)
logo_label.pack(padx=10, pady=10)

# Create a refresh button
refresh_button = Button(root, text="Refresh", command=refresh_devices)
refresh_button.pack(side=TOP, padx=5)

# Create a save to PDF button
save_button = Button(root, text="Save to PDF", command=save_to_pdf)
save_button.pack(side=TOP, padx=5)

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
