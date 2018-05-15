from flask import Flask, redirect, url_for, session, request, render_template, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined, Template

from model import *

import json, os, random

from datetime import datetime
from functools import wraps
from pprint import pprint


SECRET_KEY = 'development key'
DEBUG = True

app = Flask(__name__)
app.debug = DEBUG
app.secret_key = SECRET_KEY

app.jinja_env.undefined = StrictUndefined


# I added the following config otherwise, everytime the redirect was giving warning
# Dont put this in app.config in model.py (db connect) because that has sql alchemy related params only
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
 
# Using login-decorator - for login authentication
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def welcome():
    """Homepage."""
    
    if 'logged_in' in session:
        return redirect('/view-application')

    return render_template("home.html")


# This is an ajax route/end-point
@app.route('/register', methods=["POST"])
def handle_registration_form():
    """Registration form post handler"""

    applicant = request.form

    # Add to session
    # do backgroud check
    session['email'] = applicant['email']
    session['password'] = applicant['pswd']
    session['fname'] = applicant['fname']
    session['lname'] = applicant['lname']
    session['phone'] = applicant['phone']

    return jsonify({'msg': "Please consent the background check.", 'status': "OK"})

       



if __name__ == '__main__':
    # app.run()
    app.debug = True

    # Use the DebugToolbar
    #DebugToolbarExtension(app)   # Turned this off for demo

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # This is needed to run from vagrant
    app.run(host="0.0.0.0")

