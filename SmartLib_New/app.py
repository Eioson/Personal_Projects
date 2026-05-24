from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'smartlib_secret_key'  # Required for flashing error messages

# Mock Database matching your flowcharts
STUDENT_DATABASE = {
    "solomon": "password123",
    "edison": "pass456",
    "kevin": "pass789"
}

BOOK_INVENTORY = {
    "lajan littera": {"room": "Room 1", "capacity": 15, "available": True},
    "data structures": {"room": "Room 2", "capacity": 30, "available": False}
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password')

        # Flowchart Page 2: Check if inputs are empty
        if not username or not password:
            flash("Please fill out all details.", "error")
            return redirect(url_for('login'))

        # Flowchart Page 3: Is the user in the system?
        if username in STUDENT_DATABASE:
            if STUDENT_DATABASE[username] == password:
                # Authorized! Transfer to dashboard with username
                return redirect(url_for('dashboard', username=username))
            else:
                flash("Incorrect password. Please try again.", "error")
                return redirect(url_for('login'))
        else:
            # "Student is not in System" Dialog
            flash("Student is not in System.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username', 'Guest')
    query = request.args.get('query', '').strip().lower()
    book_results = None
    error_message = None

    # Flowchart Page 4 & 5: Find book option
    if query:
        if query in BOOK_INVENTORY:
            book_results = BOOK_INVENTORY[query]
            book_results['title'] = query.title()
        else:
            # Book not available fallback
            error_message = "Unfortunately, this book is not available. Please Try Again."

    return render_template('dashboard.html', username=username, book=book_results, error=error_message)

if __name__ == '__main__':
    # debug=True automatically reloads the app when you save changes
    app.run(debug=True)