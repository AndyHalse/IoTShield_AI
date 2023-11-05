import logging
import os
from datetime import datetime
from tkinter import Label, LEFT, Tk
import tkinter
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
import sqlite3
from directories import DB_DIR, LOGS_DIR, REPORTS_DIR, BRAND_DIR, ICONS_DIR

class ReportGenerator:
    def __init__(self):
        self.banner_frame = Label()
        self.create_banner_frame()
        self.devices = self.load_devices_from_database()
        self.generate_pdf_report()

    def load_devices_from_database(self):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect("devices.db")
            cursor = conn.cursor()

            # Fetch all devices from the database
            cursor.execute("SELECT * FROM devices")
            devices = cursor.fetchall()

            # Close the database connection
            conn.close()

            return devices

        except sqlite3.Error as e:
            logging.error(f"Error loading devices from the database: {str(e)}")
            return []

    def create_header(self):
        logo = tkinter.PhotoImage(file=BRAND_DIR)
        logo_label = Tk.Label(self.parent, image=logo)
        logo_label.image = logo

    def create_banner_frame(self):
        logo_path = os.path.join(BRAND_DIR, "company_logo.png")
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((100, 100))
        self.logo_photo = ImageTk.PhotoImage(logo_image)
        self.logo_label = Label(self.banner_frame, image=self.logo_photo)
        self.logo_label.pack(side=LEFT)

    def generate_pdf_report(self):
        try:
            if not self.devices:
                logging.error("No devices found in the database.")
                return

            # Create the PDF reports directory if it doesn't exist
            pdf_reports_dir = REPORTS_DIR
            os.makedirs(pdf_reports_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            pdf_filename = os.path.join(REPORTS_DIR, f"IoTShield_Report_{timestamp}.pdf")
            c = canvas.Canvas(pdf_filename, pagesize=landscape(A4))

            # Generate the report content
            header_font = "Helvetica-Bold"
            entry_font = "Helvetica"
            y = 700

            headers = ["Device Number", "Device Name", "Device Type", "IP Address", "MAC Address"]

            # Draw the headers
            c.setFont(header_font, 12)
            for i, header in enumerate(headers):
                c.drawString(50 + i * 150, y, header)

            # Draw the device information
            c.setFont(entry_font, 10)
            for i, device in enumerate(self.devices):
                device_number = device[0] if len(device) > 0 else "N/A"
                device_name = device[1] if len(device) > 1 else "N/A"
                device_type = device[2] if len(device) > 2 else "N/A"
                ip_address = device[3] if len(device) > 3 else "N/A"
                mac_address = device[4] if len(device) > 4 and device[4] else "N/A"

                y -= 20

                c.drawString(50, y, str(device_number))
                c.drawString(100, y, device_name)
                c.drawString(250, y, device_type)
                c.drawString(400, y, ip_address)
                c.drawString(550, y, mac_address)

            c.showPage()
            c.save()

            print(f"PDF report generated successfully. Saved to: {pdf_filename}")

        except sqlite3.Error as e:
            logging.error(f"Error generating the PDF report: {str(e)}")

# Create an instance of the ReportGenerator class
report_generator = ReportGenerator()
