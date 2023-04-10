# Import required modules
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from user import User
from userReg import UserReg
from forms import LoginForm

# Configure the app and login manager
app = Flask(__name__)
app.secret_key = 'mysecretkey'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the User Loader function for Flask-Login


@login_manager.user_loader
def load_user(id):
    with UserReg() as db:
        user = db.getId(id)
    if user:
        return User(*user[:4])
    return None

# Define the index route


@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('login'))

# Define the login route


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        account_type = form.typeofuser.data
        with UserReg() as db:
            user = db.getUser(username)
            passHash = user[2].strip("'")
        if user and check_password_hash(passHash, password) and account_type == user[3]:
            user = User(*user[:4])
            login_user(user)
            if current_user.account_type == 'administrator':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('quiz'))
        flash('Invalid username or password')
    return render_template('login.html', the_title='Login page', form=form)


@app.route('/admin')
@login_required
def admin():
    print("Admin page accessed!")
    return render_template('home.html', the_title="Home page")


@app.route('/quiz', methods=['GET', 'POST'])
@login_required
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
