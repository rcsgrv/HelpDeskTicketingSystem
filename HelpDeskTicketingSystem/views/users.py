from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from ..extensions import db, login_manager

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

from werkzeug.security import check_password_hash, generate_password_hash

@users_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user

    if request.method == 'POST':
        forename = request.form.get('forename')
        surname = request.form.get('surname')
        current_password = request.form.get('current_password')
        new_password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')

        if not forename:
            flash('Forename cannot be blank.', category='error')
        elif not surname:
            flash('Surname cannot be blank.', category='error')
        elif new_password:
            if not current_password:
                flash('You must enter your current password to set a new one.', category='error')
            elif not check_password_hash(user.password, current_password):
                flash('Current password is incorrect.', category='error')
            elif len(new_password) < 8:
                flash('New password must be at least 8 characters long.', category='error')
            elif new_password != password_confirm:
                flash('New passwords do not match.', category='error')
            else:
                user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        else:
            user.forename = forename
            user.surname = surname

            db.session.commit()
            flash('Profile updated successfully.', category='success')
            return redirect(url_for('users.profile'))

    return render_template('edit_profile.html', user=user)