# dashboard_view.py
from flask import Flask, session, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)
DB_PATH = 'database.db'

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    role = session['role']

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        if role == 'admin':
            cursor.execute("SELECT original_path, local_path, last_updated FROM file_metadata")
        else:
            cursor.execute("SELECT original_path, local_path, last_updated FROM file_metadata WHERE user_id = ?", (user_id,))

        paths = cursor.fetchall()

    return render_template('dashboard.html', paths=paths, username=session['username'], role=role)

if __name__ == '__main__':
    app.secret_key = 'your_secret_key_here'
    app.run(debug=True)
