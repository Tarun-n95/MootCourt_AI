import sqlite3

conn = sqlite3.connect('mootcourt.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    filename TEXT NOT NULL,
    case_text TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

conn.commit()
conn.close()

print("Cases table created.")