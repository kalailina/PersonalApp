"""
Simple tests for Flask routes in the London Environment app.
"""
import pytest

def test_index_route(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/')
    assert response.status_code == 200

def test_dashboard_route(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/dashboard' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/dashboard')
    assert response.status_code == 200

def test_prediction_route(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/prediction' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/prediction')
    assert response.status_code == 200

def test_feedback_route(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/feedback' page is requested (GET)
    THEN check that the response is valid
    """
    response = client.get('/feedback')
    assert response.status_code == 200

def test_index_post_not_allowed(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (POST)
    THEN check that the response is 405 Method Not Allowed
    """
    response = client.post('/')
    assert response.status_code == 405

def test_dashboard_post_not_allowed(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/dashboard' page is requested (POST)
    THEN check that the response is 405 Method Not Allowed
    """
    response = client.post('/dashboard')
    assert response.status_code == 405