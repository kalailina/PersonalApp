"""
Integration tests for the London Environment app.
"""
import pytest
from environment_app.flask_app.models import Borough, Sector, Type, EnergyConsumption, GHGEmission, Feedback
from datetime import datetime

def test_feedback_submission_integration(client, app):
    """
    GIVEN a Flask application configured for testing
    WHEN a feedback form is submitted
    THEN check that the feedback is stored in the database
    """
    with app.app_context():
        db = app.extensions['sqlalchemy'].db
        
        # Get initial count of feedback entries
        initial_count = Feedback.query.count()
        
        # Submit a feedback form
        response = client.post(
            '/feedback',
            data={
                'name': 'Integration Test User',
                'email': 'integration@example.com',
                'message': 'This is an integration test for the feedback submission process.'
            },
            follow_redirects=True
        )
        
        # Check the response
        assert response.status_code == 200
        
        # Check the database
        new_count = Feedback.query.count()
        assert new_count == initial_count + 1
        
        # Check the specific feedback entry
        feedback = Feedback.query.filter_by(email='integration@example.com').first()
        assert feedback is not None
        assert feedback.name == 'Integration Test User'
        assert feedback.message == 'This is an integration test for the feedback submission process.'

def test_prediction_flow(client, app):
    """
    GIVEN a Flask application with test data
    WHEN the prediction form is submitted
    THEN check that predictions are made correctly
    """
    with app.app_context():
        db = app.extensions['sqlalchemy'].db
        
        # Set up test data
        test_borough = Borough(borough_id=501, borough_name="Prediction Test Borough")
        test_sector = Sector(sector_id=501, sector_name="Prediction Test Sector")
        test_type = Type(type_id=501, type_name="Prediction Test Type")
        db.session.add_all([test_borough, test_sector, test_type])
        db.session.commit()
        
        # Add consumption and emission data for multiple years
        years = [2018, 2019, 2020]
        consumption_values = [100, 110, 120]
        emission_values = [50, 55, 60]
        
        for i, year in enumerate(years):
            consumption = EnergyConsumption(
                borough_id=501,
                sector_id=501,
                type_id=501,
                year=year,
                consumption=consumption_values[i]
            )
            emission = GHGEmission(
                borough_id=501,
                sector_id=501,
                type_id=501,
                year=year,
                emission=emission_values[i]
            )
            db.session.add_all([consumption, emission])
        db.session.commit()
        
        # Submit a prediction request
        response = client.post(
            '/prediction',
            data={
                'borough': 501,  # Specific borough
                'sector': 501,   # Specific sector
                'year': 2025
            },
            follow_redirects=True
        )
        
        # Check the response
        assert response.status_code == 200
        assert b'Prediction Results' in response.data
        assert b'Prediction Test Borough' in response.data
        assert b'Prediction Test Sector' in response.data
        assert b'2025' in response.data
        
        # Basic check for prediction results
        # We can't check exact values, but we can check for the explanation
        assert b'Based on historical data' in response.data

def test_dashboard_data_flow(client, app):
    """
    GIVEN a Flask application with test data
    WHEN the dashboard page is loaded with filters
    THEN check that the appropriate data is returned
    """
    with app.app_context():
        db = app.extensions['sqlalchemy'].db
        
        # Set up test data for the dashboard
        test_borough = Borough(borough_id=601, borough_name="Dashboard Test Borough")
        test_sector = Sector(sector_id=601, sector_name="Dashboard Test Sector")
        test_type = Type(type_id=601, type_name="Dashboard Test Type")
        db.session.add_all([test_borough, test_sector, test_type])
        db.session.commit()
        
        # Add consumption and emission data
        consumption = EnergyConsumption(
            borough_id=601,
            sector_id=601,
            type_id=601,
            year=2020,
            consumption=150.0
        )
        emission = GHGEmission(
            borough_id=601,
            sector_id=601,
            type_id=601,
            year=2020,
            emission=75.0
        )
        db.session.add_all([consumption, emission])
        db.session.commit()
        
        # Access the dashboard with filters
        response = client.get('/dashboard?year=2020&borough=Dashboard+Test+Borough')
        
        # Check the response
        assert response.status_code == 200
        assert b'Environmental Data Dashboard' in response.data
        
        # Since we're not checking the actual chart content (which is generated by plotly),
        # we just check that the response includes chart tags
        assert b'<div class="js-plotly-plot"' in response.data

def test_app_configuration(app):
    """
    GIVEN a Flask application
    WHEN the app is configured
    THEN check the configuration settings
    """
    # Check the basic configuration
    assert app.config['TESTING'] is True
    assert app.config['WTF_CSRF_ENABLED'] is False
    assert 'sqlite:///' in app.config['SQLALCHEMY_DATABASE_URI']
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False

def test_database_connections(app):
    """
    GIVEN a Flask application
    WHEN the database is initialized
    THEN check that database connections work
    """
    with app.app_context():
        db = app.extensions['sqlalchemy'].db
        
        # Check that the database engine is properly set up
        assert db.engine is not None
        
        # Check that we can query the database
        result = db.session.execute("SELECT 1").scalar()
        assert result == 1
        
        # Check that we can create and query tables
        test_data = Borough(borough_id=999, borough_name="DB Connection Test")
        db.session.add(test_data)
        db.session.commit()
        
        queried_data = Borough.query.get(999)
        assert queried_data is not None
        assert queried_data.borough_name == "DB Connection Test"