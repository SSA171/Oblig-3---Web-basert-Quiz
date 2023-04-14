# Import required modules
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, login_required
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash
from user import User
from userReg import UserReg
from quizReg import QuizReg
from forms import LoginForm, QuestionForm, OptionForm

# Configure the app and login manager
app = Flask(__name__)
app.secret_key = 'mysecretkey'
csrf = CSRFProtect(app)
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
        form = QuestionForm()
        if request.method == 'POST':
            quiz_id = request.form.get('quiz_id')
            if quiz_id is None:
                return redirect(url_for('admin'))
            return redirect(url_for('admin_tool', quiz_id=quiz_id))
        
        with QuizReg() as db:
            quiz_list = db.getAllQuiz()
        return render_template('admin_quiz_select.html', the_title="Quiz select page", quiz_list=quiz_list,form=form)
    return redirect(url_for(index))

@app.route('/admin/tool', methods=['GET', 'POST'])
@login_required
def admin_tool():
    if current_user.account_type != 'administrator':
        return redirect(url_for(index))
    
    quiz_id = request.args.get('quiz_id')
    form = QuestionForm()
    if request.method == 'POST':
        quiz_tool = request.form.get('quiz_tool')
        if quiz_tool is None:
            return redirect(url_for('admin_tool', quiz_id=quiz_id))
        elif quiz_tool == 'edit':
            return redirect(url_for('update', quiz_id=quiz_id, ))
        else:
            return redirect(url_for('result_quiz', quiz_id=quiz_id))
    return render_template('admin_quiz_tool.html', the_title="Quiz Tool page", quiz_id = quiz_id, form = form)

@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if current_user.account_type != 'administrator':
        return redirect(url_for('index'))

    quiz_id = request.args.get('quiz_id')
    questionForm = QuestionForm()
    optionForm = OptionForm()
    with QuizReg() as db:
        questions = db.getQuestionAll(quiz_id)
        options = {}
        for question in questions:
            idQuest = question[0]
            options[idQuest] = db.getOptionsAll(idQuest)

    if request.method == 'POST':
        question_changes = []
        option_changes = []
        for question in questions:
            question_id = request.form.get(f"idQuest_{question[0]}")
            question_text = request.form.get(f"question_text_{question[0]}")
            category = request.form.get(f"category_{question[0]}")
            if question_text != question[2] or category != question[3]:
                question_changes.append((question_id, question[2], question_text, question[3], category))
                #db.updateQuestion(question_id, question_text, category)
            for option in options[question[0]]:
                option_id = option[0]
                option_text = request.form.get(f"option_text_{option_id}")
                is_correct = request.form.get(f"is_correct_{option_id}")
                if option_text != option[2] or is_correct != option[3]:
                    option_changes.append((option_id, option[2], option_text, option[3], is_correct))
                    #db.updateOption(option_id, option_text, is_correct)

        print(f"Question changes: {question_changes}")
        print(f"Option changes: {option_changes}")

    return render_template('admin_quiz.html', the_title='Quiz update', questions=questions, options=options, questionForm=questionForm, optionForm=optionForm, quiz_id=quiz_id)




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