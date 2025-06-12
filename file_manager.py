import os
import shutil
import sqlite3
from datetime import datetime

DB_PATH = "database.db"  # Use existing DB if compatible
DATA_DIR = "data_store"

# Ensure local directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_path TEXT UNIQUE,
                local_path TEXT,
                description TEXT,
                last_updated TIMESTAMP
            )
        ''')
        conn.commit()

def add_file(original_path, description=""):
    if not os.path.exists(original_path):
        return "Error: File does not exist."

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM file_metadata WHERE original_path = ?", (original_path,))
        if cursor.fetchone():
            return "This file path is already added."

        filename = os.path.basename(original_path)
        local_path = os.path.join(DATA_DIR, filename)
        shutil.copy2(original_path, local_path)

        cursor.execute('''
            INSERT INTO file_metadata (original_path, local_path, description, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (original_path, local_path, description, datetime.now()))

        conn.commit()
    return "File added successfully."

def delete_file(original_path):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT local_path FROM file_metadata WHERE original_path = ?", (original_path,))
        row = cursor.fetchone()
        if not row:
            return "File path not found."

        local_path = row[0]
        if os.path.exists(local_path):
            os.remove(local_path)

        cursor.execute("DELETE FROM file_metadata WHERE original_path = ?", (original_path,))
        conn.commit()
    return "File deleted successfully."

def list_files():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_path, local_path, description, last_updated FROM file_metadata")
        return cursor.fetchall()

# Run on module load
init_db()
