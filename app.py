from flask import Flask

from flask import flash
#g is a global object we can attach things to for global access between views and modules
from flask import g
from flask import redirect
from flask import render_template
from flask import url_for
#LoginManager - An appliance to handle user authentication.
from flask.ext.login import LoginManager

import forms
import models

#server variables
DEBUG = True
PORT = 8080
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'nbUTWE9yhr/xDLosbxcInOLIabzaypvmdHyhITw5odIHmrduQeh2G'

#login manager setup
login_manager = LoginManager()  #creates instance of the manager
login_manager.init_app(app)     #setup of manager for our app (passing the app to the manager)
login_manager.login_view = 'login'      #name of the view we redirect people not logged in yet. Manager does this automatically

#user_loader - A decorator to mark the function responsible for loading a user from whatever data source we use.
@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)    #getting the User with an id equal to this Userid
    except models.DoesNotExist:     #This is a peewee exception
        return None

# before_request - A decorator to mark a function as running before the request hits a view.
@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()

#after_request - A decorator to mark a function as running before the response is returned.
@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    return response

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()     #This grabs our form info from the POST and puts it into an instance of the class
    if form.validate_on_submit():   #this will run our validation tests on the form info
        flash("Yay, you registered!", "success")
        models.User.create_user(    #If the data is validated, we'll add it to the database
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        return redirect(url_for('index'))   #With the user added, we'll redirect to the index page
    return render_template('register.html', form=form)     #If the data doesn't validate, we redirect back to the register page

@app.route('/')
def index():
    return 'Hey'

#This runs the app if this isn't an imported module of another script
if __name__ == '__main__':
    #Creates our database
    models.initialize()
    try:
        #creates a superuser account for us if it doesn't already exist
        models.User.create_user(
            username='nicolasHampton',
            email='email@email.com',
            password='openSesame',
            admin=True)
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
