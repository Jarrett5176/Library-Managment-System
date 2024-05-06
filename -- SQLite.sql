-- Create User table
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS LibraryItem (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author_artist TEXT,
    item_type TEXT NOT NULL CHECK (item_type IN ('Book', 'CD', 'DVD')),
    availability INTEGER DEFAULT 1 CHECK (availability IN (0, 1))
);

-- Create Checkout table
CREATE TABLE IF NOT EXISTS Checkout (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    item_id INTEGER,
    checkout_date TEXT DEFAULT CURRENT_TIMESTAMP,
    return_date TEXT,
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (item_id) REFERENCES LibraryItem(id)
);

-- Create the LibraryItem table
CREATE TABLE IF NOT EXISTS LibraryItem (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_artist TEXT,
    item_type TEXT NOT NULL,
    availability INTEGER DEFAULT 1
);

