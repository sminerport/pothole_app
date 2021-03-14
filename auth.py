from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, Pothole, Equipment, RepairCrew, WorkOrder
from . import db
from re import sub
from decimal import Decimal

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

@auth.route('/employee', methods=['POST'])
def work_orders_post():
    
    pothole_number = request.form.get('potholes', type=int)
    Pothole.query.filter(Pothole.id == pothole_number).\
        update({"w_order": (1)})
    db.session.commit()
    crew_number = request.form.get('crew', type=int)
    hours = request.form.get('hours', type=int)
    status = request.form.get('status', type=str)
    filler = request.form.get('filler', type=int)
    equipment = request.form.getlist('equipment')
    cost = request.form.get('cost', type=str)
    cost = Decimal(sub(r'[^\d.]', '', cost))


    
    # create a new work order
    new_work_order = WorkOrder(pothole_id=pothole_number,repair_crew_id=crew_number,hours=hours,
                              status=status,fillerAmount=filler,cost=cost)
    db.session.add(new_work_order)
    db.session.commit()
    
    workOrders = db.session.query(WorkOrder, Pothole, RepairCrew).\
            join(Pothole, Pothole.id == WorkOrder.pothole_id).\
            join(RepairCrew, RepairCrew.id == WorkOrder.repair_crew_id).all()
    print(workOrders)
    for order in workOrders:
        print(order.Pothole.location)
    print(equipment)
    
    return render_template('work_orders.html', workOrders = workOrders)

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
    equipmentList = Equipment.query.order_by(Equipment.equipment).all()
    crewList = RepairCrew.query.order_by(RepairCrew.id).all()
    
    return render_template('employee.html', potholes=potholes, equipment=equipmentList, crewList=crewList)

@auth.route('/_update_work_dropdown')
def update_work_dropdown():
    pothole_number = request.args.get('selected_class', type=str)
    pothole_number = pothole_number.split("#",1)[1]
    pothole_number = int(pothole_number[0])

    pothole = Pothole.query.get(pothole_number)
    
    streetNumber = pothole.streetNumber
    streetName = pothole.streetName
    zip = pothole.zip
    size = pothole.size
    district = pothole.district
    location = pothole.location
    priority = pothole.priority
    
    # html_string_selected = ''
    # for row in rows:
    #     html_string_selected += '<option values="{}">{}</option>'.format(row['zipleft'], row['zipleft'])
    #     
    # print(html_string_selected)
        
    return jsonify(streetNumber = streetNumber, streetName = streetName, zip = zip,
                   size = size, district = district, location=location, priority = priority)
    
@auth.route('/_update_work_order')
def update_work_order():
    crew = request.args.get('crew', type=int)
    filler = request.args.get('filler', type=int)
    status = request.args.get('status', type=str)
    hours = request.args.get('hours', type=int)
    equipment = request.args.get('equipment')
    equipment = equipment.split(",")
    
    crewQuery = RepairCrew.query.get(crew)
    people = crewQuery.people
    cost = 0
    peopleCost = people * 20
    fillerCost = filler * 12.50
    
    equipmentQuery = Equipment.query.filter(Equipment.equipment.in_(equipment)).with_entities(Equipment.costPerHour)
    for row in equipmentQuery:
        print(f"row: {row.costPerHour}")
        cost += peopleCost * fillerCost * hours * row.costPerHour
    
    cost = "${:,.2f}".format(cost)
   #  print(f"crew: {crew}")
   #  print(f"filler: {filler}")
   #  print(f"status: {status}")
   #  print(f"hours: {hours}")
   #  print(f"equipment: {equipment}")
   #  for x in equipment:
   #      print(f"test: {x}")
    
    return jsonify(cost=cost)
    
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
    return 'Logout'