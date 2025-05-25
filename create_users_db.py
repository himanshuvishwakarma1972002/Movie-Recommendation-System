import sqlite3

# Create database and users table
conn = sqlite3.connect('users.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("✅ Database and users table created!")
