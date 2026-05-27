import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'smartlib_secret_key'

# Local persistent database files
USER_DB_FILE = 'users.json'
BOOK_DB_FILE = 'book_inventory.json'


# --- DATABASE FILE HELPERS ---

def load_users():
    """Loads institutional user accounts and normalizes older database formats."""
    if not os.path.exists(USER_DB_FILE):
        default_users = {
            "velascos@nu.edu.ph": {"password": "password123", "role": "student"},
            "patesel@student.nu-cebu.edu.ph": {"password": "password1234", "role": "student"},
            "teacher@nu.edu.ph": {"password": "password123", "role": "teacher"},
            "admin@nu.edu.ph": {"password": "password123", "role": "librarian"}
        }
        with open(USER_DB_FILE, 'w') as f:
            json.dump(default_users, f, indent=4)
        return default_users

    with open(USER_DB_FILE, 'r') as f:
        try:
            data = json.load(f)
            dirty = False
            sanitized = {}
            for email, payload in data.items():
                if isinstance(payload, str):
                    sanitized[email] = {"password": payload, "role": "student"}
                    dirty = True
                elif isinstance(payload, dict):
                    if "role" not in payload:
                        payload["role"] = "student"
                        dirty = True
                    sanitized[email] = payload
                else:
                    sanitized[email] = {"password": "password123", "role": "student"}
                    dirty = True

            if dirty:
                with open(USER_DB_FILE, 'w') as f_out:
                    json.dump(sanitized, f_out, indent=4)
            return sanitized
        except json.JSONDecodeError:
            return {}


def load_books():
    """Loads physical catalog inventory from persistent JSON storage."""
    if not os.path.exists(BOOK_DB_FILE):
        default_books = {
            "lajan littera": {"room": "Room 1", "capacity": 15, "available": True},
            "data structures": {"room": "Room 2", "capacity": 30, "available": False}
        }
        with open(BOOK_DB_FILE, 'w') as f:
            json.dump(default_books, f, indent=4)
        return default_books

    with open(BOOK_DB_FILE, 'r') as f:
        try:
            data = json.load(f)
            dirty = False
            sanitized = {}
            for title, info in data.items():
                if isinstance(info, dict):
                    if "room" not in info:
                        info["room"] = "General Area"
                        dirty = True
                    if "capacity" not in info:
                        info["capacity"] = 10
                        dirty = True
                    if "available" not in info:
                        info["available"] = True
                        dirty = True
                    sanitized[title] = info
                else:
                    sanitized[title] = {"room": "General Area", "capacity": 10, "available": True}
                    dirty = True

            if dirty:
                with open(BOOK_DB_FILE, 'w') as f_out:
                    json.dump(sanitized, f_out, indent=4)
            return sanitized
        except json.JSONDecodeError:
            return {}


def save_user(email, password, role):
    users = load_users()
    users[email] = {"password": password, "role": role}
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)


def save_books(books):
    with open(BOOK_DB_FILE, 'w') as f:
        json.dump(books, f, indent=4)


# --- ROUTING LOGIC ---

# 1) THE HYPER-SPECIFIC LOGIN CHECKPOINT (Role extracted directly from database payload)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error_msg = None
    if request.method == 'POST':
        input_username = request.form.get('username', '').strip()
        input_password = request.form.get('password', '').strip()

        users_db = load_users()

        if input_username in users_db:
            correct_password = users_db[input_username].get('password')

            if input_password == correct_password:
                # Extracts role string from persistent storage data
                user_role = users_db[input_username].get('role', '').lower().strip()

                # Forced redirection handoffs
                if user_role == 'student':
                    print(f"[AUTH SUCCESS] Routing {input_username} to STUDENT dashboard.")
                    return redirect(url_for('dashboard', username=input_username, role='student'))

                elif user_role == 'teacher' or user_role == 'faculty':
                    print(f"[AUTH SUCCESS] Routing {input_username} to TEACHER dashboard.")
                    return redirect(url_for('dashboard', username=input_username, role='teacher'))

                elif user_role == 'librarian' or user_role == 'admin':
                    print(f"[AUTH SUCCESS] Routing {input_username} to LIBRARIAN dashboard.")
                    return redirect(url_for('dashboard', username=input_username, role='librarian'))

                else:
                    print(f"[WARNING] Unknown role '{user_role}'. Defaulting to guest.")
                    return redirect(url_for('dashboard', username=input_username, role='guest'))
            else:
                error_msg = "Incorrect password. Please try again."
        else:
            error_msg = "Username or Email not found in our database."

    return render_template('login.html', error=error_msg)


# 2) ACCOUNT CREATION LOGIC (Role dropdown active on frontend form)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_msg = None
    if request.method == 'POST':
        email = request.form.get('username', '').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = request.form.get('role', 'student').lower().strip()

        if not email or not password or not confirm_password or not role:
            error_msg = "All registration fields are required."
        elif password != confirm_password:
            error_msg = "Passwords do not match."
        else:
            users = load_users()
            if email in users:
                error_msg = "This account is already registered."
            else:
                save_user(email, password, role)
                flash("Registration successful!", "success")
                return redirect(url_for('dashboard', username=email, role=role))

    return render_template('signup.html', error=error_msg)


# 3) DECOUPLED MULTI-DASHBOARD DISTRIBUTOR
@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = request.args.get('username', 'Guest User').strip()
    role = request.args.get('role', 'guest').lower().strip()

    # Capture state arguments from search POST or address bar GET requests
    if request.method == 'POST':
        query = request.form.get('query', '').strip().lower()
        if request.form.get('username'): username = request.form.get('username').strip()
        if request.form.get('role'): role = request.form.get('role').lower().strip()
    else:
        query = request.args.get('query', '').strip().lower()

    books = load_books()
    book_results = None
    error_message = None

    if query:
        if query in books:
            book_results = books[query]
            book_results['title'] = query.title()
        else:
            error_message = f"Unfortunately, '{query.title()}' is not available. Please Try Again."

    # Direct conditional file dispatching
    if role == 'student':
        return render_template('student_dashboard.html', username=username, role=role, book=book_results, error=error_message)
    elif role == 'teacher':
        return render_template('teacher_dashboard.html', username=username, role=role, book=book_results, error=error_message, books=books)
    elif role == 'librarian':
        return render_template('librarian_dashboard.html', username=username, role=role, book=book_results, error=error_message, books=books, users=load_users())
    else:
        return render_template('guest_dashboard.html', username=username, role='guest', book=book_results, error=error_message)


# --- MUTATION ENDPOINTS (GUEST PROTECTION INCLUDED) ---

@app.route('/reserve_space', methods=['POST'])
def reserve_space():
    username = request.form.get('username')
    role = request.form.get('role', 'guest').strip().lower()

    if role == 'guest':
        flash("Action Restricted. Guest status accounts are blocked from reserving workspaces.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    room_name = request.form.get('room_name', '').strip()
    time_slot = request.form.get('time_slot', '').strip()

    if room_name and time_slot:
        flash(f"Classroom reserved: '{room_name}' for slot '{time_slot}'!", "success")
    else:
        flash("Room and Time parameters are required.", "error")

    return redirect(url_for('dashboard', username=username, role=role))


@app.route('/suggest_book', methods=['POST'])
def suggest_book():
    username = request.form.get('username')
    role = request.form.get('role', 'guest').strip().lower()

    if role == 'guest':
        flash("Action Restricted. Guest status accounts are blocked from recommending books.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    book_title = request.form.get('book_title', '').strip()
    if book_title:
        flash(f"Material proposal for '{book_title}' has been successfully logged.", "success")
    else:
        flash("Proposal details are required.", "error")

    return redirect(url_for('dashboard', username=username, role=role))


@app.route('/toggle_book', methods=['POST'])
def toggle_book():
    username = request.form.get('username')
    role = request.form.get('role', 'guest').strip().lower()

    if role == 'guest':
        flash("Action Restricted. Administrative authorization is required.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    title = request.form.get('title', '').strip().lower()
    books = load_books()
    if title in books:
        books[title]['available'] = not books[title]['available']
        save_books(books)
        flash(f"Modified catalog availability for '{title.title()}'.", "success")
    else:
        flash("Catalog item not found.", "error")

    return redirect(url_for('dashboard', username=username, role=role))


@app.route('/add_book', methods=['POST'])
def add_book():
    username = request.form.get('username')
    role = request.form.get('role', 'guest').strip().lower()

    if role == 'guest':
        flash("Action Restricted. Administrative authorization is required.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    title = request.form.get('title', '').strip().lower()
    room = request.form.get('room', '').strip()
    capacity = request.form.get('capacity', '0')
    available = request.form.get('available') == 'true'

    if not title or not room:
        flash("Title and assigned catalog room are required fields.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    try:
        cap_val = int(capacity)
    except ValueError:
        cap_val = 10

    books = load_books()
    books[title] = {"room": room, "capacity": cap_val, "available": available}
    save_books(books)

    flash(f"Registered material '{title.title()}' to storage catalog.", "success")
    return redirect(url_for('dashboard', username=username, role=role))


if __name__ == '__main__':
    app.run(debug=True)