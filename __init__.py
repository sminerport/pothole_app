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
        con.close()
    
    return app