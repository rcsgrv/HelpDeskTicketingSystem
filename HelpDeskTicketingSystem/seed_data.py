from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from .extensions import db
from .models import User, Ticket

def populate_dummy_data():
    if User.query.first():
        print("Seed data already exists.")
        return

    # 10 users
    users = []
    for i in range(1, 11):
        user = User(
            forename=f'User{i}',
            surname='Test',
            email=f'user{i}@example.com',
            password=generate_password_hash(f'password{i}'),
            account_type='Administrator' if i == 1 else 'Regular User'
        )
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    # 10 tickets
    subjects = [
        'Login form is not functioning correctly',
        'Page crashes on submit',
        'Feature request: Dark Mode',
        'Bug in search filter',
        'Slow dashboard loading',
        'Error 500 on profile update',
        'Unable to reset password',
        'Missing tooltip on button',
        'Dropdown not responsive',
        'Checkbox selection issue'
    ]
    descriptions = [
        'This is a dummy ticket for testing.',
        'Steps to reproduce: open page, click button.',
        'Expected vs actual results differ.',
        'New ticket for development testing.',
        'This appears only on mobile.',
        'Firefox shows different behaviour.',
        'Investigate logs for error stack trace.',
        'Maybe a caching issue?',
        'Seen after last deployment.',
        'Only affects users with long names.'
    ]
    statuses = ['Open', 'In Progress', 'Closed']
    priorities = ['Low', 'Medium', 'High']
    estimated_times = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    base_time = datetime.now()

    tickets = []
    for i in range(10):
        ticket = Ticket(
            subject=subjects[i],
            description=descriptions[i],
            status=statuses[i % len(statuses)],
            priority=priorities[i % len(priorities)],
            estimated_time=estimated_times[i],
            date_created=base_time - timedelta(days=i),
            user_id=users[i % len(users)].id
        )
        tickets.append(ticket)

    db.session.add_all(tickets)
    db.session.commit()

    print("Seeded 10 users and 10 tickets.")
