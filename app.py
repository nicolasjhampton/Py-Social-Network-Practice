from flask import Flask
#g is a global object we can attach things to for global access between views and modules
from flask import g

import models

DEBUG = True
PORT = 8080
HOST = '127.0.0.1'

app = Flask(__name__)

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


#This runs the app if this isn't an imported module of another script
if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
