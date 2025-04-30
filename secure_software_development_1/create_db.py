import sqlite3
import bcrypt

def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Drop table if already exists
    c.execute('DROP TABLE IF EXISTS users')

    # Create new users table
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # ✅ Hash password before storing (for secure login demo)
    plain_password = 'testpass'
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())

    # ✅ Store hashed password
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('testuser', hashed_password))

    # ❌ Store plain-text password for INSECURE DEMO ONLY
    c.execute('INSERT OR REPLACE INTO users (username, password) VALUES (?, ?)', ('insecure_user', 'insecure_pass'))


    conn.commit()
    conn.close()
    print("Database created with hashed password.")

if __name__ == '__main__':
    create_database()