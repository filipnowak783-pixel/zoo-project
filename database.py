import sqlite3

# connects to the database (creates it if it doesnt exist)
def get_db():
    conn = sqlite3.connect('zoo.db')
    conn.row_factory = sqlite3.Row  # so we can access columns by name
    return conn


# run this once to create all the tables
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # zoo bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zoo_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            visit_date TEXT NOT NULL,
            adults INTEGER NOT NULL,
            children INTEGER NOT NULL,
            addon TEXT,
            notes TEXT,
            total REAL NOT NULL,
            booking_ref TEXT NOT NULL
        )
    ''')

    # hotel bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hotel_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            guest_name TEXT NOT NULL,
            guest_email TEXT NOT NULL,
            hotel_name TEXT NOT NULL,
            room_type TEXT NOT NULL,
            checkin_date TEXT NOT NULL,
            checkout_date TEXT NOT NULL,
            guests INTEGER NOT NULL,
            total REAL NOT NULL,
            booking_ref TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Database created!")
