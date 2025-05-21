from flask import Blueprint, render_template
from flask_login import login_required, current_user
from HelpDeskTicketingSystem.models.TicketModel import Ticket

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def home():
    if current_user.account_type == 'admin':
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, tickets=tickets)
