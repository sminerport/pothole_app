from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Pothole, Equipment, RepairCrew
from . import db

auth = Blueprint('auth', __name__)
@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first() # if this returns a user, the the email is already in the db
    
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    
    # add the new user to the db
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    
    email = request.form.get('email')
    password = request.form.get('password')
    type = request.form.get('loginType')
    
    user = User.query.filter_by(email=email).first()
    
    #check if user exists
    #take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    
    # if the above check passes, then we know the user has the right credentials
    if type=='Citizen':
        login_user(user)
        return redirect(url_for('main.profile'))
    elif type=='Employee':
        login_user(user)
        return redirect(url_for('auth.employee'))
        
@auth.route('/employee')
@login_required
def employee():
    
    potholes = Pothole.query.filter_by(w_order=0).all()
    
    return render_template('employee.html', potholes=potholes)

@auth.route('/_update_work_dropdown')
def update_work_dropdown():
    pothole_number = request.args.get('selected_class', type=str)
    pothole_number = pothole_number.split("#",1)[1]
    pothole_number = int(pothole_number[0])
    
    print(pothole_number)
    
    pothole = Pothole.query.get(pothole_number)
    
    print(pothole.streetNumber)
    
    streetNumber = pothole.streetNumber
    streetName = pothole.streetName
    zip = pothole.zip
    
    # html_string_selected = ''
    # for row in rows:
    #     html_string_selected += '<option values="{}">{}</option>'.format(row['zipleft'], row['zipleft'])
    #     
    # print(html_string_selected)
        
    return jsonify(streetNumber = streetNumber, streetName = streetName, zip = zip)
    

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
    return 'Logout'