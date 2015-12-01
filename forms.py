from flask-wtf import Form

#Flask-WTF uses wtforms behind the scenes for the actual form, field, and widget creation.
from wtforms import PasswordField
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import Regexp
from wtforms.validators import ValidationError

from models import User


def name_exists(form, field):
    """Tests a new username to see if it already exists in the database"""
    if user.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')

def email_exists(form, field):
    """Tests a new email to see if it already exists in the database"""
    if user.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')

class RegisterForm(Form):
    """Class for Regsitration form validation"""
    username = StringField(
        'Username', # First argument is the label
        validators = [  # Second argument is an array of validators
            DataRequired(),     # Built in to wtf
            Regexp(     # Defines a regex pattern as a validator
                r'^[a-zA-Z0-9_]+$',
                message = ("Username should be one word, letters, "
                           "numbers and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators = [
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PaswordField(
        'Password',
        validators = [
            DataRequired(),
            Length(min=6),
            EqualTo('password2', message='Passwords must match') # Note it refers to the variable name, not the label
        ])
    password2 = PaswordField(
        'Confirm Password',
        validators = [
            DataRequired()
        ])
