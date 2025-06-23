from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from ..models import User
from HelpDeskTicketingSystem.utils.registration_helper import validate_registration_form
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, login_manager

# Route logic, Blueprints, basic HTML, and database configurationg were implemented with guidance from a tutorial by Tech With Tim (Tech With Tim, 2021).

# This Blueprint manages user authentication and registration, including login, logout, 
# user registration with form validation, and administrator account verification 
# via a secure administrator verification code. Session storage is used to temporarily store registration data 
# for administrator users pending verification.
# Password hashing is used for security purposes, and Flask-Login is used for user session management and access control.

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email:
            flash('Please enter your email address.', category='error')
        elif '@' not in email or '.' not in email.split('@')[-1]:
            flash('Please enter a valid email address.', category='error')
        elif not password:
            flash('Please enter your password.', category='error')
        else:
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('home.home'))
            else:
                flash('Incorrect username or password. Please try again.', category='error')
    
    return render_template("login.html", user=current_user, email='')

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

        error = validate_registration_form(forename, surname, email, password, password_confirm, account_type, user)
        if error:
            flash(error, category='error')
            return render_template(
                "register.html",
                user=current_user,
                forename=forename,
                surname=surname,
                email=email,
                account_type=account_type
            )

        if account_type == 'Administrator':
            session['pending_user'] = {
                'forename': forename,
                'surname': surname,
                'email': email,
                'password': password,
                'account_type': account_type
            }
            return redirect(url_for('auth.admin_code'))

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
            flash('Session expired. Please complete the registration form again.', category='error')
            return redirect(url_for('auth.register'))

        if submitted_code == correct_code:
            new_user = User(
                forename=pending_user['forename'],
                surname=pending_user['surname'],
                email=pending_user['email'],
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
            flash('Incorrect verification code. Please try again.', category='error')

    return render_template('admin_code.html')