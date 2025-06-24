import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from HelpDeskTicketingSystem.utils.ticket_helper import validate_ticket_form

# Tests for verifying the validation in ticket_helper

# Subject Validation

@pytest.mark.parametrize("subject", ["", " ", None])
def test_subject_blank(subject):
    result = validate_ticket_form(subject, "Valid description", "Open", "High", 2)
    assert result == "Subject cannot be blank."

def test_subject_too_long():
    long_subject = "A" * 101
    result = validate_ticket_form(long_subject, "Valid description", "Open", "High", 2)
    assert result == "Subject must not exceed 100 characters."

# Description Validation

@pytest.mark.parametrize("description", ["", " ", None])
def test_description_blank(description):
    result = validate_ticket_form("Valid subject", description, "Open", "High", 2)
    assert result == "Description cannot be blank."

def test_description_too_long():
    long_description = "A" * 501
    result = validate_ticket_form("Valid subject", long_description, "Open", "High", 2)
    assert result == "Description must not exceed 500 characters."

# Priority Validation

def test_priority_blank():
    result = validate_ticket_form("Valid subject", "Valid description", "Open", "", 2)
    assert result == "You must select a priority."

# Status Validation

def test_status_blank():
    result = validate_ticket_form("Valid subject", "Valid description", "", "High", 2)
    assert result == "You must select a status."

# Estimated Time Validation

@pytest.mark.parametrize("estimated_time", [0.5, 41, "abc", None])
def test_estimated_time_invalid(estimated_time):
    expected_messages = {
        0.5: "Estimated time cannot be less than 1 hour.",
        41: "Estimated time cannot be more than 40 hours.",
        "abc": "Estimated time must be a number.",
        None: "Estimated time must be a number.",
    }
    result = validate_ticket_form("Valid subject", "Valid description", "Open", "High", estimated_time)
    assert result == expected_messages[estimated_time]

# Successful Case

def test_valid_ticket_data():
    result = validate_ticket_form("Valid subject", "Valid description", "Closed", "Medium", 5)
    assert result is None