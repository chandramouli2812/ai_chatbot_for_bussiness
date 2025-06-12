import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        amount REAL,
        profit REAL
    )
    ''')

    # Add dummy data for today
    cur.execute("SELECT COUNT(*) FROM sales")
    if cur.fetchone()[0] == 0:
        today = datetime.now().strftime("%Y-%m-%d")
        for _ in range(10):
            cur.execute("INSERT INTO sales (date, amount, profit) VALUES (?, ?, ?)",
                        (today, 1000, 200))  # Modify as needed

    conn.commit()
    conn.close()
