from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from HelpDeskTicketingSystem.models.TicketModel import Ticket
from ..extensions import db

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

        if len(subject) < 1:
            flash('Subject cannot be blank.', category='error')
        elif len(subject) > 50:
            flash('Subject must not exceed 50 characters.', category='error')
        elif len(description) < 1:
            flash('Description cannot be blank.', category='error')
        elif len(description) > 250:
            flash('Description must not exceed 250 characters.', category='error')
        elif not priority:
            flash('You must select a priority.', category='error')
        elif not status:
            flash('You must select a status.', category='error')
        elif estimated_time:
            try:
                estimated_time_val = float(estimated_time)
                if estimated_time_val < 0:
                    flash('Estimated time cannot be < 1 hours.', category='error')
                    return render_template('tickets.create_ticket.html', user=current_user)
            except ValueError:
                flash('Estimated time must be a number.', category='error')
                return render_template('tickets.create_ticket.html', user=current_user)
        else:
            new_ticket = Ticket(
                subject=subject,
                description=description,
                priority=priority,
                status=status,
                time_estimate=float(estimated_time) if estimated_time else None,
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
    
    if ticket.user_id != current_user.id and current_user.account_type != 'admin':
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
    
    if ticket.user_id != current_user.id and current_user.account_type != 'admin':
        flash('You do not have permission to edit this ticket.', category='error')
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        ticket.subject = request.form.get('subject')
        ticket.description = request.form.get('description')
        ticket.status = request.form.get('status')
        ticket.priority = request.form.get('priority')
        ticket.estimated_time = request.form.get('estimated_time')

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

    if current_user.account_type != 'admin':
        flash('You do not have permission to delete this ticket.', category='error')
        return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))

    db.session.delete(ticket)
    db.session.commit()
    flash('Ticket deleted successfully.', category='success')
    return redirect(url_for('home.home'))