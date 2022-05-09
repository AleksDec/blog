import os

from flask import Flask, render_template, redirect, url_for, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from os import path
from flask_login import LoginManager, current_user
from functools import wraps
from dotenv import load_dotenv

# ------------- Getting password from the environmental variable ----------------
load_dotenv()

db = SQLAlchemy()
DB_NAME = os.getenv('DB_NAME')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # Suppressing the SQLALCHEMY_TRACK_MODIFICATIONS warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # Connect to DB
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # CSRF security
    app.config['CSRF_ENABLED'] = True
    # CKEditor, Bootstrap
    ckeditor = CKEditor(app)
    Bootstrap(app)

    db.init_app(app)

    # -------  Import views & auth  -------
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # -------  Import User db & create database  --------
    from .models import User, BlogPost
    create_database(app)

    # --------  Creating LoginManager class to cooperate with our Flask app  ---------
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # --------  Create a user_loader function  ---------
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # # --------  Create an admin-only function  ----------
    # def admin_only(f):
    #     @wraps(f)
    #     def decorated_function(*args, **kwargs):
    #         if current_user.id != 1:
    #             return abort(403)
    #         return f(*args, **kwargs)
    #     return decorated_function

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created database!")
