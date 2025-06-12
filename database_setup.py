# # database_setup.py
# import sqlite3

# def setup_database():
#     conn = sqlite3.connect("database.db")
#     cursor = conn.cursor()

#     # Create users table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL,
#             role TEXT NOT NULL CHECK(role IN ('admin', 'user'))
#         )
#     ''')

#     # Create file metadata table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS file_metadata (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER NOT NULL,
#             original_path TEXT NOT NULL,
#             local_path TEXT NOT NULL,
#             last_updated TEXT,
#             FOREIGN KEY(user_id) REFERENCES users(id)
#         )
#     ''')

#     # Optional: Insert default admin user (password is 'admin123')
#     cursor.execute("SELECT * FROM users WHERE username = 'admin'")
#     if not cursor.fetchone():
#         cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
#                        ('admin', 'admin123', 'admin')
#                        ('mouli', 'mouli123', 'User'))

#     conn.commit()
#     conn.close()

# if __name__ == '__main__':
#     setup_database()
#     print("Database initialized.")
import sqlite3
import os

def init_db():
    db_path = os.path.join(os.getcwd(), 'database.db')  # Adjust as needed
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the file_metadata table with all required columns
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS file_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        file_path TEXT,
        description TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized with file_metadata table.")
