import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'smartlib_secret_key'

# Path to our lightweight JSON database file
DB_FILE = 'users.json'


def load_users():
    """Loads users from the JSON file. If the file doesn't exist, initializes it with defaults."""
    if not os.path.exists(DB_FILE):
        default_users = {
            "solomon@nu.edu.ph": "password123",
            "edison@nu.edu.ph": "pass456",
            "kevin@nu.edu.ph": "pass789"
        }
        with open(DB_FILE, 'w') as f:
            json.dump(default_users, f, indent=4)
        return default_users

    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_user(email, password):
    """Appends a new user account directly to our persistent storage."""
    users = load_users()
    users[email] = password
    with open(DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)


# Book inventory tracker matching your project specs
BOOK_INVENTORY = {
    "lajan littera": {"room": "Room 1", "capacity": 15, "available": True},
"data structures": {"room": "Room 2", "capacity": 30, "available": False}
}

# --- 1) SIGN UP & CONFIRM --> HOMEPAGE FLOW ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not email or not password or not confirm_password:
            flash("All fields are required.", "error")
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for('signup'))

        # Check the persistent database file
        users = load_users()
        if email in users:
            flash("This email is already registered in the system.", "error")
            return redirect(url_for('signup'))

        # Save to file permanently
        save_user(email, password)

        # FLOW 1: Automagically log them in and redirect straight to the homepage upon confirmation!
        flash("Account created successfully!", "success")
        return redirect(url_for('dashboard', username=email))

    return render_template('signup.html')


# --- 2) LOGIN --> HOMEPAGE FLOW ---
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        if not email or not password:
            flash("Please fill out all details.", "error")
            return redirect(url_for('login'))

        users = load_users()

        # Checks login information against our persistent database file
        if email in users:
            if users[email] == password:
                return redirect(url_for('dashboard', username=email))
            else:
                flash("Incorrect password. Please try again.", "error")
                return redirect(url_for('login'))
        else:
            flash("Student profile is not in the system.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')


# --- THE HOMEPAGE (DASHBOARD) ---
@app.route('/dashboard')
def dashboard():
    username = request.args.get('username', 'Guest')
    query = request.args.get('query', '').strip().lower()
    book_results = None
    error_message = None

    if query:
        if query in BOOK_INVENTORY:
            book_results = BOOK_INVENTORY[query]
            book_results['title'] = query.title()
        else:
            error_message = "Unfortunately, this book is not available. Please Try Again."

    return render_template('dashboard.html', username=username, book=book_results, error=error_message)


if __name__ == '__main__':
    app.run(debug=True)