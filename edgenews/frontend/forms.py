from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    name = TextField('name', validators=[DataRequired()])
    email = TextField('email', validators=[DataRequired()])
    plain_password = PasswordField('plain_password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    name = TextField('name', validators=[DataRequired()])
    plain_password = PasswordField('plain_password', validators=[DataRequired()])
