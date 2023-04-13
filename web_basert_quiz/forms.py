from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    typeofuser = SelectField('Login as', choices=[('user', 'User'), ('administrator', 'Administrator')], validators=[DataRequired()])
    submit = SubmitField('Login')

class QuestionForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    category = SelectField('Login as', choices=[('math', 'Math'), ('science', 'Science'), ('music','Music'), ('others', 'Others')], validators=[DataRequired()])
    submit = SubmitField('Edit question')
    