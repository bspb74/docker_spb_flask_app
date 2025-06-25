from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    session.permanent = True
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.pwd, pwd):
                flash('Login is Successful!', category='success')
                login_user(user, remember=True)
                session['user_id'] = user.id
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist!', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        fName = request.form.get('firstName')
        lName = request.form.get('lastName')
        pwd1 = request.form.get('password1')
        pwd2 = request.form.get('password2')

        createAccount = True

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
            createAccount = False
        if len(email) < 4:
            flash("Not a Valid Email!", category='error')
            createAccount = False
        if len(fName) < 2:
            flash("First Name must be greater than 2", category='error')
            createAccount = False
        if len(lName) < 2:
            flash("First Name must be greater than 2", category='error')
            createAccount = False
        if pwd1 != pwd2:
            flash("Passwords do not match", category='error')
            createAccount = False
        elif len(pwd1) < 9:
            flash("Password length must be at least 8 characters", category='error')
            createAccount = False

        if createAccount:
            new_user = User(email=email, fName=fName, lName=lName, pwd=generate_password_hash(pwd1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account Created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)