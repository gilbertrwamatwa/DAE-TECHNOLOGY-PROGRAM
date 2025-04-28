import sqlite3

def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Drop table if already exists (safe cleanup)
    c.execute('DROP TABLE IF EXISTS users')

    # Create new table
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Insert a test user
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('testuser', 'testpass'))

    conn.commit()
    conn.close()
    print("Database created successfully.")

if __name__ == '__main__':
    create_database()
