from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    typeofuser = SelectField('Login as', choices=[('user', 'User'), ('administrator', 'Administrator')], validators=[DataRequired()])
    submit = SubmitField('Login')

class QuestionForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], choices=[('Geography', 'Geography'), ('History', 'History'), ('Science', 'Science'), ('Mathematics', 'Mathematics')])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    answer = SelectField('Answer', validators=[DataRequired()], choices=[('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3'), ('option4', 'Option 4')])
