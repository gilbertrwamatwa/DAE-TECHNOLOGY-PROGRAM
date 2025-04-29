from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import re
import bcrypt


app = Flask(__name__)

# ✅ Input validation: basic pattern check and length limit
def is_valid_input(value):
    # Disallow SQL control characters, limit to 50 chars, no spaces or semicolons
    if len(value) > 50:
        return False
    if re.search(r"[;'\"]|--|\s", value):  # checks for SQLi characters
        return False
    return True

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Insecure Login Route
@app.route('/login_insecure', methods=['GET', 'POST'])
def login_insecure():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()

        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        print(f"Executing Query: {query}")
        
        cursor.execute(query)
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for('success'))
        else:
            error = 'Invalid credentials'
    return render_template('login_insecure.html', error=error)

# ✅ Secure Login Route
@app.route('/login_secure', methods=['GET', 'POST'])
def login_secure():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not is_valid_input(username) or not is_valid_input(password):
            error = "Invalid input format."
        else:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()

                # ✅ Only fetch hashed password for given username
                cursor.execute("SELECT * FROM users WHERE username=?", (username,))
                user = cursor.fetchone()
                conn.close()

                if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                    return redirect(url_for('success'))
                else:
                    error = "Invalid credentials"
            except Exception:
                error = "Something went wrong. Please try again."
    return render_template('login_secure.html', error=error)

# Success Page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
