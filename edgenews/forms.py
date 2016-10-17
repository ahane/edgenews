from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import DataRequired

class SignupForm(Form):
    name = TextField('name', validators=[DataRequired()])
    email = TextField('email', validators=[DataRequired()])
    plain_password = PasswordField('plain_password', validators=[DataRequired()])

class LoginForm(Form):
    name = TextField('name', validators=[DataRequired()])
    plain_password = PasswordField('plain_password', validators=[DataRequired()])
