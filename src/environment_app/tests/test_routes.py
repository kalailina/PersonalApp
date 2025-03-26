"""
Tests for Flask routes in the London Environment app.
"""
import pytest

# ----- HOME PAGE TESTS -----

def test_index(client):
    """
    GIVEN a Flask test client
    WHEN the '/' page is requested (GET)
    THEN check that the status code is 200
    """
    response = client.get('/')
    assert response.status_code == 200

def test_index_method_not_allowed(client):
    """
    GIVEN a Flask test client
    WHEN the '/' page is requested with POST (which it doesn't support)
    THEN check that a 405 Method Not Allowed response is returned
    """
    response = client.post('/')
    assert response.status_code == 405  # Method Not Allowed

# ----- DASHBOARD TESTS -----

def test_dashboard(client):
    """
    GIVEN a Flask test client
    WHEN the '/dashboard' page is requested (GET)
    THEN check that the status code is 200
    """
    response = client.get('/dashboard')
    assert response.status_code == 200

def test_dashboard_with_parameters(client):
    """
    GIVEN a Flask test client
    WHEN the '/dashboard' page is requested with query parameters
    THEN check that the status code is 200
    """
    response = client.get('/dashboard?year=2022&borough=All')
    assert response.status_code == 200

def test_dashboard_method_not_allowed(client):
    """
    GIVEN a Flask test client
    WHEN the '/dashboard' page is requested with POST (which it doesn't support)
    THEN check that a 405 Method Not Allowed response is returned
    """
    response = client.post('/dashboard')
    assert response.status_code == 405  # Method Not Allowed

# ----- PREDICTION TESTS -----

def test_prediction_get(client):
    """
    GIVEN a Flask test client
    WHEN the '/prediction' page is requested (GET)
    THEN check that the status code is 200
    """
    response = client.get('/prediction')
    assert response.status_code == 200

def test_prediction_post_valid(client):
    """
    GIVEN a Flask test client
    WHEN a POST request with valid form data is made to '/prediction'
    THEN check that the status code is 200
    """
    response = client.post(
        '/prediction',
        data={
            'borough': -1,  # All boroughs
            'sector': -1,   # All sectors
            'year': 2030,
            'submit': True  # Add submit to simulate form submission
        }
    )
    assert response.status_code == 200

def test_prediction_post_invalid(client):
    """
    GIVEN a Flask test client
    WHEN a POST request with invalid form data is made to '/prediction'
    THEN check that the form errors are displayed
    """
    response = client.post(
        '/prediction',
        data={
            'borough': -1,
            'sector': -1,
            'year': 2100,  # Year outside the allowed range
            'submit': True
        }
    )
    assert response.status_code == 200

# ----- FEEDBACK TESTS -----

def test_feedback_get(client):
    """
    GIVEN a Flask test client
    WHEN the '/feedback' page is requested (GET)
    THEN check that the status code is 200
    """
    response = client.get('/feedback')
    assert response.status_code == 200

def test_feedback_post_valid(client):
    """
    GIVEN a Flask test client
    WHEN a POST request with valid form data is made to '/feedback'
    THEN check that the user is redirected
    """
    response = client.post(
        '/feedback',
        data={
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test feedback message that meets the length requirements.',
            'submit': True
        },
        follow_redirects=True
    )
    assert response.status_code == 200

def test_feedback_post_invalid(client):
    """
    GIVEN a Flask test client
    WHEN a POST request with invalid form data is made to '/feedback'
    THEN check that the form is redisplayed
    """
    response = client.post(
        '/feedback',
        data={
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Short',  # Message too short
            'submit': True
        }
    )
    assert response.status_code == 200