from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Define the users dictionary with username/password pairs
users = {'user': {'password': '123', 'role': 'user'},
         'admin': {'password': '123', 'role': 'administrator'}}

# Check if the user is authenticated on every request
@app.before_request
def require_login():
    allowed_routes = ['login', 'logout']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))

# Render the login form
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
       
        username = request.form['username']
        password = request.form['password']
        account_type = request.form['typeofuser']
        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['account_type'] = account_type
            if account_type == 'administrator':
                return render_template('home.html', the_title="Home page")
            else:
                return render_template('quiz.html', the_title="Quiz page")
        else:
            flash('Invalid username or password')
    return render_template('login.html', the_title="Login page")

if __name__ == "__main__":
    app.run()
