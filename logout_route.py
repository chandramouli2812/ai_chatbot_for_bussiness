# logout_route.py
from flask import Flask, redirect, url_for, session, render_template, request, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
DB_PATH = 'database.db'
LOCAL_COPY_DIR = 'local_data'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session.get('role', 'user')

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if role == 'admin':
            cursor.execute("SELECT original_path, local_path, last_updated, user_id FROM file_metadata")
        else:
            cursor.execute("SELECT original_path, local_path, last_updated FROM file_metadata WHERE user_id = ?", (user_id,))
        paths = cursor.fetchall()

    return render_template("dashboard.html", paths=paths, role=role)

@app.route('/add_path', methods=['POST'])
def add_path():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    original_path = request.form['original_path'].strip()
    user_id = session['user_id']

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM file_metadata WHERE original_path = ? AND user_id = ?", (original_path, user_id))
        if cursor.fetchone():
            flash("Path already added.")
        else:
            local_path = os.path.join(LOCAL_COPY_DIR, f'user_{user_id}', os.path.basename(original_path))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            if os.path.exists(original_path):
                with open(original_path, 'rb') as fsrc, open(local_path, 'wb') as fdst:
                    fdst.write(fsrc.read())
            cursor.execute("INSERT INTO file_metadata (user_id, original_path, local_path, last_updated) VALUES (?, ?, ?, datetime('now'))",
                           (user_id, original_path, local_path))
            conn.commit()
            flash("Path added successfully.")

    return redirect(url_for('dashboard'))

@app.route('/delete_path', methods=['POST'])
def delete_path():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    original_path = request.form['original_path'].strip()
    user_id = session['user_id']
    role = session['role']

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if role == 'admin':
            cursor.execute("SELECT local_path FROM file_metadata WHERE original_path = ?", (original_path,))
        else:
            cursor.execute("SELECT local_path FROM file_metadata WHERE original_path = ? AND user_id = ?", (original_path, user_id))

        result = cursor.fetchone()
        if result:
            local_path = result[0]
            if os.path.exists(local_path):
                os.remove(local_path)
            cursor.execute("DELETE FROM file_metadata WHERE original_path = ?" + ("" if role == 'admin' else " AND user_id = ?"),
                           (original_path,) if role == 'admin' else (original_path, user_id))
            conn.commit()
            flash("Path deleted successfully.")
        else:
            flash("Path not found or not authorized.")

    return redirect(url_for('dashboard'))
