# Import required modules
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from user import User
from userReg import UserReg
from quizReg import QuizReg
from forms import LoginForm, QuestionForm

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

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.account_type == 'administrator':
        if request.method == 'POST':
            quiz_id = request.form.get('quiz_id')
            if quiz_id is None:
                return redirect(url_for('admin'))
            return redirect(url_for('admin_tool', quiz_id=quiz_id))
        
        with QuizReg() as db:
            quiz_list = db.getAllQuiz()
        return render_template('admin_quiz_select.html', the_title="Quiz select page", quiz_list=quiz_list)
    return redirect(url_for(index))

@app.route('/admin/tool', methods=['GET', 'POST'])
@login_required
def admin_tool():
    if current_user.account_type != 'administrator':
        return redirect(url_for(index))
    
    quiz_id = request.args.get('quiz_id')
    if request.method == 'POST':
        quiz_tool = request.form.get('quiz_tool')
        if quiz_tool is None:
            return redirect(url_for('admin_tool', quiz_id=quiz_id))
        elif quiz_tool == 'edit':
            return redirect(url_for('edit_question', quiz_id=quiz_id))
        else:
            return redirect(url_for('result_quiz', quiz_id=quiz_id))
    return render_template('admin_quiz_tool.html', the_title="Quiz Tool page", quiz_id = quiz_id)

@app.route('/edit_question', methods=['GET', 'POST'])
@login_required
def edit_question():
    if current_user.account_type != 'administrator':
        return redirect(url_for('index'))

    quiz_id = request.args.get('quiz_id')
    form = QuestionForm()
    with QuizReg() as db:
        questions = db.getQuestionAll(quiz_id)
    if request.method == 'POST':
        for question in questions:
            question_id = question[0]
            question_text = request.form.get(f'question{question_id}')
            idQuest = question_id
    return render_template('quiz_editor.html', questions=questions, form=form, quiz_id=quiz_id)

@app.route('/edit_options', methods=['GET', 'POST'])
@login_required
def edit_options():
    if current_user.account_type != 'administrator':
        return redirect(url_for('index'))

    idQuest = request.args.get('idQuest')
    with QuizReg() as db:
        options = db.getOptionsAll(idQuest)
        print(options)
    return render_template('option_editor.html', options=options, idQuest = idQuest)


@app.route('/create_question', methods=['GET', 'POST'])
@login_required
def create_question():
    if current_user.account_type != 'administrator':
        return redirect(url_for('quiz'))

    if request.method == 'POST':
        # Get data from form
        quiz_id = request.form['quiz_id']
        category = request.form['category']
        question_text = request.form['question_text']
        option1 = request.form['option1']
        option2 = request.form['option2']
        option3 = request.form['option3']
        option4 = request.form['option4']
        correct_option = request.form['correct_option']

        # Insert question into database
        with QuizReg() as db:
            db.createQuestion(quiz_id, category, question_text)
            question_id = db.getLastQuestionId()
            db.createOption(question_id, option1)
            db.createOption(question_id, option2)
            db.createOption(question_id, option3)
            db.createOption(question_id, option4)
            db.setCorrectOption(question_id, correct_option)

        flash('Question created successfully.')
        return redirect(url_for('create_question'))

    else:
        with QuizReg() as db:
            quiz_list = db.getAllQuiz()

        return render_template('create_question.html', the_title = 'Create Question', quiz_list = quiz_list)


@app.route('/result_question', methods=['GET','POST'])
@login_required
def result_question():
    if current_user.account_type != 'administrator':
        return redirect(url_for('index'))
    
    with QuizReg() as db:
        quiz_id = request.args.get('quiz_id')
        quiz = db.getQuizId(quiz_id)
        quiz_title = quiz[1]
        results = db.getResultsAll(quiz_id)
        
    for result in results:
        with UserReg() as db:
            user = db.getId(result[1])
            username = user[1]
    return render_template('admin_results.html', the_title=quiz_title, results = results, username = username)
    


@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')
        if quiz_id is None:
            return redirect(url_for('quiz'))
        return redirect(url_for('do_quiz', quiz_id=quiz_id))
    else:
        with QuizReg() as db:
            quiz_list = db.getAllQuiz()
    return render_template('quiz_home.html', the_title="Quiz page", quiz_list=quiz_list)


@app.route('/doquiz', methods=['GET', 'POST'])
@login_required
def do_quiz():
    if request.method == 'POST':
        quiz_id = request.args.get('quiz_id')
        totalt = request.args.get('totalt')
        # Evaluate quiz and show results
        user_answers = request.form.to_dict()
        score = 0
        
        for key in user_answers:
            idOpt = user_answers[key]
            with QuizReg() as db:
                answer = db.getOptId(idOpt)
            if answer[3] == 1:
                score += 1
        return render_template('results.html', score=score, totalt=totalt)
    
    else:
        # Show quiz questions
        with QuizReg() as db:
            quiz_id = request.args.get('quiz_id')
            questions = db.getQuestionAll(quiz_id)
            quiz_title = db.getQuizId(quiz_id)
            options = {}
            totalt = 0
            for question in questions:
                options[question[0]] = db.getOptionsAll(question[0])
                totalt += 1
        return render_template('quiz.html', the_title=quiz_title[1], quiz_id=quiz_id, questions=questions, options=options, totalt=totalt)
    

# Define the logout route

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))


# Define the app's main function
if __name__ == '__main__':
    app.run(debug=True)