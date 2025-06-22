from unittest.mock import patch, MagicMock

# This test verifies that the profile view renders the profile page correctly for an authenticated user.
# It uses patching to mock the current user retrieval and template rendering, allowing the route logic
# to be tested without a full application context or actual user data.

# Test for ensuring that the profile page renders correctly for an authenticated user.

def test_profile_view(app):
    with app.test_request_context('/profile'):
        mocked_user = MagicMock(is_authenticated=True)
        with patch('flask_login.utils._get_user', return_value=mocked_user), \
             patch('HelpDeskTicketingSystem.views.users.render_template') as mock_render:
            
            mock_render.return_value = 'rendered'
            from HelpDeskTicketingSystem.views.users import profile
            result = profile()

            mock_render.assert_called_once_with('profile.html', user=mocked_user)
            assert result == 'rendered'