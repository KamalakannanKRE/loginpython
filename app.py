from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Used for session management, generate a secret key

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'  # This should match the service name in your Docker Compose
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Database@123'
app.config['MYSQL_DB'] = 'mydatabase'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Return results as dictionaries

mysql = MySQL(app)

# Sample user data in memory for demonstration
users = {}



@app.route('/')
def home():
    return 'Welcome to the Flask Registration and Login App with MySQL!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists in the database
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM userkamal WHERE username=%s', (username,))
        existing_user = cursor.fetchone()
        cursor.close()

        if existing_user:
            flash('Username already taken. Choose another one.', 'error')
        else:
            # Insert the new user into the database
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO userkamal (username, password) VALUES (%s, %s)', (username, password))
            mysql.connection.commit()
            cursor.close()

            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match a user in the database
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM userkamal WHERE username=%s AND password=%s', (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login failed. Check your username and password.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
