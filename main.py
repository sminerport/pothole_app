from flask import Blueprint, render_template
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
    
    streetList = conn.execute("SELECT DISTINCT t.FULLNAME FROM \
                                 (SELECT FULLNAME \
                                 FROM DenverStreets \
                                 WHERE JURISID == 'DENVER') AS t").fetchall()
    print(streetList)
    conn.close()
                                
    return render_template('profile.html', name=current_user.name, streetList=streetList)