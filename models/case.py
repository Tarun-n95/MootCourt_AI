import sqlite3

class Case:
    @staticmethod
    def save_case(user_id, filename, case_text):
        conn = sqlite3.connect('database/mootcourt.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO cases (user_id, filename, case_text) VALUES (?, ?, ?)', (user_id, filename, case_text))
        conn.commit()
        conn.close()

    @staticmethod
    def get_cases_by_user(user_id):
        conn = sqlite3.connect('database/mootcourt.db')
        cursor = conn.cursor()
        cursor.execute('SELECT filename FROM cases WHERE user_id = ?', (user_id,))
        cases = cursor.fetchall()
        conn.close()
        return cases
