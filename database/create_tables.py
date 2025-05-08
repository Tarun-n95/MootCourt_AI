import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('mootcourt.db')  

# Create a cursor object to execute SQL
cursor = conn.cursor()

# SQL command to create users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Save changes
conn.commit()

# Close connection
conn.close()

print("Database and table created.")