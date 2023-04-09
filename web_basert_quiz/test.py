from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# MySQL database connection
db = mysql.connector.connect(
    host='localhost',
    user='your_username',
    password='your_password',
    database='your_database_name'
)

# Quiz editor page accessible only to admins
@app.route('/quiz_editor')
def quiz_editor():
    if 'username' in session and session['user_type'] == 'admin':
        return render_template('quiz_editor.html')
    else:
        return redirect('/')

# Quiz page accessible to all users
@app.route('/quiz')
def quiz():
    if 'username' in session:
        return render_template('quiz.html')
    else:
        return redirect('/')

# Login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the database to check the user credentials
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        if user:
            # Set session variables upon successful login
            session['username'] = user[1]
            session['user_type'] = user[3]
            if user[3] == 'admin':
                return redirect('/quiz_editor')
            else:
                return redirect('/quiz')
        else:
            # Display an error message if the user credentials are invalid
            error_message = "Invalid username or password. Please try again."
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
