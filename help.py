# help_file.py

help_text = """
Help File for IoTShield™ Application

Table of Contents

Introduction
System Requirements
Installation
User Interface
4.1. GUI Overview
4.2. Searching and Filtering Devices
4.3. Pie Chart Display
4.4. Live Network Structure Display
4.5. Color Swatch
4.6. Notifications
Reports
Logo Integration
Time and Date Display
Secure Logging
Exit and Help Buttons
Sending Email with Data and Graphics
1. Introduction

Thank you for choosing IoTShield™, an application designed to automatically detect and identify IP devices on LAN/WAN networks, including IoT devices vulnerable to outside hackers. This help file provides comprehensive guidance on using the application effectively to enhance your network security.

2. System Requirements

Before installing IoTShield™, please ensure that your system meets the following requirements:

Operating System: [List compatible operating systems]
Processor: [Minimum processor requirements]
RAM: [Minimum RAM requirements]
Disk Space: [Minimum disk space requirements]
Internet Connection: Required for machine learning algorithms and email notifications
3. Installation

To install IoTShield™, please follow these steps:

[Step 1]
[Step 2]
[Step 3]
[Step 4]
[Step 5]
4. User Interface

The IoTShield™ application provides a user-friendly GUI to monitor and manage network devices. The following sections explain various features of the GUI:

4.1. GUI Overview

Upon launching IoTShield™, the GUI displays an expanding pack that lists all detected devices. Each device is represented by a relevant device type icon image, along with its IP address, device name, device type, device software/firmware version number, Mac address, CPU data, memory data, and other relevant information.

4.2. Searching and Filtering Devices

To search for specific devices based on their IP address or name, use the search and filter feature provided in the GUI. Simply enter the IP address or name in the designated search field, and the GUI will update accordingly to display the filtered results.

4.3. Pie Chart Display

The GUI includes a visually informative pie chart that illustrates the distribution of normal and abnormal devices on the network. The chart helps users quickly identify the overall network health.

4.4. Live Network Structure Display

To visualize the entire network structure with both nominal and abnormal bi-directional data, IoTShield™ provides a live graphical display. This feature allows users to monitor network devices in real-time and identify any anomalies detected by the machine learning algorithms.

4.5. Color Swatch

The GUI incorporates a color swatch using the following hex color codes: #5a17d6, #a37cf0, #420889, #8816ce, 9980d1. These colors are used to enhance visual elements and distinguish different components within the application.

4.6. Notifications

IoTShield™ sends notifications when certain limits have been reached or unusual behavior in data packets has been detected. Users can configure the triggers for these notifications. The email content includes comprehensive information about the device with over-limit or abnormal behavior.

5. Reports

IoTShield™ generates basic reports in PDF format that provide valuable information on network devices, bi-directional byte rates, and any anomalies or security threats detected by the anomaly detection machine learning algorithms. These reports help users analyze network performance and identify potential vulnerabilities.

6. Logo Integration

Both the GUI and PDF reports can be customized with your company's logo. To integrate your logo into IoTShield™, simply place a file named 'logo.png' in the same directory as the application.

7. Time and Date Display

To keep track of activities and provide accurate timestamps, IoTShield™ displays the current time and date on both the GUI and PDF reports.

8. Secure Logging

IoTShield™ creates logs that track all activities and ensures their security from hackers. These logs help users monitor the application's performance, troubleshoot issues, and maintain a secure network environment.

9. Exit and Help Buttons

The GUI includes an exit button to close the application when you have finished using it. Additionally, a help button is available to provide quick access to this help file for any assistance required.

10. Sending Email with Data and Graphics

IoTShield™ enables users to send comprehensive data and graphics in a single email. By selecting the appropriate option within the application, users can generate an email containing all relevant information, aiding in communication and sharing of insights.

Should you require any further assistance or encounter any issues while using IoTShield™, please refer to this help file or reach out to our support team at [support email/phone]. We are committed to ensuring your network's security and are here to help you every step of the way.
"""

# Create a HelpFile class to encapsulate the help file functionality
class HelpFile:
    def __init__(self):
        pass

    def show_help(self):
        print(help_text)

# Create an instance of HelpFile and call the show_help method to display the help text
help_file = HelpFile()
help_file.show_help()
