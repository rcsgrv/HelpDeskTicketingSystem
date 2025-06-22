import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from HelpDeskTicketingSystem import create_app
from HelpDeskTicketingSystem.extensions import db
from tests.test_config import TestConfig
from unittest.mock import MagicMock

# This Pytest fixture sets up and tears down the Flask application for testing purposes

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

# This Pytest fixture provides a test client for sending requests to the application

@pytest.fixture
def client(app):
    return app.test_client()