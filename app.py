import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from create_db import LibraryItem
from user_manage import login as user_login, User, all_users, add_user
from init import sys_init

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role FROM User WHERE id=?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                user_id, username, role = user_data
                return User(user_id, username, role)
    except Exception as e:
        print(f"Error during user loading: {e}")
    return None
# Route for the home page
@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.role == 'Librarian':
        return redirect(url_for('librarian_dashboard'))
    elif current_user.role == 'Patron':
        return redirect(url_for('patron_dashboard'))
    return render_template('index.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = user_login(username, password)
        if user:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

# Route for user logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Dashboard for librarians
@app.route('/librarian_dashboard')
@login_required
def librarian_dashboard():
    if current_user.role != 'Librarian':
        flash("Access denied: Only librarians can access this page.")
        return redirect(url_for('home'))
    return render_template('librarian_dashboard.html')

# Dashboard for patrons
@app.route('/patron_dashboard')
@login_required
def patron_dashboard():
    if current_user.role != 'Patron':
        flash("Access denied: Only patrons can access this page.")
        return redirect(url_for('home'))
    return render_template('patron_dashboard.html')

# Route to add a librarian
@app.route('/add_librarian', methods=['GET', 'POST'])
@login_required
def add_librarian():
    if current_user.role != 'Librarian':
        flash("Access denied: Only librarians can add other librarians.")
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'Librarian'
        if add_user(username, password, role):
            flash('Librarian added successfully!')
            return redirect(url_for('librarian_dashboard'))
        else:
            flash('Failed to add librarian.')
    return render_template('add_librarian.html')

# Route to add a patron
@app.route('/add_patron', methods=['GET', 'POST'])
@login_required
def add_patron():
    if current_user.role != 'Librarian':
        flash("Access denied: Only librarians can add patrons.")
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'Patron'
        if add_user(username, password, role):
            flash('Patron added successfully!')
            return redirect(url_for('librarian_dashboard'))
        else:
            flash('Failed to add patron.')
    return render_template('add_patron.html')

# Routes for handling library items and users
@app.route('/search_items')
@login_required
def search_items():
    # Add logic to fetch items based on a search query
    return render_template('search_items.html')
@app.route('/search_results')
@login_required
def search_results():
    query = request.args.get('search_query', '')
    if query:
        items = LibraryItem.query.filter(LibraryItem.title.ilike(f'%{query}%')).all()
    else:
        items = []
    return render_template('search_results.html', items=items, query=query)


@app.route('/add_library_item', methods=['GET', 'POST'])
@login_required
def add_library_item():
    if current_user.role != 'Librarian':
        flash("Access denied: Only librarians can add library items.")
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form.get('title')
        author_artist = request.form.get('author_artist')
        item_type = request.form.get('item_type')
        availability = request.form.get('availability', type=int)

        try:
            new_item = LibraryItem(title=title, author_artist=author_artist, item_type=item_type, availability=availability)
            db.session.add(new_item)
            db.session.commit()
            flash('Library item added successfully!')
            return redirect(url_for('add_library_item'))
        except Exception as e:
            db.session.rollback()
            flash(f'Failed to add library item: {str(e)}')
            print(f'Error: {str(e)}')  # For debugging

    return render_template('add_library_item.html')


@app.route('/display_users')
@login_required
def display_users():
    # Fetch all users and display
    users = all_users()
    return render_template('display_users.html', users=users)

@app.route('/search_user_by_id', methods=['GET', 'POST'])
@login_required
def search_user_by_id():
    # Logic to search for a user by ID and display
    if request.method == 'POST':
        user_id = request.form['user_id']
        # Search logic here...
        flash('User found!')
        return redirect(url_for('search_user_by_id'))
    return render_template('search_user_by_id.html')

@app.route('/display_user_checkout_items')
@login_required
def display_user_checkout_items():
    # Logic to display items checked out by a user
    return render_template('display_user_checkout_items.html')

@app.route('/users')
@login_required
def users():
    return render_template('users.html')

@app.route('/usersajax')
@login_required
def usersajax():
    return render_template('usersajax.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
