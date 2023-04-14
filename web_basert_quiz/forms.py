from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, HiddenField, BooleanField,validators,FieldList,FormField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    typeofuser = SelectField('Login as', choices=[('user', 'User'), ('administrator', 'Administrator')], validators=[DataRequired()])
    submit = SubmitField('Login')

class QuestionForm(FlaskForm):
    idQuest = HiddenField('idQuest')
    quiz_id = HiddenField('quiz_id')
    question_text = StringField('Question Text', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Update')

class OptionForm(FlaskForm):
    idOpt = HiddenField('idOpt')
    quest_id = HiddenField('quest_id')
    option_text = StringField('Option Text', validators=[DataRequired()])
    is_correct = BooleanField('is_correct')
    submit = SubmitField('Update')