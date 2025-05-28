from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from HelpDeskTicketingSystem.models.TicketModel import Ticket

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    if current_user.account_type == 'Administrator':
        tickets = Ticket.query.order_by(Ticket.id.desc()).paginate(page=page, per_page=per_page)
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.id.desc()).paginate(page=page, per_page=per_page)

    return render_template("home.html", user=current_user, tickets=tickets, per_page=per_page)