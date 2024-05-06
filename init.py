import sqlite3
import bcrypt
import logging

logging.basicConfig(level=logging.INFO)

def sys_init():
    """Initialize the database and other necessary components."""
    try:
        with sqlite3.connect('library.db') as conn:
            cursor = conn.cursor()
            # Transaction begins automatically
            # Create User table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS User (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            ''')
            # Create LibraryItem table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS LibraryItem (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    author_artist TEXT,
                    item_type TEXT NOT NULL,
                    availability INTEGER DEFAULT 1
                )
            ''')
            # Create Checkout table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Checkout (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    item_id INTEGER,
                    checkout_date TEXT DEFAULT CURRENT_TIMESTAMP,
                    return_date TEXT,
                    FOREIGN KEY (user_id) REFERENCES User(id),
                    FOREIGN KEY (item_id) REFERENCES LibraryItem(id)
                )
            ''')

            # Add admin user to the database if not already present
            cursor.execute("SELECT * FROM User WHERE username=?", ('admin',))
            if not cursor.fetchone():  # Admin user not found
                # If admin user doesn't exist, create one with a default password 'admin123'
                password_hash = bcrypt.hashpw(b'admin123', bcrypt.gensalt())
                cursor.execute('''
                    INSERT INTO User (username, password_hash, role)
                    VALUES (?, ?, ?)
                ''', ('admin', password_hash.decode('utf-8'), 'Librarian'))
                conn.commit()  # Commit changes
                logging.info("Database initialized and admin user created.")
            else:
                logging.info("Database already initialized.")
    except Exception as e:
        logging.error(f"An error occurred while initializing the database: {e}")
        raise

# Call the sys_init function when the module is executed
if __name__ == "__main__":
    sys_init()
