import os
import shutil
import sqlite3
import time
from datetime import datetime

DB_PATH = "database.db"
DATA_DIR = "data_store"

UPDATE_INTERVAL_SECONDS = 6 * 60 * 60  # 6 hours

def update_files():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT original_path, local_path FROM file_metadata")
        files = cursor.fetchall()

        for original_path, local_path in files:
            if os.path.exists(original_path):
                shutil.copy2(original_path, local_path)
                cursor.execute("""
                    UPDATE file_metadata
                    SET last_updated = ?
                    WHERE original_path = ?
                """, (datetime.now(), original_path))
            else:
                print(f"Warning: {original_path} does not exist anymore.")

        conn.commit()

def run_scheduler():
    while True:
        print(f"[Scheduler] Running update at {datetime.now()}...")
        update_files()
        print(f"[Scheduler] Sleeping for {UPDATE_INTERVAL_SECONDS} seconds...")
        time.sleep(UPDATE_INTERVAL_SECONDS)

if __name__ == "__main__":
    run_scheduler()
