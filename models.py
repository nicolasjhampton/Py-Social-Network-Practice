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
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        #order_by is a tuple, so you need the trailing comma
        #The dash is indicating decending order
        order_by = ('-joined_at',)

    def get_posts(self):
        """Get all the posts for the current user."""
        return Post.select().where (Post.user == self)

    def get_stream(self):
        """Eventually this will be like a newsfeed of
        our posts plus all posts of people we are friends with."""
        return Post.select().where(
            (Post.user == self)
        )

    #Class method decorator to indicate a function that creates an instance of the class
    #This insures that we can do things like hash the password when we make a user
    #Circumvents the User.create() method (That wont hash the password)
    @classmethod
    def create_user(cls, username, email, password, admin=False):
        """Secure user creation in the database"""
        try:
            cls.create(
                username = username,
                email = email,
                password = generate_password_hash(password),
                is_admin = True)
        except IntegrityError:
            raise ValueError("User already exists")

class Post(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    # rel_model points to the related Model
    # related_name is what the rel_model calls this model
    # These are required for foreign key creation
    user = ForeignKeyField(rel_model=User, related_name='posts')
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


def initialize():
    """Called when the program starts if not called as an imported module."""
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()
