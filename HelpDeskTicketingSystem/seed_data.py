from werkzeug.security import generate_password_hash
from datetime import datetime, timezone
from .extensions import db
from .models import User, Ticket

def populate_seed_data():
    if User.query.first():
        print("Seed data already exists.")
        return

    # 10 users
    users = []
    for i in range(1, 11):
        user = User(
            forename=f'User{i}',
            surname='Test',
            email=f'user{i}@test.com',
            password=generate_password_hash(f'password{i}'),
            account_type='Administrator' if i == 1 else 'Regular User'
        )
        users.append(user)

    db.session.add_all(users)
    db.session.commit()

    users = User.query.all()

    # 10 tickets
    subjects = [
        'Candidate - Schedule - Performance',
        'Maintenance - Financials - Back Office Export Templates',
        'Maintenance - System - Job Scheduler - Mailbox Scanner',
        'Maintenance - Templates - Documents / Email / SMS',
        'Vacancy - Vacancy Record - Shortlist',
        'Timesheet - Timesheet Adjustments - Adjust Hours',
        'Vacancy - Vacancy Record - Shortlist - Requirement Modification Events',
        'Placement - Schedule - Delete Booking & Requirements',
        'Client - Client Contacts',
        'Searching - Main Entity Search Screens'
    ]
    descriptions = [
        'When a candidate has a large number of placements (>200) the schedule tab takes 20-30 seconds to load.',
        'Two fields overlap on the Back Office Export Templates form when creating a candidate export template.',
        'The System Mailbox form needs to be renamed to Mailbox Scanner Ruleset.',
        'Merging an email hides all attachments that were added to the email.',
        'Users are able to add multiple instances of the same shortlist record without any validation errors occurring.',
        'Adjustment timesheets error when you set them to Rejected.',
        'Requirements Added logs are getting raised when adding bookings to placement records.',
        'Eclipse encounters an error when attempting to delete bookings on a placement record.',
        'Client Contact Record Opened logs do not link to the client record.',
        'Users are unable to login to Eclipse if a live list exists that contains a search option that uses a stored proc.'
    ]
    statuses = ['Open', 'In Progress', 'Closed']
    priorities = ['Low', 'Normal', 'High']
    estimated_times = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

    tickets = []
    for i in range(10):
        ticket = Ticket(
            subject=subjects[i],
            description=descriptions[i],
            status=statuses[i % len(statuses)],
            priority=priorities[i % len(priorities)],
            estimated_time=estimated_times[i],
            date_created=datetime.now(timezone.utc),
            user_id=users[i % len(users)].id
        )
        tickets.append(ticket)

    db.session.add_all(tickets)
    db.session.commit()

    print("Seeded 10 users and 10 tickets.")
