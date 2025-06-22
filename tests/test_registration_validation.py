import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from HelpDeskTicketingSystem.utils.registration_helper import validate_registration_form
from email_validator import EmailNotValidError

# Tests for verifying the validation in registration_helper

# Forename Validation

@pytest.mark.parametrize("forename", ["", " ", None])
def test_forename_blank(forename):
    result = validate_registration_form(forename, "User", "testuser@test.com", "password", "password", "Regular User", None)
    assert result == "Forename cannot be blank."

def test_forename_length():
    long_name = "A" * 51
    result = validate_registration_form(long_name, "User", "testuser@test.com", "password", "password", "Regular User", None)
    assert result == "Forename cannot exceed 50 characters."

# Surname Validation

@pytest.mark.parametrize("surname", ["", " ", None])
def test_surname_blank(surname):
    result = validate_registration_form("Test", surname, "testuser@test.com", "password", "password", "Regular User", None)
    assert result == "Surname cannot be blank."

def test_surname_too_long():
    long_name = "A" * 51
    result = validate_registration_form("Test", long_name, "testuser@test.com", "password", "password", "Regular User", None)
    assert result == "Surname cannot exceed 50 characters."

# Email Validation

@pytest.mark.parametrize("email", ["", " ", None])
def test_email_blank(email):
    result = validate_registration_form("Test", "User", email, "password", "password", "Regular User", None)
    assert result == "Email cannot be blank."

def test_email_invalid():
    result = validate_registration_form("Test", "User", "invalid-email", "password", "password", "Regular User", None)
    assert "An email address must have an @-sign." in result 

def test_email_already_exists():
    result = validate_registration_form("Test", "User", "testuser@test.com", "password", "password", "Regular User", user="mock-user")
    assert result == "The email you have provided is already associated with an account."

# Password Validation

def test_password_too_short():
    result = validate_registration_form("Test", "User", "testuser@test.com", "pass", "pass", "Regular User", None)
    assert result == "Password must be at least 8 characters long."

def test_password_too_long():
    result = validate_registration_form("Test", "User", "testuser@test.com", "x" * 21, "x" * 21, "Regular User", None)
    assert result == "Password cannot exceed 20 characters."

def test_passwords_do_not_match():
    result = validate_registration_form("Test", "User", "testuser@test.com", "password", "password321", "Regular User", None)
    assert result == "Your passwords do not match."

# Account Type Validation

def test_account_type_blank():
    result = validate_registration_form("Test", "User", "testuser@test.com", "password", "password", "", None)
    assert result == "You must select an account type."

def test_account_type_invalid():
    result = validate_registration_form("Test", "User", "testuser@test.com", "password", "password", "Admin", None)
    assert result == "Invalid account type selected."

# Successful Case

def test_valid_registration_data():
    result = validate_registration_form("Test", "User", "testuser@test.com", "password", "password", "Regular User", None)
    assert result is None