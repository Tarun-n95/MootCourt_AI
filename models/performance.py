import sqlite3

class Performance:
    @staticmethod
    def save_performance(user_id, opponent_name, score, result, transcription=None, feedback=None):
        conn = sqlite3.connect('database/mootcourt.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO performance (user_id, opponent_name, score, result, transcription, feedback)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, opponent_name, score, result, transcription, feedback))
        conn.commit()
        conn.close()

    @staticmethod
    def get_performance_by_user(user_id):
        conn = sqlite3.connect('database/mootcourt.db')
        cursor = conn.cursor()
        cursor.execute('SELECT opponent_name, score, result, timestamp, transcription, feedback FROM performance WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
        data = cursor.fetchall()
        conn.close()
        return data
    
    @staticmethod
    def get_challenge_count_by_user(user_id):
        conn = sqlite3.connect('database/mootcourt.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM performance WHERE user_id = ? AND result = "Oral Answer"', (user_id,))
        count = cursor.fetchone()[0]
        conn.close()
        return count