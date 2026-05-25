from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'smartlib_secret_key'


# 1. The root URL now automatically loads the Dashboard in Guest Mode
@app.route('/')
@app.route('/dashboard')
def dashboard():
    # If no username/role are passed, default to a Guest session
    username = request.args.get('username', 'Guest User')
    role = request.args.get('role', 'guest')
    query = request.args.get('query', '').strip().lower()

    BOOK_INVENTORY = {
        "lajan littera": {"room": "Room 1", "capacity": 15, "available": True},
        "data structures": {"room": "Room 2", "capacity": 30, "available": False}
    }

    book_results = None
    error_message = None

    if query:
        if query in BOOK_INVENTORY:
            book_results = BOOK_INVENTORY[query]
            book_results['title'] = query.title()
        else:
            error_message = "Unfortunately, this book is not available. Please Try Again."

    return render_template('dashboard.html', username=username, role=role, book=book_results, error=error_message)


# 2. Move your actual Login/Sign-In page handling here
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Your existing login validation logic here...
        # If successful, redirect to dashboard with the proper role:
        # return redirect(url_for('dashboard', username=user['username'], role=user['role']))
        pass
    return render_template('login.html')  # Assuming Solomon's login page is named login.html


@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)