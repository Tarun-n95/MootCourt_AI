import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def create_user(username, email, password):
        hashed_password = generate_password_hash(password)
        conn = sqlite3.connect('database/mootcourt.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                        (username, email, hashed_password))
        conn.commit()
        conn.close()
        
    @staticmethod
    def find_by_email(email):
        conn = sqlite3.connect('database/mootcourt.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        return user