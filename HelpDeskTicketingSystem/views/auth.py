from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, login_manager

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            flash('Logged in successfully.', category='success')
            login_user(user, remember=True)
            return redirect(url_for('home.home'))
        else:
            flash('Incorrect username or password. Please try again.', category='error')
    
    return render_template("login.html", user=current_user)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        forename = request.form.get('forename')
        surname = request.form.get('surname')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        account_type = request.form.get('account_type')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('The email you have provided is already associated with an account.', category='error')
        elif len(email) < 1:
            flash('Email cannot be blank.', category='error') 
        elif len(forename) < 1:
            flash('Forename cannot be blank.', category='error') 
        elif len(surname) < 1:
            flash('Surname cannot be blank.', category='error') 
        elif password != password_confirm:
            flash('Your passwords do not match.', category='error') 
        elif len(password) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        else:
            new_user = User(email=email, forename=forename, surname=surname, password=generate_password_hash(password, method='pbkdf2:sha256'), account_type=account_type)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account successfully created.', category='success')
            return redirect(url_for('home.home'))
        
    return render_template("register.html", user=current_user)