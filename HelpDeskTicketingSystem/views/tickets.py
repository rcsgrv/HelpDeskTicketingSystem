from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from HelpDeskTicketingSystem.models.TicketModel import Ticket
from HelpDeskTicketingSystem.utils.ticket_helper import validate_ticket_form, render_ticket_form
from ..extensions import db

# This Blueprint handles ticket management functionality including creating, viewing, editing, 
# and deleting tickets. This Blueprint enforces user authentication and access control, allowing only ticket owners 
# or administrators to view or modify tickets.
# Form validation is used to ensure data integrity before database operations are performed, and appropriate user feedback is provided via flash messages. 

tickets_bp = Blueprint('tickets', __name__)

@tickets_bp.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':
        subject = request.form.get('subject')
        description = request.form.get('description')
        status = request.form.get('status')
        priority = request.form.get('priority')
        estimated_time = request.form.get('estimated_time')

        error = validate_ticket_form(subject, description, priority, status, estimated_time)
        if error:
            return render_ticket_form(
                'create_ticket.html',
                error=error,
                user=current_user,
                subject=subject,
                description=description,
                priority=priority,
                status=status,
                estimated_time=estimated_time
            )

        new_ticket = Ticket(
            subject=subject,
            description=description,
            priority=priority,
            status=status,
            estimated_time=float(estimated_time),
            user_id=current_user.id
        )
        db.session.add(new_ticket)
        db.session.commit()
        flash('Ticket created successfully!', category='success')
        return redirect(url_for('home.home'))

    return render_template('create_ticket.html', user=current_user)

@tickets_bp.route('/ticket_details/<int:ticket_id>', methods=['GET'])
@login_required
def ticket_details(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()

    if not ticket:
        flash('Ticket not found.', category='error')
        return redirect(url_for('home.home'))
    
    if ticket.user_id != current_user.id and current_user.account_type != 'Administrator':
        flash('You do not have permission to view this ticket.', category='error')
        return redirect(url_for('home.home'))

    return render_template('ticket_details.html', ticket=ticket)

@tickets_bp.route('/edit_ticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()

    if not ticket:
        flash('Ticket not found.', category='error')
        return redirect(url_for('home.home'))

    if ticket.user_id != current_user.id and current_user.account_type != 'Administrator':
        flash('You do not have permission to edit this ticket.', category='error')
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        subject = request.form.get('subject')
        description = request.form.get('description')
        estimated_time = request.form.get('estimated_time')

        if current_user.account_type != 'Administrator':
            status = ticket.status 
            priority = ticket.priority
        else:
            status = request.form.get('status')
            priority = request.form.get('priority')

        error = validate_ticket_form(subject, description, priority, status, estimated_time)
        if error:
            return render_ticket_form(
                'edit_ticket.html',
                error=error,
                ticket=ticket
            )

        ticket.subject = subject
        ticket.description = description
        ticket.status = status
        ticket.priority = priority
        ticket.estimated_time = float(estimated_time)

        db.session.commit()
        flash('Ticket updated successfully.', category='success')
        return redirect(url_for('tickets.ticket_details', ticket_id=ticket.id))

    return render_template('edit_ticket.html', ticket=ticket)

@tickets_bp.route('/delete_ticket/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()

    if not ticket:
        flash('Ticket not found.', category='error')
        return redirect(url_for('home.home'))

    if current_user.account_type != 'Administrator':
        flash('You do not have permission to delete this ticket.', category='error')
        return redirect(url_for('tickets.ticket_details', ticket_id=ticket.id))

    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully.', category='success')
    return redirect(url_for('home.home'))
