from flask import Blueprint, render_template
from flask_login import login_required, current_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)