import sqlite3
import logging
import os
from directories import (DB_DIR)

DB_PATH = os.path.join(DB_DIR, "devices.db")


def load_data_from_db():
    logging.info("Loading data from the database...")
    devices = []
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices")
            devices = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            devices = [dict(zip(columns, device)) for device in devices]
        logging.info(f"Fetched {len(devices)} devices from the database.")
    except sqlite3.Error as e:
        logging.error(f"Error while loading data from the database: {e}")

    return devices


def is_database_empty():
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


def check_database():
    logging.info(f"Connecting to database at: {DB_PATH}")
    if os.path.exists(DB_PATH):
        if os.access(DB_PATH, os.W_OK):
            logging.info("Write access to the database file confirmed.")
        else:
            logging.warning("No write access to the database file.")
    else:
        logging.error(f"Database file not found at {DB_PATH}")
