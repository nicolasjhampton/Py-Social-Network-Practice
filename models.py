""" Basic setup for a user database """

import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.bcrypt import check_password_hash
#Flask keeps external packages like flask-login under this ext extension
from flask.ext.login import UserMixin

from peewee import *

DATABASE = SqliteDatabase('social.db')

#Mixins are small functionality adders, so put them before the main inheritance class
class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = Charfield(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        #order_by is a tuple, so you need the trailing comma
        #The dash is indicating decending order
        order_by = ('-joined_at',)

    #Class method decorator to indicate a function that creates an instance of the class
    #This insures that we can do things like hash the password when we make a user
    #Circumvents the User.create() method (That wont hash the password)
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                is_admin = admin)
        except IntegrityError:
            raise ValueError("User already exists")


def initialize():
    """Called when the program starts if not called as an imported module."""
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
