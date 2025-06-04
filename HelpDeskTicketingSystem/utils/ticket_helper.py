def validate_ticket_form(subject, description, priority, status, estimated_time):
    if not subject or len(subject.strip()) < 1:
        return 'Subject cannot be blank.'
    if len(subject) > 50:
        return 'Subject must not exceed 50 characters.'
    if not description or len(description.strip()) < 1:
        return 'Description cannot be blank.'
    if len(description) > 250:
        return 'Description must not exceed 250 characters.'
    if not priority:
        return 'You must select a priority.'
    if not status:
        return 'You must select a status.'
    try:
        estimated_time_val = float(estimated_time)
        if estimated_time_val < 1:
            return 'Estimated time cannot be less than 1 hour.'
        if estimated_time_val > 40:
            return 'Estimated time cannot be more than 40 hours.'
    except (ValueError, TypeError):
        return 'Estimated time must be a number.'
    return None 

def render_ticket_form(template, error, **context):
    from flask import flash, render_template
    flash(error, category='error')
    return render_template(template, **context)
