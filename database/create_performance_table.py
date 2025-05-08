import sqlite3

conn = sqlite3.connect('mootcourt.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE performance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    opponent_name TEXT,
    score INTEGER NOT NULL,
    result TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

conn.commit()
conn.close()

print("Performance table created.")