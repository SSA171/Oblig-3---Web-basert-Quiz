from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    typeofuser = SelectField('Login as', choices=[(
        'user', 'User'), ('administrator', 'Administrator')], validators=[DataRequired()])
    submit = SubmitField('Login')
