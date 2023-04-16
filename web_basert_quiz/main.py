# Import required modules
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, current_user, login_required
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash
from user import User
from userReg import UserReg
from quizReg import QuizReg
from forms import LoginForm, QuestionForm, OptionForm, QuizForm

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
                return redirect(url_for('quiz_select'))
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
        return render_template('admin_quiz_select.html', the_title="Quiz select page", quiz_list=quiz_list, form=form)
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
            return redirect(url_for('update', quiz_id=quiz_id))
        elif quiz_tool == 'delete':
            return redirect(url_for('delete', quiz_id=quiz_id))
        else:
            return redirect(url_for('result_question', quiz_id=quiz_id))
    return render_template('admin_quiz_tool.html', the_title="Quiz Tool page", quiz_id=quiz_id, form=form)


@app.route('/quiz_add', methods=['GET', 'POST'])
@login_required
def quiz_add():
    if current_user.account_type != 'administrator':
        return redirect(url_for('index'))

    quiz_id = request.args.get('quiz_id')
    form = QuizForm()

    if request.method == 'POST' and form.validate_on_submit():
        title = request.form.get('title')
        with QuizReg() as db:
            db.addQuiz(title)
        return redirect(url_for('quiz_add', quiz_id=quiz_id))
    return render_template('admin_quiz_add.html', the_title='Create new quiz', form=form, quiz_id=quiz_id)


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

    if request.method == 'POST' and questionForm.validate_on_submit():
        idQuest = request.form.getlist('idQuest')
        question_text = request.form.getlist('question_text')
        category = request.form.getlist('category')
        quest_id = request.form.getlist('quest_id')
        idOpt = request.form.getlist('idOpt')
        option_text = request.form.getlist('option_text')
        is_correct = request.form.getlist('is_correct')
        data = {}

        for i in range(len(idQuest)):
            question_id = idQuest[i]
            if question_id not in data:
                data[question_id] = {
                    'quiz_id': quiz_id,
                    'question_text': question_text[i],
                    'category': category[i],
                    'options': []
                }
            option = {
                'idOpt': idOpt[i],
                'option_text': option_text[i],
                'is_correct': int(idOpt[i] in is_correct)
            }
            data[question_id]['options'].append(option)

        with QuizReg() as db:

            for question_id, question_data in data.items():
                db.updateQuestion(
                    question_id=question_id,
                    quiz_id=question_data['quiz_id'],
                    question_text=question_data['question_text'],
                    category=question_data['category']
                )
                for option_data in question_data['options']:
                    db.updateOption(
                        option_id=option_data['idOpt'],
                        quest_id=question_id,
                        option_text=option_data['option_text'],
                        is_correct=option_data['is_correct']
                    )
        return redirect(url_for('update', quiz_id=quiz_id))
    return render_template('admin_quiz.html', the_title='Quiz update', questions=questions, options=options, questionForm=questionForm, optionForm=optionForm, quiz_id=quiz_id)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if current_user.account_type != 'administrator':
        return redirect(url_for('index'))

    quiz_id = request.args.get('quiz_id')
    form = QuestionForm()

    if request.method == 'POST' and form.validate_on_submit():
        question_text = request.form.get('question_text')
        category = request.form.get('category')
        total_options = request.form.get('total_options')
        with QuizReg() as db:
            db.addQuestion(quiz_id, question_text, category)

        return redirect(url_for('add_options', quiz_id=quiz_id, total_options=total_options))
    return render_template('admin_add.html', the_title='Add questions', form=form, quiz_id=quiz_id)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if current_user.account_type != 'administrator':
        return redirect(url_for(index))

    form = QuestionForm()
    quiz_id = request.args.get('quiz_id')
    with QuizReg() as db:
        questions = db.getQuestionAll(quiz_id)

    if request.method == 'POST':
        idQuest = request.form.get('idQuest')
        if quiz_id is None:
            return redirect(url_for('delete'))
        with QuizReg() as db:
            db.deleteQuestion(idQuest)
            questions = db.getQuestionAll(quiz_id)
    return render_template('admin_delete.html', the_title="Question delete page", questions=questions, form=form)


@app.route('/add_options', methods=['GET', 'POST'])
@login_required
def add_options():
    if current_user.account_type != 'administrator':
        return redirect(url_for('index'))

    quiz_id = request.args.get('quiz_id')
    total_options = request.args.get('total_options')
    form = OptionForm()
    with QuizReg() as db:
        quest_id = db.getLastQuestId()
        quest_id = quest_id[0]

    if request.method == 'POST' and form.validate_on_submit():
        option_text = request.form.getlist('option_text')
        is_correct = request.form.get('is_correct')
        with QuizReg() as db:
            for i in range(len(option_text)):
                if i == int(is_correct):
                    db.addOptions(quest_id, option_text[i], '1')
                else:
                    db.addOptions(quest_id, option_text[i], '0')
            return 'done'
    return render_template('admin_add_options.html', the_title='Add options', form=form, quiz_id=quiz_id, total_options=int(total_options), quest_id=quest_id)


@app.route('/result_question', methods=['GET', 'POST'])
@login_required
def result_question():
    if current_user.account_type != 'administrator':
        return redirect(url_for('index'))

    with QuizReg() as db:
        quiz_id = request.args.get('quiz_id')
        quiz = db.getQuizId(quiz_id)
        quiz_title = quiz[1]
        questions = db.getQuestionAll
        results = db.getResultsAll(quiz_id)
        user_answers = {}

    for result in results:
        with UserReg() as db:
            user = db.getId(result[1])
            username = user[1]
            idResult = result[0]

        with QuizReg() as db:
            user_answer = db.getUserAnswersAll(idResult)
            user_answers[idResult] = user_answer

    return render_template('admin_results.html', the_title=quiz_title, results=results, username=username, user_answers=user_answers)


# user sine ting

@app.route('/quiz_select', methods=['GET', 'POST'])
@login_required
def quiz_select():
    form = QuizForm()
    if request.method == 'POST':
        quiz_id = request.form.get('quiz_id')
        if quiz_id is None:
            return redirect(url_for('quiz_select'))
        return redirect(url_for('quiz', quiz_id=quiz_id))
    else:
        with QuizReg() as db:
            quiz_list = db.getAllQuiz()
    return render_template('quiz_home.html', the_title="Quiz page", quiz_list=quiz_list, form=form)


@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    if current_user.account_type != 'user':
        return redirect(url_for('index'))

    with QuizReg() as db:
        quiz_id = request.args.get('quiz_id')
        questions = db.getQuestionAll(quiz_id)
        questions_dict = {}

        if len(questions) < 1:
            return 'This quiz is not done'

        for i in range(len(questions)):
            idQuest = str(questions[i][0])
            if idQuest not in questions_dict:
                questions_dict[idQuest] = {
                    'question_text': questions[i][2],
                    'category': questions[i][3],
                    'options': []
                }
            options = db.getOptionsAll(idQuest)
            for j in range(len(options)):
                option = {
                    'idOpt': str(options[j][0]),
                    'quest_id': options[j][1],
                    'option_text': options[j][2],
                    'is_correct': options[j][3]
                }
                questions_dict[idQuest]['options'].append(option)
        first_question_id = list(questions_dict.keys())[0]
        session["questions"] = questions_dict
        session["options"] = {}
        session["score"] = 0
        for question in questions_dict:
            session["options"][question] = questions_dict[question]['options']
    return render_template('quiz.html', quiz_id=quiz_id, question=session["questions"][first_question_id]["question_text"], options=session["options"][first_question_id], question_number=first_question_id, form=QuestionForm())


@app.route('/do_quiz2', methods=['GET', 'POST'])
@login_required
def do_quiz():
    if current_user.account_type != 'user':
        return redirect(url_for('index'))

    quiz_id = request.args.get('quiz_id')
    questions = session['questions']
    options = session['options']
    current_question_number = int(request.form['question_number'])
    answers = request.form.getlist('answers')

    # Check the answer and update the score
    current_question = questions[str(current_question_number)]
    current_options = options[str(current_question_number)]

    for answer in answers:
        with QuizReg() as db:
            quest_id = current_options[int(answer)-1]['quest_id']
            idOpt = current_options[int(answer)-1]['idOpt']
            idUser = current_user.id
            db.addUserAnswer(quest_id, idOpt, idUser)

        if current_options[int(answer)-1]['is_correct']:
            session['score'] += 1

    # Move to the next question or end the quiz
    if current_question_number == len(questions):
        totalt = current_question_number
        with QuizReg() as db:
            db.addResult(int(current_user.id), quiz_id,
                         session['score'], totalt)
        return render_template('results.html', score=session['score'], totalt=totalt)

    next_question_number = current_question_number + 1
    next_question = questions[str(next_question_number)]

    return render_template('quiz.html',
                           quiz_id=quiz_id,
                           question_number=next_question_number,
                           question=next_question['question_text'],
                           options=options[str(next_question_number)],
                           form=QuestionForm())


# Define the logout route

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('index'))


# Define the app's main function
if __name__ == '__main__':
    app.run(debug=True)
