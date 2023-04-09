# Import required modules
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from user import User
from userReg import UserReg

# Configure the app and login manager
app = Flask(__name__)
app.secret_key = 'mysecretkey'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the User Loader function for Flask-Login


@login_manager.user_loader
def load_user(username):
    with UserReg() as db:
        user_info = db.getUser(username)
    if user_info:
        user = User(*user_info)
        return user
    else:
        return None

# Define the index route


@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html', the_title="Login page")

# Define the login route


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        account_type = request.form['typeofuser']
        with UserReg() as db:
            user = db.getUser(username)
            passHash = user[2].strip("\'")
        if user and check_password_hash(passHash, password):
            user_obj = User(user[0], user[1], passHash, user[3])
            login_user(user_obj)
            session['account_type'] = user[3]
            if account_type == 'administrator' and user[3] == 'administrator':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('quiz'))
        flash('Invalid username or password')
    return render_template('login.html', the_title="Login page")


@app.route('/admin')
@login_required
def admin():
    if current_user.account_type == 'administrator':
        return render_template('home.html', the_title="Home page")
    else:
        return redirect(url_for('index'))


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Evaluate quiz and show results
        questions = Question.query.all()
        score = 0
        total = 0
        for question in questions:
            total += 1
            selected_options = request.form.getlist(str(question.id))
            selected_answer = ','.join(selected_options)
            if selected_answer == question.answer:
                score += 1
        return render_template('results.html', the_title="Results page", score=score, total=total)
    else:
        # Show quiz questions
        questions = Question.query.all()
        return render_template('quiz.html', the_title="Quiz page", questions=questions)

# Define the logout route


@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))


# Define the app's main function
if __name__ == '__main__':
    app.run(debug=True)
