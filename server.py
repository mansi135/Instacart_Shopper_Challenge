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
    session['phone_type'] = applicant['phone_type']
    session['over_21'] = applicant['over_21']

    return jsonify({'msg': "Please consent the background check.", 'status': "OK"})

       
@app.route('/confirmation')
def show_confirmation():
    """Add applicant to DB and send confirmation"""

    # if user is already logged in then he should not access this page
    if 'logged_in' in session:
        return redirect('/view-application')

    # if user is trying to access without registering then send him to register page
    if 'password' not in session:
        return redirect('/')

    
    session['date_applied'] = datetime.now().date()
    session['status'] = 'applied'

    shopper_object = {}
    shopper_object['first_name'] = session['fname']   
    shopper_object['last_name'] = session['lname']  
    shopper_object['phone'] = session['phone']   
    shopper_object['email'] = session['email'] 
    shopper_object['phone_type'] = session['phone_type']
    shopper_object['over_21'] = session['over_21']
    shopper_object['date_applied'] = session['date_applied']
    shopper_object['status'] = session['status']  
    shopper_object['_id'] = random.randint(1, 100000) # in real database it will be autoinc primary key

    session['shopper_object'] = shopper_object

    #  Emitting the record to backend console with bare minimum inputs from user
    pprint(shopper_object)

    del session['password']

    session['logged_in'] = True

    return render_template("confirmation.html")


@app.route('/login')
def login():
    """Render Login Page"""

    if 'logged_in' in session:
        return redirect('/view-application')

    return render_template("login.html")


# This is an ajax route/end-point
# We are not persisting data in database, but if there was an existing data, then they can login 
@app.route('/login', methods=["POST"])
def login_check():
    """Login check"""

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        existing_applicant = Applicant.query.filter_by(email=email, password=password).one()
    except:
        return jsonify({'msg': "Email or Password is incorrect. Please try again!",'status': "NotOK"})

    session['email'] = email
    session['logged_in'] = True

    return jsonify({'msg': "Welcome {} You are successfully logged in.".format(existing_applicant.first_name), 'status': "OK"})



@app.route('/view-application')
@login_required
def view_application():
    """View the application page"""

    # not-persisted user
    if 'shopper_object' in session:
        shopper = session['shopper_object']
    else:
        email = session['email']
        shopper = Applicant.query.filter_by(email=email).one()
        shopper.date_applied = shopper.date_applied.strftime('%Y-%m-%d')
    
    return render_template("application.html", shopper=shopper)



# This is an ajax route/end-point
@app.route('/edit-application', methods=["POST"])
@login_required
def edit():
    """Edit Application"""

    edited_info = request.form

    if 'shopper_object' in session:
        return jsonify({'msg': "We are not persisting in database.", 'status': "OK"})

    else:
        shopper = Applicant.query.filter_by(email=session['email']).one()

        if shopper.phone != edited_info['phone'] and Applicant.query.filter_by(phone=edited_info['phone']).first() or \
                shopper.email != edited_info['email'] and Applicant.query.filter_by(email=edited_info['email']).first():
            return jsonify({'msg': "This email or phone number is already taken.", 'status': "notOK"})
            
        else:
            shopper.email = edited_info['email']
            shopper.first_name = edited_info['fname']
            shopper.last_name = edited_info['lname']
            shopper.phone = edited_info['phone']
            shopper.phone_type = edited_info['phone_type']
            shopper.over_21 = edited_info['over_21']

            session['email'] = shopper.email

            db.session.commit()

            return jsonify({'msg': "Successfully Udpated.", 'status': "OK"})


@app.route('/logout')
def logout():
    """Logout Applicant"""

    #del session['user_id']
    session.clear()
    flash("You were logged out.")

    return redirect("/")


if __name__ == '__main__':
    # app.run()
    app.debug = True

    # Use the DebugToolbar
    #DebugToolbarExtension(app)   # Turned this off for production quality code

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # This is needed to run from vagrant
    app.run(host="0.0.0.0")

