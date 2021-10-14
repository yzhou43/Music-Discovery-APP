from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError

from models import *

# Check the login input
def check_login(form, field):

    password = field.data
    username = form.username.data

    # Check if the username is in the database
    user_data = User.query.filter_by(username=username).first()
    if user_data is None:
        raise ValidationError("Username or password is incorrect")
    # Check password in invalid
    elif password != user_data.password:
        raise ValidationError("Username or password is incorrect")


# Check if the username already exists
def check_username(form, field):
    username = field.data
    user_object = User.query.filter_by(username=username).first()
    if user_object:
        raise ValidationError("Username already exists! Please choose a different one.")


class SignupForm(FlaskForm):

    username = StringField(
        "username",
        validators=[InputRequired(), check_username],
    )
    password = PasswordField(
        "password",
        validators=[InputRequired()],
    )
    submit_button = SubmitField("Sign up")


class LoginForm(FlaskForm):

    username = StringField("username", validators=[InputRequired()])
    password = PasswordField(
        "password",
        validators=[InputRequired(), check_login],
    )
    submit_button = SubmitField("Login")
