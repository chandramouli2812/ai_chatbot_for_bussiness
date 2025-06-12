# auth_routes.py
from flask import Flask, request, session, redirect, url_for, render_template, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key
DB_PATH = 'database.db'

def get_user(username):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
        return cursor.fetchone()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        if user and user[2] == password:
            session['user_id'] = user[0]
            session['username'] = user[1]
            session['role'] = user[3]
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'user'

        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                               (username, password, role))
                conn.commit()
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                return render_template('register.html', error='Username already exists')

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return f"Welcome {session['username']} ({session['role']})"

if __name__ == '__main__':
    app.run(debug=True)
