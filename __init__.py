from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQL Alchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '\xd5c\xad\x07\x8bv\x0cd\x9f\xc6\xfb\xf8xM\x08S'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    db.init_app(app)
    
    #blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    #blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app