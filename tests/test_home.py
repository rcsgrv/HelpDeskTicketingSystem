import pytest
from unittest.mock import patch, MagicMock
from HelpDeskTicketingSystem.views.home import home

# These tests validate the home view's behaviour for different user roles by mocking the current user,
# database queries, and template rendering. Patching is used to simulate pagination and query filtering
# so the tests focus on verifying that the correct tickets and user context are passed to the template
# depending on whether the user is an Administrator or a Regular User.

@pytest.fixture
def mock_pagination():
    mock_paginate = MagicMock()
    mock_paginate.items = ['ticket_1', 'ticket_2']
    return mock_paginate

# Test that an Administrator user sees all tickets with pagination

def test_home_admin_user(app, mock_pagination):
    with app.test_request_context('/?page=1&per_page=5'):
        mock_user = MagicMock(account_type='Administrator')

        with patch('flask_login.utils._get_user', return_value=mock_user), \
             patch('HelpDeskTicketingSystem.views.home.Ticket') as mock_ticket, \
             patch('HelpDeskTicketingSystem.views.home.render_template') as mock_render_template:

            mock_ticket.query.order_by.return_value.paginate.return_value = mock_pagination

            result = home()

            mock_render_template.assert_called_once_with(
                "home.html",
                user=mock_user,
                tickets=mock_pagination,
                per_page=5
            )
            assert result == mock_render_template.return_value

# Test that a Regular User only sees their own tickets with pagination

def test_home_regular_user(app, mock_pagination):
    with app.test_request_context('/?page=1&per_page=5'):
        mock_user = MagicMock(account_type='Regular User', id=42)

        with patch('flask_login.utils._get_user', return_value=mock_user), \
             patch('HelpDeskTicketingSystem.views.home.Ticket') as mock_ticket, \
             patch('HelpDeskTicketingSystem.views.home.render_template') as mock_render_template:

            mock_ticket.query.filter_by.return_value.order_by.return_value.paginate.return_value = mock_pagination

            result = home()

            mock_ticket.query.filter_by.assert_called_once_with(user_id=42)
            mock_ticket.query.filter_by.return_value.order_by.assert_called_once()
            mock_ticket.query.filter_by.return_value.order_by.return_value.paginate.assert_called_once_with(page=1, per_page=5)

            mock_render_template.assert_called_once_with(
                "home.html",
                user=mock_user,
                tickets=mock_pagination,
                per_page=5
            )
            assert result == mock_render_template.return_value