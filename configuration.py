import logging
from msilib.schema import SelfReg
import os
import sqlite3
import tkinter as tk

from networkx import selfloop_edges
from directories import BRAND_DIR
from tkinter import filedialog, ttk
from typing import Self
from PIL import Image, ImageTk
from directories import DB_DIR, LOGS_DIR, LOGS_DIR, REPORT_DIR, BRAND_DIR, ICONS_DIR, DB_DIR

# Configure logging
logging.basicdirectories(level=logging.DEBUG)

def initialize_components(self):
    self.primary_color_var = tk.StringVar()
    self.secondary_color_var = tk.StringVar()
    self.header1_var = tk.StringVar(value="Header 1")
    self.header2_var = tk.StringVar(value="Header 2")
    self.ip_range_var = tk.StringVar(value="192.168.1.1-192.168.1.255")
    self.exclude_ips_var = tk.StringVar(value="192.168.1.1,192.168.1.2")
    self.pdf_author_var = tk.StringVar(value="Default Author")
    self.pdf_title_prefix_var = tk.StringVar(value="Report: ")
    self.configuration_button.pack()
    self.header_mapping_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    self.header_mapping_frame = ttk.Frame(self)
    self.configuration_button = ttk.Button(self.header_mapping_frame, text="Configuration", command=self.run_configuration_dialog)

    self.header_mapping_table = ttk.Treeview(self.header_mapping_frame, columns=["Header", "Mapped Data"])
    self.header_mapping_table.heading("#0", text="", anchor='w')
    self.header_mapping_table.heading("Header", text="Header")
    self.header_mapping_table.heading("Mapped Data", text="Mapped Data")
    self.header_mapping_table.column("#0", stretch=False, width=0)
    self.header_mapping_table.column("Header", stretch=True)
    self.header_mapping_table.column("Mapped Data", stretch=True)
    self.header_mapping_table.pack(fill=tk.BOTH, expand=True)
    self.display_logo(self.logo_path_var.get())

class ConfigurationDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Configuration")
        self.initUI()
#         self.initialize_components()

    def initUI(self):
        logging.debug("Initializing UI")
        layout = ttk.Notebook(self)

        # Create tabs
        directories_tab = ttk.Frame(layout)
        logo_tab = ttk.Frame(layout)
        header_mapping_tab = ttk.Frame(layout)

        layout.add(directories_tab, text="Directories")
        layout.add(logo_tab, text="Logo")
        layout.add(header_mapping_tab, text="Header Mapping")

        self.create_directories_tab(directories_tab)
        self.create_logo_tab(logo_tab)
        self.create_header_mapping_tab(header_mapping_tab)

        layout.pack(fill=tk.BOTH, expand=True)

    def fetch_directories_from_db(self):
        database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'devices.db')
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT Directory FROM devices")
        directories = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return directories


    def create_directories_tab(self, parent):
        directories_frame = ttk.Frame(parent)
        directories_frame.pack(fill=tk.BOTH, expand=True)

        # ... (Add the rest of the code for Directories Configuration tab here)

    def create_logo_tab(self, parent):
        logo_frame = ttk.Frame(parent)
        logo_frame.pack(fill=tk.BOTH, expand=True)

    
    def create_branding_colors_tab(self, parent):
        colors_frame = ttk.Frame(parent)
        colors_frame.pack(fill=tk.BOTH, expand=True)
        
        default_colors = ["#6941C7","#7E56DA","#54389E","#bb8fce", "#a569bd", "#8e44ad", "#7d3c98", "#6c3483"]
        
        ttk.Label(colors_frame, text="Select Branding Colors", font=("Microsoft JhengHei UI", 14)).pack(row=0, column=0, sticky='w', pady=10, padx=10, columnspan=2)
        
        self.primary_color_var = tk.StringVar()
        self.secondary_color_var = tk.StringVar()
        
        ttk.Label(colors_frame, text="Primary Color").pack(row=1, column=0, sticky='w', padx=10)
        primary_color_combobox = ttk.Combobox(colors_frame, values=default_colors, textvariable=self.primary_color_var)
        primary_color_combobox.pack(row=1, column=1, padx=10, pady=5, sticky='ew')
        primary_color_combobox.set(default_colors[0])
        
        ttk.Label(colors_frame, text="Secondary Color").pack(row=2, column=0, sticky='w', padx=10)
        secondary_color_combobox = ttk.Combobox(colors_frame, values=default_colors, textvariable=self.secondary_color_var)
        secondary_color_combobox.pack(row=2, column=1, padx=10, pady=5, sticky='ew')
        secondary_color_combobox.set(default_colors[1])

    def create_header_renaming_tab(self, parent):
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(header_frame, text="Rename Headers", font=('Arial', 14)).pack(row=0, column=0, sticky='w', pady=10, padx=10, columnspan=2)
        
        self.header1_var = tk.StringVar(value="Header 1")
        self.header2_var = tk.StringVar(value="Header 2")
        
        ttk.Label(header_frame, text="Header 1").pack(row=1, column=0, sticky='w', padx=10)
        ttk.Entry(header_frame, textvariable=self.header1_var).pack(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(header_frame, text="Header 2").pack(row=2, column=0, sticky='w', padx=10)
        ttk.Entry(header_frame, textvariable=self.header2_var).pack(row=2, column=1, padx=10, pady=5, sticky='ew')

    def create_network_configuration_tab(self, parent):
        network_frame = ttk.Frame(parent)
        network_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(network_frame, text="Network Configuration", font=('Arial', 14)).pack(row=0, column=0, sticky='w', pady=10, padx=10, columnspan=2)
        
        self.ip_range_var = tk.StringVar(value="192.168.1.1-192.168.1.255")
        self.exclude_ips_var = tk.StringVar(value="192.168.1.1,192.168.1.2")
        
        ttk.Label(network_frame, text="IP Range to Scan").pack(row=1, column=0, sticky='w', padx=10)
        ttk.Entry(network_frame, textvariable=self.ip_range_var).pack(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(network_frame, text="Exclude IPs").pack(row=2, column=0, sticky='w', padx=10)
        ttk.Entry(network_frame, textvariable=self.exclude_ips_var).pack(row=2, column=1, padx=10, pady=5, sticky='ew')

    def create_pdf_generation_tab(self, parent):
        pdf_frame = ttk.Frame(parent)
        pdf_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(pdf_frame, text="PDF Generation Configuration", font=('Arial', 14)).pack(row=0, column=0, sticky='w', pady=10, padx=10, columnspan=2)
        
        self.pdf_author_var = tk.StringVar(value="Default Author")
        self.pdf_title_prefix_var = tk.StringVar(value="Report: ")
        
        ttk.Label(pdf_frame, text="Author Name").pack(row=1, column=0, sticky='w', padx=10)
        ttk.Entry(pdf_frame, textvariable=self.pdf_author_var).pack(row=1, column=1, padx=10, pady=5, sticky='ew')
        
        ttk.Label(pdf_frame, text="Title Prefix").pack(row=2, column=0, sticky='w', padx=10)
        ttk.Entry(pdf_frame, textvariable=self.pdf_title_prefix_var).pack(row=2, column=1, padx=10, pady=5, sticky='ew')

    def create_header_mapping_tab(self, parent):
        header_mapping_frame = ttk.Frame(parent)
        header_mapping_frame.pack(fill=tk.BOTH, expand=True)

        self.configuration_button = ttk.Button(header_mapping_frame, text="Configuration", command=self.run_configuration_dialog)
        self.configuration_button.pack()

        self.header_mapping_frame = ttk.Frame(self)
        self.header_mapping_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.header_mapping_table = ttk.Treeview(self.header_mapping_frame, columns=["Header", "Mapped Data"])
        self.header_mapping_table.heading("#0", text="", anchor='w')
        self.header_mapping_table.heading("Header", text="Header")
        self.header_mapping_table.heading("Mapped Data", text="Mapped Data")
        self.header_mapping_table.column("#0", stretch=False, width=0)
        self.header_mapping_table.column("Header", stretch=True)
        self.header_mapping_table.column("Mapped Data", stretch=True)
        self.header_mapping_table.pack(fill=tk.BOTH, expand=True)

    def run_configuration_dialog(self):
        dialog = tk.Tk()(self)
        dialog.title("Configuration Dialog")


if __name__ == "__main__":
    app = ConfigurationDialog()
    app.mainloop()
#     selfloop_edges.display_logo(self.logo_path_var.get())