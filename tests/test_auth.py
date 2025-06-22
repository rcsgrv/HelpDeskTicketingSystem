import pytest
from unittest.mock import patch, MagicMock
from flask import session
from HelpDeskTicketingSystem.views.auth import login, logout, register, admin_code
from werkzeug.security import generate_password_hash

# These tests validate the auth view's behaviour in the application, including login, logout, registration,
# and administrator verification. Patching is used in each function to mock dependencies
# such as database queries, password checks, session management, and template rendering, allowing
# each route's logic to be tested without requiring a full application context or real database interactions.

@pytest.fixture
def mock_user():
    user = MagicMock()
    user.password = generate_password_hash('correct_password')
    return user

# Test for rendering the login page on GET request

def test_login_get(app):
    with app.test_request_context('/login', method='GET'):
        with patch('flask_login.utils._get_user', return_value=None), \
             patch('HelpDeskTicketingSystem.views.auth.render_template') as mock_render_template:
            mock_render_template.return_value = 'rendered'
            result = login()
            mock_render_template.assert_called_once_with("login.html", user=None, email='')
            assert result == 'rendered'

# Test for successful login when credentials are correct

def test_login_post_success(app, mock_user):
    with app.test_request_context('/login', method='POST', data={'email': 'testuser@test.com', 'password': 'correct_password'}):
        with patch('HelpDeskTicketingSystem.views.auth.User.query') as mock_query, \
             patch('werkzeug.security.check_password_hash', return_value=True), \
             patch('HelpDeskTicketingSystem.views.auth.login_user') as mock_login_user, \
             patch('HelpDeskTicketingSystem.views.auth.flash') as mock_flash, \
             patch('HelpDeskTicketingSystem.views.auth.redirect') as mock_redirect, \
             patch('HelpDeskTicketingSystem.views.auth.url_for') as mock_url_for:

            mock_query.filter_by.return_value.first.return_value = mock_user
            mock_url_for.return_value = '/'
            mock_redirect.return_value = 'redirected'

            response = login()

            mock_flash.assert_called_once_with('Logged in successfully.', category='success')
            mock_login_user.assert_called_once_with(mock_user, remember=True)
            mock_redirect.assert_called_once_with('/')
            assert response == 'redirected'

# Test for failed login when credentials are incorrect

def test_login_post_failure(app):
    with app.test_request_context('/login', method='POST', data={'email': 'testuser@test.com', 'password': 'wrong'}):
        with patch('HelpDeskTicketingSystem.views.auth.User.query') as mock_query, \
             patch('werkzeug.security.check_password_hash', return_value=False), \
             patch('HelpDeskTicketingSystem.views.auth.flash') as mock_flash, \
             patch('HelpDeskTicketingSystem.views.auth.render_template') as mock_render_template, \
             patch('flask_login.utils._get_user', return_value=None):

            mock_query.filter_by.return_value.first.return_value = MagicMock(password='fake_hash')
            mock_render_template.return_value = 'rendered'

            response = login()

            mock_flash.assert_called_once_with('Incorrect username or password. Please try again.', category='error')
            mock_render_template.assert_called_once_with("login.html", user=None, email='')
            assert response == 'rendered'

# Test for logging out a currently authenticated user

def test_logout(app):
    with app.test_request_context('/logout'):
        with patch('flask_login.utils._get_user', return_value=MagicMock(is_authenticated=True)), \
             patch('HelpDeskTicketingSystem.views.auth.logout_user') as mock_logout_user, \
             patch('HelpDeskTicketingSystem.views.auth.redirect') as mock_redirect, \
             patch('HelpDeskTicketingSystem.views.auth.url_for') as mock_url_for:

            mock_url_for.return_value = '/login'
            mock_redirect.return_value = 'redirected'

            response = logout()

            mock_logout_user.assert_called_once()
            mock_redirect.assert_called_once_with('/login')
            assert response == 'redirected'

# Test for rendering the registration page on GET request

def test_register_get(app):
    with app.test_request_context('/register', method='GET'):
        with patch('flask_login.utils._get_user', return_value=None), \
             patch('HelpDeskTicketingSystem.views.auth.render_template') as mock_render_template:

            mock_render_template.return_value = 'rendered'
            response = register()

            mock_render_template.assert_called_once_with("register.html", user=None)
            assert response == 'rendered'

# Test for successful registration of a regular user

def test_register_post_valid_regular_user(app):
    data = {
        'email': 'test@test.com',
        'forename': 'Test',
        'surname': 'User',
        'password': 'password',
        'password_confirm': 'password',
        'account_type': 'Regular User'
    }
    with app.test_request_context('/register', method='POST', data=data):
        with patch('flask_login.utils._get_user', return_value=None), \
             patch('HelpDeskTicketingSystem.views.auth.User.query') as mock_query, \
             patch('HelpDeskTicketingSystem.views.auth.validate_registration_form', return_value=None), \
             patch('werkzeug.security.generate_password_hash', return_value='hashed_pw'), \
             patch('HelpDeskTicketingSystem.views.auth.db.session.add') as mock_add, \
             patch('HelpDeskTicketingSystem.views.auth.db.session.commit') as mock_commit, \
             patch('HelpDeskTicketingSystem.views.auth.login_user') as mock_login, \
             patch('HelpDeskTicketingSystem.views.auth.flash') as mock_flash, \
             patch('HelpDeskTicketingSystem.views.auth.redirect') as mock_redirect, \
             patch('HelpDeskTicketingSystem.views.auth.url_for') as mock_url_for:

            mock_query.filter_by.return_value.first.return_value = None
            mock_url_for.return_value = '/'
            mock_redirect.return_value = 'redirected'

            result = register()

            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            mock_login.assert_called_once()
            mock_flash.assert_called_once_with('Account successfully created.', category='success')
            assert result == 'redirected'

# Test for registration form submission with validation errors

def test_register_post_with_errors(app):
    data = {
        'email': 'test@test.com',
        'forename': 'Test',
        'surname': 'User',
        'password': 'pass',
        'password_confirm': 'pass',
        'account_type': 'Regular User'
    }
    with app.test_request_context('/register', method='POST', data=data):
        with patch('flask_login.utils._get_user', return_value=None), \
             patch('HelpDeskTicketingSystem.views.auth.User.query') as mock_query, \
             patch('HelpDeskTicketingSystem.views.auth.validate_registration_form', return_value='Error message'), \
             patch('HelpDeskTicketingSystem.views.auth.flash') as mock_flash, \
             patch('HelpDeskTicketingSystem.views.auth.render_template') as mock_render_template:

            mock_query.filter_by.return_value.first.return_value = None
            mock_render_template.return_value = 'rendered'
            result = register()

            mock_flash.assert_called_once_with('Error message', category='error')
            mock_render_template.assert_called_once_with(
                "register.html",
                user=None,
                forename='Test',
                surname='User',
                email='test@test.com',
                account_type='Regular User'
            )
            assert result == 'rendered'

# Test for ensuring that administrator registration redirects to administrator verification code page            

def test_register_post_admin_redirects_to_admin_verification_code(app):
    data = {
        'email': 'admintestuser@test.com',
        'forename': 'Administrator',
        'surname': 'User',
        'password': 'password',
        'password_confirm': 'password',
        'account_type': 'Administrator'
    }
    with app.test_request_context('/register', method='POST', data=data):
        with patch('flask_login.utils._get_user', return_value=None), \
             patch('HelpDeskTicketingSystem.views.auth.User.query') as mock_query, \
             patch('HelpDeskTicketingSystem.views.auth.validate_registration_form', return_value=None), \
             patch('HelpDeskTicketingSystem.views.auth.redirect') as mock_redirect, \
             patch('HelpDeskTicketingSystem.views.auth.url_for') as mock_url_for:

            mock_query.filter_by.return_value.first.return_value = None
            mock_url_for.return_value = '/admin_code'
            mock_redirect.return_value = 'redirected'

            result = register()

            assert 'pending_user' in session
            assert result == 'redirected'

# Test for rendering the administrator verification code entry page on GET request

def test_admin_code_get(app):
    with app.test_request_context('/admin_code', method='GET'):
        with patch('HelpDeskTicketingSystem.views.auth.render_template') as mock_render:
            mock_render.return_value = 'rendered'
            assert admin_code() == 'rendered'

# Test for successfully submitting the correct administrator verification code and creating an administrator user

def test_admin_code_post_correct_code(app):
    with app.test_request_context('/admin_code', method='POST', data={'admin_code': '53c17e4d8efdafeddd375e53e4689cc757f1f322ef4595caedc3e85e2fb79c4e'}):
        session['pending_user'] = {
            'forename': 'Administrator',
            'surname': 'User',
            'email': 'admintestuser@test.com',
            'password': 'hashed_pw',
            'account_type': 'Administrator'
        }
        with patch('HelpDeskTicketingSystem.views.auth.User') as mock_user_class, \
             patch('HelpDeskTicketingSystem.views.auth.db.session.add') as mock_add, \
             patch('HelpDeskTicketingSystem.views.auth.db.session.commit') as mock_commit, \
             patch('HelpDeskTicketingSystem.views.auth.session.pop', wraps=session.pop) as mock_pop, \
             patch('HelpDeskTicketingSystem.views.auth.login_user') as mock_login, \
             patch('HelpDeskTicketingSystem.views.auth.flash') as mock_flash, \
             patch('HelpDeskTicketingSystem.views.auth.redirect') as mock_redirect, \
             patch('HelpDeskTicketingSystem.views.auth.url_for') as mock_url_for:

            mock_user_instance = MagicMock()
            mock_user_class.return_value = mock_user_instance
            mock_url_for.return_value = '/'
            mock_redirect.return_value = 'redirected'

            result = admin_code()

            mock_add.assert_called_once()
            mock_commit.assert_called_once()
            mock_pop.assert_called_once_with('pending_user', None)
            mock_login.assert_called_once()
            mock_flash.assert_called_once_with('Administrator account successfully created.', category='success')
            assert result == 'redirected'

# Test for submitting an incorrect administrator verification code and getting an error message

def test_admin_code_post_incorrect_code(app):
    client = app.test_client()
    with client.session_transaction() as sess:
        sess['pending_user'] = {
            'forename': 'Admin',
            'surname': 'User',
            'email': 'admin@test.com',
            'password': 'hashed_pw',
            'account_type': 'Administrator'
        }

    with patch('HelpDeskTicketingSystem.views.auth.flash') as mock_flash, \
         patch('HelpDeskTicketingSystem.views.auth.render_template') as mock_render:
        mock_render.return_value = 'rendered'

        response = client.post('/admin_code', data={'admin_code': 'wrong'})
        mock_flash.assert_called_once_with('Incorrect verification code. Please try again.', category='error')
        assert b'rendered' in response.data or response.data == b'rendered'

# Test for submitting administrator verification code without a pending session user 

def test_admin_code_post_no_pending_user(app):
    with app.test_request_context('/admin_code', method='POST', data={'admin_code': '53c17e4d8efdafeddd375e53e4689cc757f1f322ef4595caedc3e85e2fb79c4e'}):
        with patch('HelpDeskTicketingSystem.views.auth.flash') as mock_flash, \
             patch('HelpDeskTicketingSystem.views.auth.redirect') as mock_redirect, \
             patch('HelpDeskTicketingSystem.views.auth.url_for') as mock_url_for:

            mock_url_for.return_value = '/register'
            mock_redirect.return_value = 'redirected'

            result = admin_code()

            mock_flash.assert_called_once_with('Session expired. Please complete the registration form again.', category='error')
            assert result == 'redirected'