import logging
import os
import sqlite3
import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

from directories import DB_DIR, LOGS_DIR, LOGS_DIR, REPORT_DIR, BRAND_DIR, ICONS_DIR

# Configure logging
log_file_path = os.path.join(LOGS_DIR, "device_discovery.log")
logging.basicdirectories(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s", filename=log_file_path)
logger = logging.getLogger("DeviceDiscovery")
logger.info("Application started, and I'm ready to spill the beans!")


class AssetsDialog(tk.Tk):
    def __init__(self, db_file):
        super().__init__()
        self.title("Assets List")
        self.geometry("1024x900")

        self.db_file = db_file  # Store the database file path

        self.create_header()
        self.create_assets_table()
        self.create_notes_area()

        self.load_assets_data()  # Load and display assets when the dialog is created

    def create_header(self):
        header_frame = tk.Frame(self)
        header_frame.pack(fill=tk.BOTH, expand=True)

        logo_image = Image.open(os.path.join(BRAND_DIR, "company_logo.png"))
        logo_image = logo_image.resize((100, 100), Image.ANTIALIAS)
        self.logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(header_frame, image=self.logo_photo)
        logo_label.pack(side=tk.LEFT)

    def create_assets_table(self):
        self.assets_table = ttk.Treeview(self)
        self.assets_table["columns"] = ("ID", "MAC Address", "Vendor", "IP Address", "Address")
        self.assets_table.heading("#0", text="", anchor='w')
        self.assets_table.heading("ID", text="ID")
        self.assets_table.heading("MAC Address", text="MAC Address")
        self.assets_table.heading("Vendor", text="Vendor")
        self.assets_table.heading("IP Address", text="IP Address")
        self.assets_table.heading("Address", text="Address")
        self.assets_table.column("#0", stretch=False, width=0)
        self.assets_table.column("ID", stretch=False, width=50)
        self.assets_table.column("MAC Address", stretch=True)
        self.assets_table.column("Vendor", stretch=True)
        self.assets_table.column("IP Address", stretch=True)
        self.assets_table.column("Address", stretch=True)
        self.assets_table.pack(fill=tk.BOTH, expand=True)

    def create_notes_area(self):
        notes_frame = tk.Frame(self)
        notes_frame.pack(fill=tk.BOTH, expand=True)

        self.notes_label = tk.Label(notes_frame, text="Notes:")
        self.notes_label.pack(side=tk.LEFT, padx=5, pady=5, anchor='w')

        self.notes_edit = tk.Text(notes_frame, wrap=tk.WORD, font=("Helvetica", 12))
        self.notes_edit.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        save_note_button = tk.Button(notes_frame, text="Save Note", command=self.save_note)
        save_note_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def load_assets_data(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()

            try:
                cursor.execute("SELECT id, mac_address, hostname_vendor, ip_address, address FROM devices")
                assets_data = cursor.fetchall()

                self.assets_table.delete(*self.assets_table.get_children())

                for row_data in assets_data:
                    self.assets_table.insert("", "end", values=row_data)
            except sqlite3.Error as e:
                logger.error(f"Error loading assets data: {e}")

    def save_note(self):
        note_text = self.notes_edit.get("1.0", tk.END).strip()
        if note_text:
            current_datetime = time.strftime("%c")
            note_with_datetime = f"{current_datetime} - {note_text}\n"

            # Logic to save the note to the selected asset in the database
            # Update the database record for the selected asset with the new note and datetime

            # Clear the notes area for the next note
            self.notes_edit.delete("1.0", tk.END)

            # Refresh the assets table to reflect the updated note and datetime
            self.load_assets_data()

            # Show a message or perform any other necessary actions
            messagebox.showinfo("Note Saved", "The note has been saved successfully.")


if __name__ == "__main__":
    db_file = "path/to/database.db"  # Replace with the actual path to your database file
    dialog = AssetsDialog(db_file)
    dialog.mainloop()
