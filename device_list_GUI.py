import logging
import traceback
import os
import sqlite3
import subprocess
import tkinter as tk
from tkinter import messagebox
import webbrowser
from datetime import datetime
from tkinter import IntVar, ttk
from PIL import Image, ImageTk
import network_scanner
from directories import (DB_DIR, ICONS_DIR, LOGS_DIR, BRAND_DIR)

DB_PATH = os.path.join(DB_DIR, "devices.db")
LOG_FILE = os.path.join(LOGS_DIR, "device_list_GUI.log")

logging.basicConfig(level=logging.DEBUG, filename=LOG_FILE, filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")


class IoTShieldDeviceList(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("IoTShield - Device List")
        self.geometry("1500x900")
        self.bg_color = "#6941C7"
        self.sidebar_color = "#6941C7"
        self.configure(bg="#6941C7")

        self.check_database_connection()

        if self.is_database_empty():
            logging.warning("Database is empty. Starting network scanner.")
            self.show_scanning_message()
            subprocess.run(["python", "network_scanner.py"])

        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.cursor = self.conn.cursor()
            logging.info("Successfully connected to the database.")
            self.create_sidebar()
            self.create_main_display()  # Changed this line
        except Exception as e:
            logging.error(f"Error while connecting to the database: {e}")
            msg = ("Database not found. Please ensure the database file "
                   "is in the correct location and try again.")
            messagebox.showerror("Database Error", msg)
            return

    def check_database_connection(self):
        """Validates the database connection and existence."""
        logging.info(f"Attempting to connect to database at: {DB_PATH}")

        if os.path.exists(DB_PATH):
            logging.info(f"Database file found at {DB_PATH}")
            if os.access(DB_PATH, os.W_OK):
                logging.info("Write access to the database file confirmed.")
            else:
                logging.warning("No write access to the database file.")
        else:
            logging.error(f"Database file not found at {DB_PATH}")

    def is_database_empty(self):
        """Check if the database file doesn't exist or is empty."""
        logging.info("Checking if the database is empty...")
        if not os.path.exists(DB_PATH):
            logging.warning(f"Database file does not exist at: {DB_PATH}")
            return True

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM devices")
                count = cursor.fetchone()[0]
                logging.info(f"Database has {count} entries.")
                return count == 0
        except sqlite3.Error as e:
            logging.error(f"Error while checking if database is empty: {e}")
            return True

    def check_database_and_scan(self):
        if self.is_database_empty():
            self.show_scanning_message()
            subprocess.run(["python", "network_scanner.py"])
            self.scanning_label.pack_forget()  # Hide scanning label.
        self.create_main_display()

    def show_scanning_message(self):
        """Display a message on the GUI indicating network is being scanned."""
        self.scanning_label = tk.Label(
            self, text="Scanning network...",
            font=("Arial", 12), bg=self.bg_color, fg="white"
        )
        self.scanning_label.pack(side=tk.BOTTOM, pady=5)

    def load_logo(self):
        logo_path = os.path.join(BRAND_DIR, "company_logo.png")
        if not os.path.exists(logo_path):
            logging.error(f"Logo image not found at {BRAND_DIR}")
            return
        logo_image = Image.open(logo_path)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self.sidebar_frame, image=logo_photo,
                              bg=self.sidebar_color)
        logo_label.image = logo_photo
        logo_label.pack(pady=20)

    def create_sidebar(self):
        logging.info("Creating sidebar...")
        print("Creating sidebar...")

        self.sidebar_frame = tk.Frame(
            self, bg=self.sidebar_color, width=300
        )
        self.sidebar_frame.pack(
            side=tk.LEFT, fill=tk.Y, padx=10, pady=10
        )
        try:
            logo_path = os.path.join(BRAND_DIR, "company_logo.png")
            logo_image = Image.open(logo_path).resize((180, 180))
            self.logo = ImageTk.PhotoImage(logo_image)
            self.logo_label = tk.Label(self.sidebar_frame, image=self.logo,
                                       bg=self.sidebar_color)
            self.logo_label.pack(pady=20)
        except Exception as e:
            logging.error(f"Failed to load logo: {e}, "
                          f"{traceback.format_exc()}")

        icons_files = {
            "Device List": "device_list.png",
            "Activity Monitor": "Activity_monitor.png",
            "Analyze": "Analyse.png",
            "Device Info": "device_Info.png",
            "PDF Generator": "PDF_Report.png",
            "Reports": "reports.png",
            "Settings": "settings.png",
            "Help": "help.png",
            "Our Website": "www.png"
        }

        for btn_text, icon_file in icons_files.items():
            image_path = os.path.join(ICONS_DIR, icon_file)
            if not os.path.exists(image_path):
                err_msg = (f"Image {icon_file} not found in {ICONS_DIR}")
                logging.error(err_msg)
                continue

            try:
                original_icon = Image.open(image_path).convert("RGBA")
                background = Image.new(
                    "RGBA", original_icon.size, self.sidebar_color
                )
                background.paste(original_icon, mask=original_icon)
                resized_icon = background.resize((35, 35))
                icon_image = ImageTk.PhotoImage(resized_icon)

                btn = tk.Button(
                    self.sidebar_frame,
                    text=btn_text,
                    image=icon_image,
                    compound="left",
                    bg=self.sidebar_color,
                    fg="white",
                    font=("Microsoft JhengHei UI", 12),
                    borderwidth=0,
                    relief="raised",
                    anchor='w'
                )
                btn.image = icon_image
                btn.pack(fill=tk.X, pady=10, padx=10)
            except Exception as e:
                logging.error(f"Failed to create button {btn_text} with icon "
                              f"{icon_file}: {e}, {traceback.format_exc()}")

        logging.info("Sidebar created successfully!")

    def update_datetime(self):
        now = datetime.now().strftime('%d %B %Y, %I:%M:%S %p')
        self.datetime_label.config(text=now)
        self.after(1000, self.update_datetime)

    def run_module(self, path):
        # Placeholder function to run the selected module
        print(f"Running module at path: {path}")

    def open_website(self):
        webbrowser.open("https://aicybersolutions.eu/")

    def create_main_display(self):
        logging.info("Creating main display...")

        # Main display frame
        self.main_display_frame = tk.Frame(self, bg=self.bg_color)
        self.main_display_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True
        )

        # Initialize self.main_frame
        self.main_frame = tk.Frame(self.main_display_frame)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.main_display = tk.Frame(
            self.main_frame, bg=self.bg_color, width=1000, height=800
        )
        self.main_display.pack(fill=tk.BOTH, expand=True)

        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(devices)")
                columns_info = cursor.fetchall()
                self.columns = [column[1] for column in columns_info]
                self.setup_data_area()
                self.setup_treeview()

                devices = self.load_data_from_db()
                columns_order = [
                    'ip_address', 'mac_address', 'last_seen', 'vendor',
                    'device_name', 'os', 'users', 'application_log',
                    'timestamp', 'bit_rate', 'device_type', 'device_model',
                    'location', 'open_ports', 'status', 'network_segment',
                    'customer_field', 'os_version'
                ]
                for device in devices:
                    values = [device[col] for col in columns_order]
                    self.device_table.insert('', 'end', values=values)

                self.adjust_column_width()

                # The rest of the setup calls
                self.setup_search_widgets()
                self.setup_status_and_progress_bar()
                self.setup_refresh_button()

            logging.info("Main display created successfully!")
        except Exception as e:
            logging.error(f"Error in create_main_display: {e}")
            if hasattr(self, 'scanning_label'):
                self.scanning_label.config(text=f"Error: {e}")

    def setup_main_display_frame(self):
        self.main_display = tk.Frame(self, bg="#1D1D28")
        self.main_display.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def setup_search_widgets(self):
        self.search_label = tk.Label(
            self.sidebar_frame,
            text="Search",
            fg="white",
            bg=self.sidebar_color
        )
        self.search_label.pack(pady=5, padx=10)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.sidebar_frame,
            textvariable=self.search_var
        )
        self.search_entry.pack(pady=10, padx=10, fill=tk.X)
        self.search_var.trace_add('write', self.filter_data)

    def setup_strapline(self):
        strapline_frame = tk.Frame(self, bg="#6941C7", height=50)
        strapline_frame.pack(fill=tk.X, pady=5)
        strap_line = tk.Label(
            strapline_frame,
            text="Welcome to IoTShield Device Manager",
            font=("Microsoft JhengHei UI", 15, "bold"),
            bg="#6941C7",
            fg="white"
        )
        strap_line.place(x=self.winfo_width(), y=15)
        self.animate_strapline(strap_line)

    def animate_strapline(self, strap_line):
        x = strap_line.winfo_x()
        if x < -strap_line.winfo_width():
            x = self.winfo_width()
        strap_line.place(x=x-1)
        self.after(10, lambda: self.animate_strapline(strap_line))

    def setup_data_area(self):
        self.data_frame = tk.Frame(self, bg="#6941C7")
        self.data_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

    def setup_status_and_progress_bar(self):
        # Progress Bar
        self.progress_var = IntVar()
        style = ttk.Style()
        style.configure("TProgressbar", thickness=20, background="#6941C7")
        self.progress_bar = ttk.Progressbar(
            self,
            orient=tk.HORIZONTAL,
            mode="determinate",
            variable=self.progress_var,
            maximum=100
        )
        self.progress_bar.pack(pady=10, padx=20, fill=tk.X)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self,
            textvariable=self.status_var,
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def on_scan_button_clicked(self, event):
        devices = network_scanner()  # Function return list of found devices
        self.display_devices(devices)

    def load_data_from_db(self):
        logging.info("Initiating process to load data from the database...")

        devices = []
        try:
            with sqlite3.connect(DB_PATH) as conn:
                logging.info("Successfully connected to the database.")
                cursor = conn.cursor()
                logging.info("Executing SELECT command to fetch entries...")
                cursor.execute("SELECT * FROM devices")
                devices = cursor.fetchall()
                logging.info(f"Successfully fetched {len(devices)} data.")
                # Convert the tuple data to dictionary format for easier usage
                columns = [desc[0] for desc in cursor.description]
                devices = [dict(zip(columns, device)) for device in devices]
                logging.info("Converted fetched data into dictionary format.")

        except sqlite3.Error as e:
            logging.error(f"Error encountered: {e}")
        return devices

    def populate_data(self):
        logging.info("Populating data from the database to the treeview...")

        if not os.path.exists(DB_PATH):
            logging.warning(
                "Database not found. Initiating ARP scan to load new data..."
            )
            network_scanner.NetworkScanner().perform_arp_scan()

        # Clear the treeview
        for record in self.device_table.get_children():
            self.device_table.delete(record)

        devices = self.load_data_from_db()

        if not devices:
            logging.warning(
                "No data found in the database. Initiating ARP scan..."
            )
            network_scanner.NetworkScanner().perform_arp_scan()
            devices = self.load_data_from_db()

        # Populate the treeview with the data
        for device in devices:
            # skipping the first column, assuming it's an ID column
            self.device_table.insert('', 'end', values=device[1:])
        logging.info("Data successfully populated into the treeview.")
        print(type(device), device)

    def refresh_data(self):
        logging.debug("Refreshing data...")
        # Clear the treeview
        for row in self.device_table.get_children():
            self.device_table.delete(row)
        # Load fresh data from the database
        devices = self.load_data_from_db()
        for device in devices:
            values_to_insert = (
                device["device_number"],
                device["ip_address"],
                device["mac_address"],
                device["last_seen"],
                device["vendor"],
                device["device_name"],
                device["os"],
                device["users"],
                device["application_log"],
                device["timestamp"]
            )
            self.device_table.insert("", "end", values=values_to_insert)
        # Update the GUI
        self.update_idletasks()

    def setup_treeview(self):
        logging.info("Starting setup_treeview...")
        style = ttk.Style()
        style.configure("Treeview", background="#d8c3f8",
                        rowheight=25)
        style.configure("Treeview.Heading", background="#6941C7")
        style.map('Treeview', background=[('selected', '#6941C7')])

        logging.info("Configured Treeview styles.")

        self.device_table = ttk.Treeview(self.data_frame,
                                         show="headings")
        column_names = [
            'ip_address', 'mac_address', 'last_seen', 'vendor',
            'device_name', 'os', 'users', 'application_log',
            'timestamp'
        ]
        self.device_table["columns"] = column_names

        logging.info("Initialized Treeview and set columns.")

        for col in column_names:
            self.device_table.heading(
                col, text=col.upper(),
                command=lambda c=col: self.sort_by_column(c)
            )
            self.device_table.column(col, width=125)

        logging.info("Configured Treeview columns.")

        self.device_table.pack(fill=tk.BOTH, expand=True,
                               padx=20, pady=5)
        logging.info("Finished setting up Treeview.")

    def adjust_column_width(self):
        for idx, col in enumerate(self.device_table["columns"]):
            max_len = max(
                [len(str(self.device_table.item(item)["values"][idx]))
                    for item in self.device_table.get_children()]
            )
            max_width = max(self.device_table.column(col, "width"), max_len)
            self.device_table.column(col, width=max_width)

    def filter_data(self, *args):
        search_term = self.search_var.get().lower()

        # Clear current items
        for row in self.device_table.get_children():
            self.device_table.delete(row)

        # Search across all columns
        columns_query = "PRAGMA table_info(devices);"
        columns_info = self.cursor.execute(columns_query).fetchall()
        column_names = [column[1] for column in columns_info]

        search_query_parts = [f"`{col}` LIKE ?" for col in column_names]
        search_query = " OR ".join(search_query_parts)
        search_values = ['%' + search_term + '%' for _ in column_names]

        query = f"SELECT * FROM devices WHERE {search_query}"
        for row in self.cursor.execute(query, search_values):
            self.device_table.insert("", "end", values=row)

    def sort_by_column(self, col):
        data = [
            (self.device_table.set(child, col), child)
            for child in self.device_table.get_children('')
        ]
        data.sort()

        for idx, item in enumerate(data):
            self.device_table.move(item[1], '', idx)


if __name__ == "__main__":
    app = IoTShieldDeviceList()
    app.mainloop()
