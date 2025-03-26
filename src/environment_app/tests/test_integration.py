"""
Integration tests for the environment application.
"""
import pytest
from environment_app import create_app, db
from environment_app.flask_app.models import Borough, Sector, EnergyConsumption, GHGEmission

@pytest.fixture
def app_context():
    """Create an application context for testing."""
    app = create_app()
    with app.app_context():
        yield app

def test_database_model_relationships(app_context):
    """
    Test database model relationships.
    
    Verify:
    1. Borough can be linked to Energy Consumption
    2. Borough can be linked to GHG Emissions
    3. Sector can be linked to Energy Consumption
    4. Sector can be linked to GHG Emissions
    """
    # Get a sample borough
    borough = Borough.query.first()
    assert borough is not None, "No boroughs found in the database"

    # Check energy consumption relationship
    energy_consumptions = borough.energy_consumptions
    assert len(energy_consumptions) > 0, "No energy consumptions found for the borough"
    
    # Verify each energy consumption is linked to the borough
    for consumption in energy_consumptions:
        assert consumption.borough == borough

    # Check GHG emissions relationship
    ghg_emissions = borough.ghg_emissions
    assert len(ghg_emissions) > 0, "No GHG emissions found for the borough"
    
    # Verify each emission is linked to the borough
    for emission in ghg_emissions:
        assert emission.borough == borough

def test_data_consistency(app_context):
    """
    Test data consistency across different models.
    
    Verify:
    1. Years in Energy Consumption match years in GHG Emissions
    2. Boroughs and Sectors are consistent across models
    """
    # Get unique years from Energy Consumption
    energy_years = set(db.session.query(EnergyConsumption.year).distinct())
    
    # Get unique years from GHG Emissions
    emission_years = set(db.session.query(GHGEmission.year).distinct())
    
    # Check that years are consistent
    assert len(energy_years.symmetric_difference(emission_years)) <= 1, \
        "Significant difference in years between Energy Consumption and GHG Emissions"

def test_data_volume_and_range(app_context):
    """
    Test the volume and range of data in the database.
    
    Verify:
    1. Sufficient number of records
    2. Data values are within expected ranges
    """
    # Check record counts
    borough_count = Borough.query.count()
    sector_count = Sector.query.count()
    energy_consumption_count = EnergyConsumption.query.count()
    ghg_emission_count = GHGEmission.query.count()

    # Assert minimum record counts
    assert borough_count > 0, "No boroughs in the database"
    assert sector_count > 0, "No sectors in the database"
    assert energy_consumption_count > 100, "Too few energy consumption records"
    assert ghg_emission_count > 100, "Too few GHG emission records"

    # Sample some data to check ranges
    sample_consumption = EnergyConsumption.query.first()
    sample_emission = GHGEmission.query.first()

    # Check year ranges
    assert 2000 <= sample_consumption.year <= 2050, "Consumption year out of expected range"
    assert 2000 <= sample_emission.year <= 2050, "Emission year out of expected range"

    # Check consumption and emission values
    assert sample_consumption.consumption >= 0, "Negative energy consumption"
    assert sample_emission.emission >= 0, "Negative GHG emission"