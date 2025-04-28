from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

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

        # ❌ BAD: Vulnerable SQL (Direct injection without parentheses issues)
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


# Secure Login Route
@app.route('/login_secure', methods=['GET', 'POST'])
def login_secure():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # ✅ GOOD: Secure Query (Parameterized)
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return redirect(url_for('success'))
        else:
            error = 'Invalid credentials'
    return render_template('login_secure.html', error=error)

# Success Page
@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
