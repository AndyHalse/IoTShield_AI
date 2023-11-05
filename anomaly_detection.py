import numpy as np
from sklearn.neighbors import LocalOutlierFactor
import networkx as nx
import sqlite3
import device_discovery

def extract_features(network_traffic):
    # Get the number of packets and bytes transferred in the network traffic
    num_packets = len(network_traffic)
    num_bytes = sum(packet['bytes'] for packet in network_traffic)

    # Compute the packet rate and byte rate
    duration = network_traffic[-1]['timestamp'] - network_traffic[0]['timestamp']
    packet_rate = num_packets / duration
    byte_rate = num_bytes / duration

    # Return the extracted features as a dictionary
    return {'num_packets': num_packets, 'num_bytes': num_bytes, 'packet_rate': packet_rate, 'byte_rate': byte_rate}

def normalize_features(features):
    # Compute the mean and standard deviation of the features
    mean = np.mean(features, axis=0)
    std = np.std(features, axis=0)

    # Normalize the features by subtracting the mean and dividing by the standard deviation
    normalized_features = (features - mean) / std

    # Return the normalized features
    return normalized_features

def apply_anomaly_detection(normalized_features):
    # Define the Local Outlier Factor model
    lof_model = LocalOutlierFactor(contamination='auto')
    
    # Fit the model on the normalized features
    lof_model.fit(normalized_features)
    
    # Predict the anomaly scores for the normalized features
    anomaly_scores = lof_model.negative_outlier_factor_
    
    # Define the threshold for considering a data point as an anomaly
    threshold = np.percentile(anomaly_scores, 5)
    
    # Find the indices of the anomalies
    anomaly_indices = np.where(anomaly_scores <= threshold)[0]
    
    # Return the list of anomaly indices
    return anomaly_indices

def detect_anomalies(network_data):
    """
    Function to detect anomalies in the network data.

    :param network_data: Dictionary containing network data
    """
    network_traffic = network_data.get("Network Traffic", [])

    if not network_traffic:
        print("No network traffic data available.")
        return []

    # Extract features from the network traffic data
    features = extract_features(network_traffic)

    # Normalize the features
    normalized_features = normalize_features(np.array(list(features.values())))

    # Apply anomaly detection techniques
    anomaly_indices = apply_anomaly_detection(normalized_features)

    # Connect to the SQL database
    conn = sqlite3.connect("devices.db")
    cursor = conn.cursor()

    # Get the network address using the device_discovery module
    network_address = device_discovery.get_network_address_with_netifaces()
    if not network_address:
        print("Unable to determine the network address.")
        return []

    # Create a weighted graph
    graph = nx.Graph()

    # Fetch devices from the database
    cursor.execute("SELECT * FROM devices")
    devices = cursor.fetchall()

    # Add nodes and edges from device discovery data
    connections = device_discovery.get_device_connections(devices)
    graph.add_nodes_from(devices)
    graph.add_weighted_edges_from(connections)

    # Find minimum spanning tree
    minimum_spanning_tree = nx.minimum_spanning_tree(graph)
    print("Minimum Spanning Tree:", minimum_spanning_tree.edges())

    # Compute maximum flow
    source_node = devices[0] if devices else None
    sink_node = devices[-1] if devices else None
    maximum_flow = nx.maximum_flow(graph, source_node, sink_node)
    print("Maximum Flow:", maximum_flow)

    # Perform analysis on each device
    for device in devices:
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
        print()

    # Close the database connection
    conn.close()

    # Return the detected anomaly indices
    return anomaly_indices

# Call the detect_anomalies function to perform the analysis and anomaly detection
detect_anomalies(network_data)
