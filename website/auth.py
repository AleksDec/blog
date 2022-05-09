from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from .models import User
from . import db
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps


auth=Blueprint("auth", __name__)


# --------  Create an admin-only function  ----------
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

# ----------- SIGN-UP --------------
@auth.route("/sign-up", methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Password don\'t match!', category='error')
        else:
            hashed_password = generate_password_hash(password1, method= "pbkdf2:sha256", salt_length = 8)
            new_user = User(email=email, username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.blog'))


    return render_template("signup.html")


# ----------- LOGIN -------------
@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Successfully logged in.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.blog'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email don\'t exist. Please sign up.', category='error')

    return render_template('login.html')


# ------------ LOGOUT -------------
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))