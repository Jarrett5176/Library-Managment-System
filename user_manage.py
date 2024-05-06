import sqlite3
import bcrypt
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = user_id
        self.username = username
        self.role = role

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        # Assuming the user ID is stored as an int convert it to string as Flask-Login expects
        return str(self.id)

def login(username, password):
    """Authenticate user and return user object if successful, otherwise return None."""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash, role FROM User WHERE username=?", (username,))
            user_data = cursor.fetchone()
            if user_data:
                user_id, _, password_hash, role = user_data
                # Convert the password_hash from string to bytes
                password_hash_bytes = password_hash.encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), password_hash_bytes):
                    return User(user_id, username, role)
    except Exception as e:
        print(f"Error during login: {e}")
    return None


def add_user(username, password, role):
    """Generic function to add users (librarians/patrons) to the database."""
    try:
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO User (username, password_hash, role) VALUES (?, ?, ?)",
                           (username, password_hash.decode('utf-8'), role))
            conn.commit()
    except Exception as e:
        print(f"Error adding user: {e}")

def all_users():
    """Retrieve all users from the database."""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, role FROM User")
            return [User(user_id, username, role) for user_id, username, role in cursor.fetchall()]
    except Exception as e:
        print(f"Error retrieving users: {e}")
        return []

# Usage of add_user function for different roles
def add_librarian(username, password):
    add_user(username, password, 'Librarian')

def add_patron(username, password):
    add_user(username, password, 'Patron')
