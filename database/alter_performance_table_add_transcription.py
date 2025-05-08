import sqlite3

conn = sqlite3.connect('mootcourt.db')
cursor = conn.cursor()

cursor.execute('''
ALTER TABLE performance
ADD COLUMN transcription TEXT
''')

cursor.execute('''
ALTER TABLE performance
ADD COLUMN feedback TEXT
''')

conn.commit()
conn.close()

print("Performance table altered: transcription and feedback columns added.")