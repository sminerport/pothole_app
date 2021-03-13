from flask import Blueprint, render_template, request, jsonify
from itertools import groupby
from flask_login import login_required, current_user
import sqlite3
from . import db

def get_db_connection():
    conn = sqlite3.connect(".\\project\\db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

main = Blueprint('main', __name__)
@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    conn = get_db_connection()
    
    #get init values
    rows = conn.execute("select FULLNAME, ZIPLEFT \
                                    from DenverStreets \
                                    where JURISID == 'DENVER' \
                                    group by fullname").fetchall()
    
    conn.close()
                                
    return render_template('profile.html', name=current_user.name, streetList=rows)

@main.route('/profile', methods=['POST'])
def profile_post():
    
    streetNumber = request.form.get('streetNumber')
    streetName = request.form.get('streetName')
    state = "CO"
    city = "DENVER"
    zipCode = request.form.get('zip')
    location = request.form.get('location')
    size = int(request.form['answer'])
    priority = None
    w_order = 0
    
    conn = get_db_connection()
    
    district = conn.execute('SELECT distinct addressquad \
                            FROM DenverStreets \
                            WHERE zipleft = ? \
                            AND fullname = ?  \
                            AND jurisid = ?', (zipCode, streetName, city)).fetchone()['addressquad']
    
    if district == 'N':
         district = 'North'
    elif district == 'E':
         district = 'East'
    elif district == 'S':
         district = 'South'
    elif district == 'W':
        district = 'West'
    elif district == 'NW':
        district = 'North West'
    elif district == 'NE':
        district = 'North East'
    elif district == 'SW':
        district = 'South West'
    elif district == 'SE':
        district = 'South East'
        
    if size == 1 or size == 2:
        priority = 'Very Low'
    elif size == 3 or size == 4:
        priority = 'Low'
    elif size == 5 or size == 6:
        priority = 'Medium'
    elif size == 7 or size == 8:
        priority = 'High'
    elif size == 9 or size == 10:
        priority = 'Urgent'
        
    print(current_user.id)
    print(streetNumber)
    print(streetName)
    print(city)
    print(state)
    print(zipCode)
    print(location)
    print(district)
    print(size)
    print(priority)

    conn.execute('INSERT INTO pothole (user_id, streetNumber, streetName, city, state, \
                 zip, location, district, size, priority, w_order) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                (current_user.id,streetNumber,streetName,city,state,zipCode,location,district,size,priority,w_order))
    
    conn.commit()
    conn.close()   

    return render_template('index.html')


@main.route('/_update_dropdown')
def update_dropdown():
    selected_class = request.args.get('selected_class', type=str)
    print(selected_class)
    
    conn = get_db_connection()
    
    #get init values
    rows = conn.execute("select FULLNAME, ZIPLEFT \
                                    from DenverStreets \
                                    where JURISID == 'DENVER' \
                                    and fullname = ? \
                                    group by fullname", (selected_class,)).fetchall()
    html_string_selected = ''
    for row in rows:
        html_string_selected += '<option values="{}">{}</option>'.format(row['zipleft'], row['zipleft'])
        
    print(html_string_selected)
        
    return jsonify(html_string_selected=html_string_selected)
    