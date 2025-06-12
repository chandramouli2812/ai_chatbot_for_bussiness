# from flask import Flask, render_template, request, jsonify
# from chatbot import ask_bot
# from data_loader import init_db

# app = Flask(__name__)
# init_db()

# @app.route("/")
# def home():
#     return render_template("index.html")

# # @app.route("/chat", methods=["POST"])
# # def chat():
# #     user_input = request.json["message"]
# #     response = ask_bot(user_input)
# #     return jsonify({"response": response})

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.json
#     user_input = data.get("message", "")
#     response = ask_bot(user_input)
#     print("User:", user_input)
#     print("Bot Response:", response)
#     return jsonify({"response": response})


# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# import sqlite3
# from chatbot import ask_bot
# from dotenv import load_dotenv
# import os

# app = Flask(__name__)
# load_dotenv()

# app.secret_key = os.getenv("FLASK_SECRET")

# # Login Manager Setup
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# # Dummy user (static for now)
# class User(UserMixin):
#     def __init__(self, id):
#         self.id = id
#         self.name = "admin"
#         self.password = "admin123"

# # Dummy user lookup
# users = {"admin": User(1)}

# @login_manager.user_loader
# def load_user(user_id):
#     return User(user_id)

# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         if username == "admin" and password == "admin123":
#             user = users["admin"]
#             login_user(user)
#             return redirect(url_for("chat"))
#         return render_template("login.html", error="Invalid credentials")
#     return render_template("login.html")

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("login"))

# @app.route("/chat")
# @login_required
# def chat():
#     return render_template("index.html")

# @app.route("/dashboard")
# @login_required
# def dashboard():
#     conn = sqlite3.connect("database.db")
#     cur = conn.cursor()
#     cur.execute("SELECT date, SUM(amount), SUM(profit) FROM sales GROUP BY date")
#     data = cur.fetchall()
#     conn.close()
#     return render_template("dashboard.html", chart_data=data)

# @app.route("/chat", methods=["POST"])
# @login_required
# def handle_chat():
#     user_input = request.json.get("message")
#     response = ask_bot(user_input)
#     return jsonify({"response": response})

# if __name__ == "__main__":
#     app.run(debug=True)



# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from chatbot import ask_bot
# from data_loader import init_db
# from dotenv import load_dotenv
# import sqlite3
# import os

# # Load environment variables
# load_dotenv()

# # Initialize app
# app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET") or "your_default_secret"
# init_db()

# # Login Manager Setup
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# # Dummy user class
# class User(UserMixin):
#     def __init__(self, id):
#         self.id = id
#         self.name = "admin"
#         self.password = "admin123"

# # Static user store for testing
# users = {"admin": User(1)}

# @login_manager.user_loader
# def load_user(user_id):
#     return User(user_id)

# # Login route
# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#         if username in users and password == users[username].password:
#             login_user(users[username])
#             return redirect(url_for("dashboard"))
#         return render_template("login.html", error="Invalid credentials")
#     return render_template("login.html")

# # Logout route
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("login"))

# # Dashboard route
# @app.route("/dashboard")
# @login_required
# def dashboard():
#     conn = sqlite3.connect("database.db")
#     cur = conn.cursor()
#     cur.execute("SELECT date, SUM(amount), SUM(profit) FROM sales GROUP BY date")
#     data = cur.fetchall()
#     conn.close()
#     return render_template("dashboard.html", chart_data=data)

# # Chat page
# @app.route("/chat")
# @login_required
# def chat_page():
#     return render_template("index.html")

# # Chat API
# @app.route("/chat", methods=["POST"])
# @login_required
# def handle_chat():
#     user_input = request.json.get("message")
#     response = ask_bot(user_input)
#     return jsonify({"response": response})

# # Start the app
# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# import sqlite3
# import os
# from chatbot import ask_bot
# from data_loader import init_db

# app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'
# init_db()

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# # User Class
# class User(UserMixin):
#     def __init__(self, id, username, role):
#         self.id = id
#         self.username = username
#         self.role = role

# # User loader
# @login_manager.user_loader
# def load_user(user_id):
#     with sqlite3.connect("database.db") as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
#         user_data = cursor.fetchone()
#         if user_data:
#             return User(*user_data)
#     return None

# @app.route("/", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]

#         with sqlite3.connect("database.db") as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
#             result = cursor.fetchone()

#         if result and password == result[2]:
#             user_id, uname, _, role = result
#             user = User(user_id, uname, role)
#             login_user(user)
#             session['user_id'] = user_id
#             session['username'] = uname
#             session['role'] = role
#             return redirect(url_for("dashboard"))
#         else:
#             return render_template("login.html", error="Invalid credentials")

#     return render_template("login.html")

# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     session.clear()
#     return redirect(url_for("login"))

# # @app.route("/dashboard")
# # @login_required
# # def dashboard():
# #     user_id = session['user_id']
# #     role = session['role']

# #     with sqlite3.connect("database.db") as conn:
# #         cursor = conn.cursor()
# #         if role == 'admin':
# #             cursor.execute("SELECT original_path, local_path, last_updated, user_id FROM file_metadata")
# #         else:
# #             cursor.execute("SELECT original_path, local_path, last_updated FROM file_metadata WHERE user_id = ?", (user_id,))
# #         paths = cursor.fetchall()

# #     return render_template("dashboard.html", paths=paths, role=role)
# @app.route("/dashboard")
# @login_required
# def dashboard():
#     user_id = session['user_id']
#     role = session['role']

#     with sqlite3.connect("database.db") as conn:
#         cursor = conn.cursor()
#         if role == 'admin':
#             cursor.execute("SELECT original_path, local_path, last_updated, user_id FROM file_metadata")
#         else:
#             cursor.execute("SELECT original_path, local_path, last_updated FROM file_metadata WHERE user_id = ?", (user_id,))
#         paths = cursor.fetchall()

#     return render_template("dashboard.html", paths=paths, role=role, username=session['username'])


# @app.route("/chat")
# @login_required
# def chat():
#     return render_template("index.html")

# # @app.route("/chat", methods=["POST"])
# # @login_required
# # def handle_chat():
# #     user_input = request.json.get("message")
# #     response = ask_bot(user_input)
# #     return jsonify({"response": response})
# # @app.route("/chat", methods=["POST"])
# # @login_required
# # def handle_chat():
# #     user_input = request.json.get("message")
# #     response = ask_bot(user_input)
# #     return jsonify({"response": response})
# @app.route("/chat", methods=["POST"])
# @login_required
# def handle_chat():
#     user_input = request.json.get("message").strip().lower()
#     user_id = session['user_id']

#     with sqlite3.connect('database.db') as conn:
#         cursor = conn.cursor()

#         # Handle: Add Path
#         if user_input.startswith("add path"):
#             path = user_input.replace("add path", "").strip()
#             local_dir = os.path.join('local_data', f'user_{user_id}')
#             os.makedirs(local_dir, exist_ok=True)
#             local_path = os.path.join(local_dir, os.path.basename(path))

#             cursor.execute("SELECT * FROM file_metadata WHERE original_path = ? AND user_id = ?", (path, user_id))
#             if cursor.fetchone():
#                 return jsonify({"response": f"🔔 Path already added: {path}"})
#             try:
#                 if os.path.exists(path):
#                     with open(path, 'rb') as src, open(local_path, 'wb') as dst:
#                         dst.write(src.read())
#                     cursor.execute(
#                         "INSERT INTO file_metadata (user_id, original_path, local_path, last_updated) VALUES (?, ?, ?, datetime('now'))",
#                         (user_id, path, local_path)
#                     )
#                     conn.commit()
#                     return jsonify({"response": f"✅ Path added successfully: {path}"})
#                 else:
#                     return jsonify({"response": f"⚠️ File does not exist: {path}"})
#             except Exception as e:
#                 return jsonify({"response": f"❌ Failed to add path: {e}"})

#         # Handle: Delete Path
#         elif user_input.startswith("delete path"):
#             path = user_input.replace("delete path", "").strip()
#             cursor.execute("DELETE FROM file_metadata WHERE original_path = ? AND user_id = ?", (path, user_id))
#             conn.commit()
#             return jsonify({"response": f"🗑️ Path deleted (if it existed): {path}"})

#         # Default: Chatbot logic
#         else:
#             response = ask_bot(user_input)
#             return jsonify({"response": response})


#     # Collect all local files added by this user
#     user_files = []
#     with sqlite3.connect("database.db") as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT local_path FROM file_metadata WHERE user_id = ?", (user_id,))
#         file_rows = cursor.fetchall()
#         for row in file_rows:
#             local_path = row[0]
#             if os.path.exists(local_path):
#                 user_files.append(local_path)

#     # Pass the user message + their files to the chatbot
#     response = ask_bot(user_input, files=user_files)

#     return jsonify({"response": response})




# @app.route('/add_path', methods=['POST'])
# def add_path():
#     if 'user_id' not in session:
#         return redirect(url_for('login'))

#     original_path = request.form['original_path'].strip()
#     user_id = session['user_id']

#     with sqlite3.connect('database.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM file_metadata WHERE original_path = ? AND user_id = ?", (original_path, user_id))
#         if cursor.fetchone():
#             flash("Path already added.")
#         else:
#             local_dir = os.path.join('local_data', f'user_{user_id}')
#             os.makedirs(local_dir, exist_ok=True)
#             local_path = os.path.join(local_dir, os.path.basename(original_path))
#             if os.path.exists(original_path):
#                 with open(original_path, 'rb') as src, open(local_path, 'wb') as dst:
#                     dst.write(src.read())
#             cursor.execute(
#                 "INSERT INTO file_metadata (user_id, original_path, local_path, last_updated) VALUES (?, ?, ?, datetime('now'))",
#                 (user_id, original_path, local_path)
#             )
#             conn.commit()
#             flash("Path added successfully.")
#     return redirect(url_for('dashboard'))

# @app.route("/delete_path", methods=["POST"])
# @login_required
# def delete_path():
#     if session['role'] != 'admin':
#         return "Unauthorized", 403

#     original_path = request.form['original_path'].strip()
#     with sqlite3.connect('database.db') as conn:
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM file_metadata WHERE original_path = ?", (original_path,))
#         conn.commit()
#         flash("Path deleted.")
#     return redirect(url_for('dashboard'))



# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import os
from werkzeug.utils import secure_filename
from chatbot import ask_bot
from data_loader import init_db
from database_setup import init_db

init_db()


# Config
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'xlsx', 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

# Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        if user_data:
            return User(*user_data)
    return None

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password, role FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

        if result and password == result[2]:
            user_id, uname, _, role = result
            user = User(user_id, uname, role)
            login_user(user)
            session['user_id'] = user_id
            session['username'] = uname
            session['role'] = role
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session['user_id']
    role = session['role']

    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        if role == 'admin':
            cursor.execute("SELECT original_path, local_path, last_updated, user_id FROM file_metadata")
        else:
            cursor.execute("SELECT original_path, local_path, last_updated FROM file_metadata WHERE user_id = ?", (user_id,))
        paths = cursor.fetchall()

    return render_template("dashboard.html", paths=paths, role=role, username=session['username'])

@app.route("/chat")
@login_required
def chat():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
@login_required
def handle_chat():
    user_input = request.json.get("message").strip()
    user_id = session['user_id']
    print(f"Received input: {user_input}")

    user_files = []
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT local_path FROM file_metadata WHERE user_id = ?", (user_id,))
        file_rows = cursor.fetchall()
        for row in file_rows:
            local_path = row[0]
            if os.path.exists(local_path):
                user_files.append(local_path)

    response = ask_bot(user_input, files=user_files)
    print("Bot response:", response)

    if not response.strip():
        response = "🤖 I'm here, but I didn't find any information to help with that question."

    return jsonify({"response": response})

@app.route('/add_path', methods=['POST'])
def add_path():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    original_path = request.form['original_path'].strip()
    original_path = os.path.normpath(original_path)
    description = request.form.get('description', '').strip()
    user_id = session['user_id']

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM file_metadata WHERE original_path = ? AND user_id = ?", (original_path, user_id))
        if cursor.fetchone():
            flash("⚠️ Path already added.")
        else:
            local_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'user_{user_id}')
            os.makedirs(local_dir, exist_ok=True)
            local_path = os.path.join(local_dir, os.path.basename(original_path))

            if os.path.exists(original_path):
                with open(original_path, 'rb') as src, open(local_path, 'wb') as dst:
                    dst.write(src.read())
                cursor.execute(
                    "INSERT INTO file_metadata (user_id, original_path, local_path, description, last_updated) VALUES (?, ?, ?, ?, datetime('now'))",
                    (user_id, original_path, local_path, description)
                )
                conn.commit()
                flash("✅ Path and description added successfully.")
            else:
                flash(f"❌ File does not exist: {original_path}")
    return redirect(url_for('dashboard'))

@app.route("/delete_path", methods=["POST"])
@login_required
def delete_path():
    if session['role'] != 'admin':
        return "Unauthorized", 403

    original_path = request.form['original_path'].strip()
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM file_metadata WHERE original_path = ?", (original_path,))
        conn.commit()
        flash("✅ Path deleted.")
    return redirect(url_for('dashboard'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('❌ No file part in the request.')
        return redirect(url_for('dashboard'))

    file = request.files['file']
    description = request.form.get('description', '').strip()
    user_id = session['user_id']

    if file.filename == '':
        flash('❌ No file selected.')
        return redirect(url_for('dashboard'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], f'user_{user_id}')
        os.makedirs(user_folder, exist_ok=True)

        local_path = os.path.join(user_folder, filename)
        file.save(local_path)

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO file_metadata (user_id, original_path, local_path, description, last_updated) VALUES (?, ?, ?, ?, datetime('now'))",
                           (user_id, filename, local_path, description))
            conn.commit()
            flash('✅ File uploaded successfully.')
    else:
        flash('❌ File type not allowed.')

    return redirect(url_for('dashboard'))

if __name__ == "__main__":
    app.run(debug=True)
