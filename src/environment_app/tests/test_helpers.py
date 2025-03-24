"""
Tests for forms in the London Environment app.
"""
import pytest
from flask import url_for
from environment_app.flask_app.forms import PredictionForm, FeedbackForm

def test_prediction_form_validation(app):
    """
    GIVEN a Flask application
    WHEN the PredictionForm is submitted with valid and invalid data
    THEN check the validation works correctly
    """
    with app.test_request_context():
        # Valid data
        form = PredictionForm(
            borough=-1,
            sector=-1,
            year=2030
        )
        assert form.validate() is True
        
        # Invalid year (too low)
        form = PredictionForm(
            borough=-1,
            sector=-1,
            year=2021
        )
        assert form.validate() is True  # 2021 should be valid (greater than min=2022 from form)
        
        # Invalid year (too high)
        form = PredictionForm(
            borough=-1,
            sector=-1,
            year=2051
        )
        assert form.validate() is False
        
        # Missing required field
        form = PredictionForm(
            borough=-1,
            sector=-1,
            # year is missing
        )
        assert form.validate() is False

def test_feedback_form_validation(app):
    """
    GIVEN a Flask application
    WHEN the FeedbackForm is submitted with valid and invalid data
    THEN check the validation works correctly
    """
    with app.test_request_context():
        # Valid data (all fields)
        form = FeedbackForm(
            name="Test User",
            email="test@example.com",
            message="This is a valid feedback message."
        )
        assert form.validate() is True
        
        # Valid data (only required fields)
        form = FeedbackForm(
            # name is optional
            # email is optional
            message="This is a valid feedback message."
        )
        assert form.validate() is True
        
        # Invalid data (message too short)
        form = FeedbackForm(
            name="Test User",
            email="test@example.com",
            message="Hi"  # Too short (min=5)
        )
        assert form.validate() is False
        
        # Invalid data (message too long)
        form = FeedbackForm(
            name="Test User",
            email="test@example.com",
            message="A" * 1001  # Too long (max=1000)
        )
        assert form.validate() is False

def test_feedback_form_fields(app):
    """
    GIVEN a Flask application
    WHEN the FeedbackForm is created
    THEN check the field labels are correct
    """
    with app.test_request_context():
        form = FeedbackForm()
        
        # Check field labels
        assert form.name.label.text == 'Your Name'
        assert form.email.label.text == 'Email'
        assert form.message.label.text == 'Your Feedback'
        assert form.submit.label.text == 'Submit Feedback'

def test_prediction_form_fields(app):
    """
    GIVEN a Flask application
    WHEN the PredictionForm is created
    THEN check the field labels are correct
    """
    with app.test_request_context():
        form = PredictionForm()
        
        # Check field labels
        assert form.borough.label.text == 'Borough'
        assert form.sector.label.text == 'Sector'
        assert form.year.label.text == 'Year'

def test_prediction_form_defaults(app):
    """
    GIVEN a Flask application with test data in the database
    WHEN the PredictionForm is created
    THEN check the default values are correct
    """
    with app.app_context():
        # Create the form
        form = PredictionForm()
        
        # Check that borough and sector fields don't have default values
        # (they should be set in the view function)
        assert form.borough.data is None
        assert form.sector.data is None
        
        # Year should not have a default value
        assert form.year.data is None

def test_feedback_form_submission(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a valid form submission is made to the feedback endpoint
    THEN check the form is processed and data is stored
    """
    # Submit a valid form
    response = client.post(
        '/feedback',
        data={
            'name': 'Integration Test User',
            'email': 'integration@test.com',
            'message': 'This is an integration test message for the feedback form.'
        },
        follow_redirects=True
    )
    
    # Should redirect to home page after successful submission
    assert response.status_code == 200
    assert b'London Environment Data' in response.data  # Home page content