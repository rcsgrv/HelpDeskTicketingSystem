import pytest
from unittest.mock import patch, MagicMock
from flask import session
from HelpDeskTicketingSystem.models.TicketModel import Ticket

# These tests validate the ticket view’s behaviour in the application, including ticket creation, viewing, editing, and deletion.
# Patching is used in each function to mock dependencies such as database queries, form validation, and user authentication,
# as well as template rendering, allowing each route’s logic to be tested without requiring a full application context or real database interactions.

# This Pytest fixture creates a mock Ticket instance for testing
@pytest.fixture
def mock_ticket():
    return Ticket(id=1, subject='Test Subject', description='Test Description', status='Open', priority='Low', estimated_time=3.0, user_id=1)

# Test for rendering the ticket creation page on GET request

def test_create_ticket_get(app):
    with app.test_request_context('/create_ticket', method='GET'):
        mocked_user = MagicMock(is_authenticated=True)
        with patch('flask_login.utils._get_user', return_value=mocked_user), \
             patch('HelpDeskTicketingSystem.views.tickets.render_template') as mock_render:
            mock_render.return_value = 'rendered'
            from HelpDeskTicketingSystem.views.tickets import create_ticket
            result = create_ticket()
            mock_render.assert_called_once_with('create_ticket.html', user=mocked_user)
            assert result == 'rendered'

# Test for successful ticket creation on POST with valid form data

def test_create_ticket_post_success(app):
    form_data = {
        'subject': 'Test Subject',
        'description': 'Test Description',
        'status': 'Open',
        'priority': 'Low',
        'estimated_time': '2'
    }
    with app.test_request_context('/create_ticket', method='POST', data=form_data):
        with patch('flask_login.utils._get_user', return_value=MagicMock(id=1, is_authenticated=True)), \
             patch('HelpDeskTicketingSystem.views.tickets.validate_ticket_form', return_value=None), \
             patch('HelpDeskTicketingSystem.views.tickets.db.session.add') as mock_add, \
             patch('HelpDeskTicketingSystem.views.tickets.db.session.commit') as mock_commit, \
             patch('HelpDeskTicketingSystem.views.tickets.flash') as mock_flash, \
             patch('HelpDeskTicketingSystem.views.tickets.redirect') as mock_redirect, \
             patch('HelpDeskTicketingSystem.views.tickets.url_for') as mock_url_for:

            mock_url_for.return_value = '/'
            mock_redirect.return_value = 'redirected'

            from HelpDeskTicketingSystem.views.tickets import create_ticket
            result = create_ticket()

            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            mock_flash.assert_called_once_with('Ticket created successfully!', category='success')
            assert result == 'redirected'

# Test for ticket creation POST request with form validation errors

def test_create_ticket_post_with_errors(app):
    form_data = {
        'subject': '',
        'description': 'Test Description',
        'status': 'Open',
        'priority': 'High',
        'estimated_time': '1'
    }
    with app.test_request_context('/create_ticket', method='POST', data=form_data):
        with patch('flask_login.utils._get_user', return_value=MagicMock(is_authenticated=True)), \
             patch('HelpDeskTicketingSystem.views.tickets.validate_ticket_form', return_value='Error'), \
             patch('HelpDeskTicketingSystem.views.tickets.render_ticket_form') as mock_render:

            mock_render.return_value = 'rendered'
            from HelpDeskTicketingSystem.views.tickets import create_ticket
            result = create_ticket()
            assert result == 'rendered'

# Test for viewing ticket details as an authorised user that owns the ticket

def test_view_ticket_details_authorised_user(app, mock_ticket):
    with app.test_request_context('/ticket_details/1'):
        with patch('flask_login.utils._get_user', return_value=MagicMock(id=1, account_type='Regular User')), \
             patch('HelpDeskTicketingSystem.views.tickets.Ticket.query') as mock_query, \
             patch('HelpDeskTicketingSystem.views.tickets.render_template') as mock_render:

            mock_query.filter_by.return_value.first.return_value = mock_ticket
            mock_render.return_value = 'rendered'
            from HelpDeskTicketingSystem.views.tickets import ticket_details
            result = ticket_details(1)
            assert result == 'rendered'

# Test for viewing ticket details as an unauthorised user i.e. not the owner and not an administrator

def test_view_ticket_details_unauthorised_user(app, mock_ticket):
    with app.test_request_context('/ticket_details/1'):
        with patch('flask_login.utils._get_user', return_value=MagicMock(id=2, account_type='Regular User')), \
             patch('HelpDeskTicketingSystem.views.tickets.Ticket.query') as mock_query, \
             patch('HelpDeskTicketingSystem.views.tickets.flash') as mock_flash, \
             patch('HelpDeskTicketingSystem.views.tickets.redirect') as mock_redirect, \
             patch('HelpDeskTicketingSystem.views.tickets.url_for') as mock_url_for:

            mock_query.filter_by.return_value.first.return_value = mock_ticket
            mock_url_for.return_value = '/'
            mock_redirect.return_value = 'redirected'

            from HelpDeskTicketingSystem.views.tickets import ticket_details
            result = ticket_details(1)
            mock_flash.assert_called_once()
            assert result == 'redirected'

 # Test for editing a ticket via POST request as an administrator           

def test_edit_ticket_post_as_administrator(app, mock_ticket):
    form_data = {
        'subject': 'Updated Subject',
        'description': 'Updated Description',
        'status': 'Closed',
        'priority': 'High',
        'estimated_time': '4'
    }
    with app.test_request_context('/edit_ticket/1', method='POST', data=form_data):
        with patch('flask_login.utils._get_user', return_value=MagicMock(id=1, account_type='Administrator')), \
             patch('HelpDeskTicketingSystem.views.tickets.Ticket.query') as mock_query, \
             patch('HelpDeskTicketingSystem.views.tickets.validate_ticket_form', return_value=None), \
             patch('HelpDeskTicketingSystem.views.tickets.db.session.commit') as mock_commit, \
             patch('HelpDeskTicketingSystem.views.tickets.flash') as mock_flash, \
             patch('HelpDeskTicketingSystem.views.tickets.redirect') as mock_redirect, \
             patch('HelpDeskTicketingSystem.views.tickets.url_for') as mock_url_for:

            mock_query.filter_by.return_value.first.return_value = mock_ticket
            mock_url_for.return_value = '/ticket/1'
            mock_redirect.return_value = 'redirected'

            from HelpDeskTicketingSystem.views.tickets import edit_ticket
            result = edit_ticket(1)
            mock_commit.assert_called_once()
            mock_flash.assert_called_once()
            assert result == 'redirected'

# Test for deleting a ticket via POST request as an administrator

def test_delete_ticket_as_administrator(app, mock_ticket):
    with app.test_request_context('/delete_ticket/1', method='POST'):
        with patch('flask_login.utils._get_user', return_value=MagicMock(account_type='Administrator')), \
             patch('HelpDeskTicketingSystem.views.tickets.Ticket.query') as mock_query, \
             patch('HelpDeskTicketingSystem.views.tickets.db.session.delete') as mock_delete, \
             patch('HelpDeskTicketingSystem.views.tickets.db.session.commit') as mock_commit, \
             patch('HelpDeskTicketingSystem.views.tickets.flash') as mock_flash, \
             patch('HelpDeskTicketingSystem.views.tickets.redirect') as mock_redirect, \
             patch('HelpDeskTicketingSystem.views.tickets.url_for') as mock_url_for:

            mock_query.filter_by.return_value.first.return_value = mock_ticket
            mock_url_for.return_value = '/'
            mock_redirect.return_value = 'redirected'

            from HelpDeskTicketingSystem.views.tickets import delete_ticket
            result = delete_ticket(1)

            mock_delete.assert_called_once_with(mock_ticket)
            mock_commit.assert_called_once()
            mock_flash.assert_called_once()
            assert result == 'redirected'