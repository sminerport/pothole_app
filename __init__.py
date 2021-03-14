import pandas as pd
import sqlite3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQL Alchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '\xd5c\xad\x07\x8bv\x0cd\x9f\xc6\xfb\xf8xM\x08S'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    
    #blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    #blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    con = sqlite3.connect(".\\project\\db.sqlite")
    cur = con.cursor()
    result = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='DenverStreets';").fetchone()
    
    if result == None:
        df = pd.read_csv(".\\project\\street_centerline.csv")
        df.to_sql('DenverStreets', con)
        df.columns = df.columns.str.strip()
    
    result = cur.execute("SELECT name from sqlite_master WHERE type='table' AND name='equipment';").fetchone()
  
    if result == None:
        from .models import Equipment
        from .models import RepairCrew
        with app.app_context():
            db.create_all()
            #db.session.commit()
            newEquipment1 = Equipment(equipment="Bobcat", costPerHour = 31.25)
            newEquipment2 = Equipment(equipment="Steam Roller", costPerHour = 23.75)
            newEquipment3 = Equipment(equipment="Patch Hand Roller", costPerHour = 10.00)
            newEquipment4 = Equipment(equipment="Bull Dozer", costPerHour = 25.00)
            newEquipment5 = Equipment(equipment="Dump Truck", costPerHour = 45.50)
            newEquipment6 = Equipment(equipment="Power Tamper", costPerHour = 15.00)
            newEquipment7 = Equipment(equipment="Pro-Patch Asphalt Patcher", costPerHour = 33.25)
            newEquipment8 = Equipment(equipment="Spray-Injection Machine", costPerHour = 28.75)
            db.session.add_all([newEquipment1, newEquipment2, newEquipment3, newEquipment4, newEquipment5,
                            newEquipment6, newEquipment7, newEquipment8])
            newRepair1 = RepairCrew(people=5)
            newRepair2 = RepairCrew(people=10)
            newRepair3 = RepairCrew(people=15)
            newRepair4 = RepairCrew(people=20)
            newRepair5 = RepairCrew(people=2)
            newRepair6 = RepairCrew(people=3)
            db.session.add_all([newRepair1,
                                newRepair2,
                                newRepair3,
                                newRepair4,
                                newRepair5,
                                newRepair6])
            db.session.commit()
            
    con.close()

    return app

