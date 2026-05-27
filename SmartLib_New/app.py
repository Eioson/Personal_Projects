import os
import json
import time
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'smartlib_secret_key'

# Local database file routes
USER_DB_FILE = 'users.json'
BOOK_DB_FILE = 'book_list.json'
ROOM_DB_FILE = 'room_list.json'
RESERVATION_DB_FILE = 'reservations.json'

# --- AUTOMATED STARTUP DATABASE RESET ROUTINE ---

if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
    print("[DATABASE RESET] Initializing startup database clean-up...")

    baseline_books = {
        "The Architecture of Tomorrow: How Digital Networks Shape Human Behavior": {
            "media_type": "Physical",
            "author": "Dr. Evelyn Vance",
            "published": "2022-08-14",
            "available": True,
            "room": "General Area",
            "capacity": 10
        },
        "The Self-Hosted Frontier: A Practical Guide to NAS, Private Clouds, and Local Infrastructure": {
            "media_type": "Ebook",
            "author": "Julian Vance",
            "published": "2024-09-28",
            "available": False,
            "room": "General Area",
            "capacity": 10
        },
        "Signals in the Static: Foundations of Digital Communication and Wireless Networks": {
            "media_type": "Physical",
            "author": "Dr. Raymond Chen",
            "published": "2021-02-18",
            "available": True,
            "room": "General Area",
            "capacity": 10
        },
        "Bugs, Bytes, and Blue Screens: History\u00e2\u20ac\u2122s Most Costly Software Failures": {
            "media_type": "Ebook",
            "author": "Marcus Kim",
            "published": "2022-11-03",
            "available": True,
            "room": "General Area",
            "capacity": 10
        },
        "Ego Is the Enemy": {
            "media_type": "Physical",
            "author": "Ryan Holiday",
            "published": "2019-10-24",
            "available": False,
            "room": "General Area",
            "capacity": 10
        }
    }

    baseline_rooms = {
        "Study Room A": {
            "occupied": True,
            "time_until_available": "45 mins"
        },
        "Multimedia Room": {
            "occupied": True,
            "time_until_available": "25"
        },
        "Meeting Room A": {
            "occupied": True,
            "time_until_available": "45"
        },
        "Meeting Room B": {
            "occupied": True,
            "time_until_available": "25"
        }
    }

    try:
        # Overwrite book catalog back to default baseline profile state
        with open(BOOK_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(baseline_books, f, indent=4, ensure_ascii=False)

        # Overwrite collaborative room records back to default baseline state
        with open(ROOM_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(baseline_rooms, f, indent=4, ensure_ascii=False)

        # Hard-wipe all pending allocations back to an empty JSON array
        with open(RESERVATION_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4)

        print("[DATABASE RESET] Overwrote book catalog, study spaces, and reservation database logs.")
    except IOError as e:
        print(f"[DATABASE ERROR] Could not perform startup write reset: {e}")


# --- PERSISTENT FILE STORAGE UTILITIES ---

def load_users():
    """Loads institutional user accounts and normalizes older database formats."""
    if not os.path.exists(USER_DB_FILE):
        default_users = {
            "velascos@nu.edu.ph": {"password": "password123", "role": "student"},
            "patesel@student.nu-cebu.edu.ph": {"password": "password1234", "role": "student"},
            "teacher@nu.edu.ph": {"password": "password123", "role": "teacher"},
            "admin@nu.edu.ph": {"password": "password123", "role": "librarian"}
        }
        with open(USER_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_users, f, indent=4)
        return default_users

    with open(USER_DB_FILE, 'r', encoding='utf-8') as f:
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
                with open(USER_DB_FILE, 'w', encoding='utf-8') as f_out:
                    json.dump(sanitized, f_out, indent=4)
            return sanitized
        except json.JSONDecodeError:
            return {}


def load_books():
    """Loads active books catalog dynamically from JSON storage."""
    if not os.path.exists(BOOK_DB_FILE):
        return {}

    with open(BOOK_DB_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            dirty = False
            sanitized = {}
            for title, info in data.items():
                if isinstance(info, dict):
                    if "author" not in info:
                        info["author"] = "Unknown Author"
                        dirty = True
                    if "media_type" not in info:
                        info["media_type"] = "Hardcover Book"
                        dirty = True
                    if "published" not in info:
                        info["published"] = "N/A"
                        dirty = True
                    if "available" not in info:
                        info["available"] = True
                        dirty = True
                    sanitized[title] = info
                else:
                    sanitized[title] = {
                        "author": "Unknown Author",
                        "media_type": "Hardcover Book",
                        "published": "N/A",
                        "available": True
                    }
                    dirty = True

            if dirty:
                with open(BOOK_DB_FILE, 'w', encoding='utf-8') as f_out:
                    json.dump(sanitized, f_out, indent=4, ensure_ascii=False)
            return sanitized
        except json.JSONDecodeError:
            return {}


def load_rooms():
    """Loads study room inventory dynamically from JSON storage with status checks."""
    if not os.path.exists(ROOM_DB_FILE):
        return {}

    with open(ROOM_DB_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            dirty = False
            sanitized = {}
            for name, info in data.items():
                if isinstance(info, dict):
                    if "occupied" not in info:
                        info["occupied"] = False
                        dirty = True
                    if "time_until_available" not in info:
                        info["time_until_available"] = "Instant Access"
                        dirty = True

                    # Dynamic Normalization Layer: vacant spaces are kept at "Instant Access"
                    if not info["occupied"] and info["time_until_available"] != "Instant Access":
                        info["time_until_available"] = "Instant Access"
                        dirty = True

                    sanitized[name] = info
                else:
                    sanitized[name] = {"occupied": False, "time_until_available": "Instant Access"}
                    dirty = True

            if dirty:
                with open(ROOM_DB_FILE, 'w', encoding='utf-8') as f_out:
                    json.dump(sanitized, f_out, indent=4, ensure_ascii=False)
            return sanitized
        except json.JSONDecodeError:
            return {}


def load_reservations():
    """Loads room reservation requests dynamically from separate JSON array storage."""
    if not os.path.exists(RESERVATION_DB_FILE):
        with open(RESERVATION_DB_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4)
        return []

    with open(RESERVATION_DB_FILE, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                return []
            return data
        except json.JSONDecodeError:
            return []


def save_user(email, password, role):
    users = load_users()
    users[email] = {"password": password, "role": role}
    with open(USER_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)


def save_books(books):
    with open(BOOK_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, indent=4, ensure_ascii=False)


def save_rooms(rooms):
    with open(ROOM_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(rooms, f, indent=4, ensure_ascii=False)


def save_reservations(data):
    with open(RESERVATION_DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


# --- ROUTING ENDPOINTS ---

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
                user_role = users_db[input_username].get('role', '').lower().strip()

                # Dashboard-specific checkpoints redirection
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


# Unified Master Template Distributor
@app.route('/', methods=['GET', 'POST'])
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = request.args.get('username', 'Guest User').strip()
    role = request.args.get('role', 'guest').lower().strip()

    # Capture GET and POST parameter queries
    if request.method == 'POST':
        query = request.form.get('query', '').strip().lower()
        if request.form.get('username'): username = request.form.get('username').strip()
        if request.form.get('role'): role = request.form.get('role').lower().strip()
    else:
        query = request.args.get('query', '').strip().lower()

    books = load_books()
    rooms = load_rooms()
    book_results = None
    error_message = None

    if query:
        if query in books:
            book_results = books[query]
            book_results['title'] = query.title()
        else:
            error_message = f"Unfortunately, '{query.title()}' is not available. Please Try Again."

    # Pack dynamic payload parameters strictly to avoid template errors [2]
    render_payload = {
        'username': username,
        'role': role,
        'book': book_results,
        'error': error_message,
        'books': books,
        'rooms': rooms,
        'users': load_users(),
        'reservations': load_reservations()
    }

    if role == 'student':
        return render_template('student_dashboard.html', **render_payload)
    elif role == 'teacher':
        return render_template('teacher_dashboard.html', **render_payload)
    elif role == 'librarian':
        return render_template('librarian_dashboard.html', **render_payload)
    else:
        return render_template('guest_dashboard.html', **render_payload)


# --- ACTIONS HANDLERS (GUEST ACCESS CHECKPOINT GUARDED) ---

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
        reservations = load_reservations()
        integer_timestamp = int(time.time())

        # Construct queued reservation payload
        new_req = {
            "id": integer_timestamp,
            "room_name": room_name,
            "username": username,
            "time_slot": time_slot,
            "status": "pending"
        }
        reservations.append(new_req)
        save_reservations(reservations)
        flash(f"Reservation request for '{room_name}' submitted successfully and is pending review!", "success")
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


# Optimized: Consistently accepts 'title' from admin toggle action forms
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
        flash("Catalog item not found in records.", "error")

    return redirect(url_for('dashboard', username=username, role=role))


@app.route('/add_book', methods=['POST'])
def add_book():
    username = request.form.get('username')
    role = request.form.get('role', 'guest').strip().lower()

    if role == 'guest':
        flash("Action Restricted. Administrative authorization is required.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    title = request.form.get('title', '').strip().lower()
    author = request.form.get('author', 'Unknown Author').strip()
    media_type = request.form.get('media_type', 'Hardcover Reference').strip()
    published = request.form.get('published', '2026-05-27').strip()
    available = request.form.get('available') == 'true'

    if not title:
        flash("Title is a required field.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    books = load_books()
    books[title] = {
        "author": author,
        "media_type": media_type,
        "published": published,
        "available": available
    }
    save_books(books)

    flash(f"Registered material '{title.title()}' to storage catalog.", "success")
    return redirect(url_for('dashboard', username=username, role=role))


# Optimized: Evaluates room transitions and forces "Instant Access" when vacant
@app.route('/toggle_room', methods=['POST'])
def toggle_room():
    username = request.form.get('username')
    role = request.form.get('role', 'guest').strip().lower()

    if role == 'guest':
        flash("Action Restricted. Administrative authorization is required.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    room_name = request.form.get('room_name', '').strip()
    rooms = load_rooms()
    if room_name in rooms:
        currently_occupied = rooms[room_name].get('occupied', False)
        new_occupied_state = not currently_occupied
        rooms[room_name]['occupied'] = new_occupied_state

        if new_occupied_state:  # Vacant -> Occupied transition
            time_val = request.form.get('time_until_available', '').strip()
            if time_val:
                rooms[room_name]['time_until_available'] = time_val
            else:
                rooms[room_name]['time_until_available'] = "45 mins"
        else:  # Occupied -> Vacant transition (Forces "Instant Access")
            rooms[room_name]['time_until_available'] = "Instant Access"

        save_rooms(rooms)
        flash(f"Toggled occupancy state for '{room_name}'.", "success")
    else:
        flash("Workspace space not found.", "error")

    return redirect(url_for('dashboard', username=username, role=role))


# Optimized: Enforces vacant spaces to reset wait timers to "Instant Access" on creation
@app.route('/add_room', methods=['POST'])
def add_room():
    username = request.form.get('username')
    role = request.form.get('role', 'guest').strip().lower()

    if role == 'guest':
        flash("Action Restricted. Administrative authorization is required.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    room_name = request.form.get('room_name', '').strip()
    occupied = request.form.get('occupied') == 'true'

    if not room_name:
        flash("Room name is a required field.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    # Forced timeline checks
    if not occupied:
        time_limit = "Instant Access"
    else:
        time_limit = request.form.get('time_limit', '45 mins').strip()
        if not time_limit:
            time_limit = "45 mins"

    rooms = load_rooms()
    rooms[room_name] = {
        "occupied": occupied,
        "time_until_available": time_limit
    }
    save_rooms(rooms)

    flash(f"Registered collaborative space '{room_name}' to room registry.", "success")
    return redirect(url_for('dashboard', username=username, role=role))


# --- ADMINISTRATIVE WORKSPACE PIPELINE MUTATIONS ---

@app.route('/approve_reservation/<int:req_id>', methods=['POST'])
def approve_reservation(req_id):
    username = request.form.get('username', 'Guest User')
    role = request.form.get('role', 'librarian')

    if role == 'guest':
        flash("Action Restricted. Administrative authorization is required.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    reservations = load_reservations()
    rooms = load_rooms()

    target_res = None
    for res in reservations:
        if res.get('id') == req_id:
            target_res = res
            break

    if target_res:
        target_res['status'] = 'approved'
        room_name = target_res.get('room_name')
        time_slot = target_res.get('time_slot', '45 mins')

        # Synchronize and lock the status of study environments
        if room_name in rooms:
            rooms[room_name]['occupied'] = True
            rooms[room_name]['time_until_available'] = time_slot
            save_rooms(rooms)

        save_reservations(reservations)
        flash(f"Reservation Request #{req_id} approved. Collaborative space locked.", "success")
    else:
        flash("Specific reservation request not found.", "error")

    return redirect(url_for('dashboard', username=username, role=role))


@app.route('/reject_reservation/<int:req_id>', methods=['POST'])
def reject_reservation(req_id):
    username = request.form.get('username', 'Guest User')
    role = request.form.get('role', 'librarian')

    if role == 'guest':
        flash("Action Restricted. Administrative authorization is required.", "error")
        return redirect(url_for('dashboard', username=username, role=role))

    reservations = load_reservations()

    target_res = None
    for res in reservations:
        if res.get('id') == req_id:
            target_res = res
            break

    if target_res:
        target_res['status'] = 'rejected'
        save_reservations(reservations)
        flash(f"Reservation Request #{req_id} has been rejected.", "success")
    else:
        flash("Specific reservation request not found.", "error")

    return redirect(url_for('dashboard', username=username, role=role))


if __name__ == '__main__':
    app.run(debug=True)