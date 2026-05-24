# 1. Login Authentication Flow
def handle_login(username, password):
    if not username or not password:
        return "Display: Small re-enter details note"  # From your Flowchart Page 2

    user = database.query_user(username)
    if not user or user.password != password:
        return "Dialog: Student is not in System"  # From your Flowchart Page 3

    # If Authorized
    return {
        "status": "Authorized",
        "redirect": "SmartLib Home page",
        "username": user.username
    }


# 2. Book Query Flow
def handle_book_search(search_query, filter_settings=None):
    book = database.query_book(search_query)

    if not book:
        return "Unfortunately, this book is not available. Please Try Again."  # From your Flowchart Page 4

    if filter_settings and not book.matches(filter_settings):
        return "Proceed to alternate filter handling / Re-try"  # From your Flowchart Page 4

    # Fetch structural availability
    return {
        "title": book.title,
        "room": book.room_location,
        "capacity": book.room_capacity,
        "status": "Available" if book.is_accessible else "Unavailable"  # From Page 5
    }