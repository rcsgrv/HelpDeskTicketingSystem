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

from flask import session

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

        if user is not None:
            flash('The email you have provided is already associated with an account.', category='error')
        elif not email or len(email) < 1:
            flash('Email cannot be blank.', category='error')
        elif not forename or len(forename) < 1:
            flash('Forename cannot be blank.', category='error')
        elif not surname or len(surname) < 1:
            flash('Surname cannot be blank.', category='error')
        elif password != password_confirm:
            flash('Your passwords do not match.', category='error')
        elif not password or len(password) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        elif account_type == 'Administrator':

            session['pending_user'] = {
                'email': email,
                'forename': forename,
                'surname': surname,
                'password': password,
                'account_type': account_type
            }
            return redirect(url_for('auth.admin_code'))
        else:

            new_user = User(
                email=email,
                forename=forename,
                surname=surname,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                account_type=account_type
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account successfully created.', category='success')
            return redirect(url_for('home.home'))

    return render_template("register.html", user=current_user)

@auth_bp.route('/admin_code', methods=['GET', 'POST'])
def admin_code():
    if request.method == 'POST':
        submitted_code = request.form.get('admin_code')
        correct_code = '53c17e4d8efdafeddd375e53e4689cc757f1f322ef4595caedc3e85e2fb79c4e'  

        pending_user = session.get('pending_user')

        if not pending_user:
            flash('Session expired. Please fill out the registration form again.', category='error')
            return redirect(url_for('auth.register'))

        if submitted_code == correct_code:
            new_user = User(
                email=pending_user['email'],
                forename=pending_user['forename'],
                surname=pending_user['surname'],
                password=generate_password_hash(pending_user['password'], method='pbkdf2:sha256'),
                account_type=pending_user['account_type']
            )
            db.session.add(new_user)
            db.session.commit()
            session.pop('pending_user', None)
            login_user(new_user, remember=True)
            flash('Administrator account successfully created.', category='success')
            return redirect(url_for('home.home'))
        else:
            flash('Incorrect admin verification code.', category='error')

    return render_template('admin_code.html')
