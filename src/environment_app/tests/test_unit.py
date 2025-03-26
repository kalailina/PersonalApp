"""
Unit tests for helper functions in the environment application.
"""
import pytest
import pandas as pd
from environment_app.flask_app.helpers import (
    make_energy_prediction,
    make_emission_prediction,
    get_available_years
)
from environment_app import create_app, db

@pytest.fixture
def app_context():
    """Create an application context for testing."""
    app = create_app()
    with app.app_context():
        yield app

def test_make_energy_prediction_all_boroughs(app_context):
    """
    Test energy prediction for all boroughs.
    
    Verify:
    1. Prediction is calculated
    2. Explanation is provided
    3. Prediction is non-negative
    """
    prediction, explanation = make_energy_prediction(-1, -1, 2030)
    
    assert prediction is not None
    assert isinstance(prediction, (int, float))
    assert prediction >= 0
    assert isinstance(explanation, str)
    assert "Based on historical data" in explanation

def test_make_emission_prediction_all_boroughs(app_context):
    """
    Test emission prediction for all boroughs.
    
    Verify:
    1. Prediction is calculated
    2. Explanation is provided
    3. Prediction is non-negative
    """
    prediction, explanation = make_emission_prediction(-1, -1, 2030)
    
    assert prediction is not None
    assert isinstance(prediction, (int, float))
    assert prediction >= 0
    assert isinstance(explanation, str)
    assert "Based on historical data" in explanation

def test_get_available_years(app_context):
    """
    Test retrieval of available years.
    
    Verify:
    1. Years are returned
    2. Years are integers
    3. Years are in a reasonable range
    """
    years = get_available_years()
    
    assert isinstance(years, list)
    assert len(years) > 0
    assert all(isinstance(year, int) for year in years)
    
    # Check years are in a reasonable range
    min_year = min(years)
    max_year = max(years)
    assert min_year >= 2000
    assert max_year <= 2050

def test_prediction_with_specific_borough(app_context):
    """
    Test prediction for a specific borough.
    
    Verify prediction works with a specific borough ID.
    """
    # Assuming borough_id 1 exists
    prediction, explanation = make_energy_prediction(1, -1, 2030)
    
    assert prediction is not None
    assert isinstance(prediction, (int, float))
    assert prediction >= 0

def test_prediction_with_specific_sector(app_context):
    """
    Test prediction for a specific sector.
    
    Verify prediction works with a specific sector ID.
    """
    # Assuming sector_id 1 exists
    prediction, explanation = make_emission_prediction(-1, 1, 2030)
    
    assert prediction is not None
    assert isinstance(prediction, (int, float))
    assert prediction >= 0

def test_prediction_invalid_year(app_context):
    """
    Test prediction with an invalid year.
    
    Verify graceful handling of prediction for an unreasonable future year.
    """
    # Far future year
    prediction, explanation = make_energy_prediction(-1, -1, 2100)
    
    # Should still return a prediction
    assert prediction is not None
    assert isinstance(prediction, (int, float))
    assert prediction >= 0
    assert "Based on historical data" in explanation