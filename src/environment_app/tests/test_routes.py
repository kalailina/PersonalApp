"""
Tests for all Flask routes in the London Environment app.
"""
import pytest

# ----- HOME PAGE TESTS -----

def test_index_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that a '200' status code is returned and expected content is in the response
    """
    response = client.get('/')
    
    assert response.status_code == 200
    assert b'London Environment Data' in response.data
    assert b'Interactive Dashboard' in response.data
    assert b'Predictive Analytics' in response.data

def test_index_method_not_allowed(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested with an unsupported HTTP method (POST)
    THEN check that a '405' status code is returned
    """
    response = client.post('/')
    assert response.status_code == 405  # Method Not Allowed

# ----- DASHBOARD TESTS -----

def test_dashboard_get_no_parameters(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/dashboard' page is requested (GET) with no query parameters
    THEN check that a '200' status code is returned and expected content is in the response
    """
    response = client.get('/dashboard')
    
    assert response.status_code == 200
    assert b'Environmental Data Dashboard' in response.data
    assert b'Filter Options' in response.data

def test_dashboard_method_not_allowed(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/dashboard' page is requested with an unsupported HTTP method (POST)
    THEN check that a '405' status code is returned
    """
    response = client.post('/dashboard')
    assert response.status_code == 405  # Method Not Allowed

# ----- PREDICTION TESTS -----

def test_prediction_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/prediction' page is requested (GET)
    THEN check that a '200' status code is returned and expected content is in the response
    """
    response = client.get('/prediction')
    
    assert response.status_code == 200
    assert b'Predict Future Energy Consumption &amp; Emissions' in response.data
    assert b'Prediction Form' in response.data
    assert b'Borough' in response.data
    assert b'Year' in response.data

# ----- FEEDBACK TESTS -----

def test_feedback_get(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/feedback' page is requested (GET)
    THEN check that a '200' status code is returned and feedback form is in the response
    """
    response = client.get('/feedback')
    
    assert response.status_code == 200
    assert b'We Value Your Feedback' in response.data
    assert b'Your Name' in response.data
    assert b'Email' in response.data
    assert b'Your Feedback' in response.data

def test_feedback_post_valid(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request with valid form data is submitted to '/feedback'
    THEN check that the form is processed and the user is redirected
    """
    response = client.post(
        '/feedback',
        data={
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test feedback message that meets the length requirements.'
        },
        follow_redirects=True
    )
    
    # Should redirect to home page after successful submission
    assert response.status_code == 200
    assert b'London Environment Data' in response.data  # Home page content

def test_feedback_post_invalid(client):
    """
    GIVEN a Flask application configured for testing
    WHEN a POST request with invalid form data is submitted to '/feedback'
    THEN check that the form is displayed again with error messages
    """
    response = client.post(
        '/feedback',
        data={
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Short'  # Too short message (requirements: 5-1000 chars)
        }
    )
    
    assert response.status_code == 200
    assert b'We Value Your Feedback' in response.data
    assert b'Feedback must be between 5 and 1000 characters' in response.data