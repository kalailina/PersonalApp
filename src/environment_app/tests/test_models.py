# test_models.py

def test_borough_model(app):
    """
    GIVEN a Flask app context
    WHEN a new Borough object is created
    THEN check its attributes
    """
    with app.app_context():
        from src.environment_app.flask_app.models import Borough
        
        # Test creating a new Borough instance
        borough = Borough(borough_id=999, borough_name="Test Borough")
        assert borough.borough_id == 999
        assert borough.borough_name == "Test Borough"

def test_sector_model(app):
    """
    GIVEN a Flask app context
    WHEN a new Sector object is created
    THEN check its attributes
    """
    with app.app_context():
        from src.environment_app.flask_app.models import Sector
        
        # Test creating a new Sector instance
        sector = Sector(sector_id=999, sector_name="Test Sector")
        assert sector.sector_id == 999
        assert sector.sector_name == "Test Sector"

def test_feedback_model(app):
    """
    GIVEN a Flask app context
    WHEN a new Feedback object is created
    THEN check its attributes
    """
    with app.app_context():
        from src.environment_app.flask_app.models import Feedback
        
        # Test creating a new Feedback instance
        feedback = Feedback(
            name="Test User",
            email="test@example.com",
            message="This is a test message",
            submitted_at="2025-03-23 12:00:00"
        )
        
        # Check attributes
        assert feedback.name == "Test User"
        assert feedback.email == "test@example.com"
        assert feedback.message == "This is a test message"
        assert feedback.submitted_at == "2025-03-23 12:00:00"

def test_energy_consumption_model(app):
    """
    GIVEN a Flask app context
    WHEN a new EnergyConsumption object is created
    THEN check its attributes
    """
    with app.app_context():
        from src.environment_app.flask_app.models import EnergyConsumption
        
        # Test creating a new EnergyConsumption instance
        consumption = EnergyConsumption(
            consumption_id=999,
            borough_id=1,
            sector_id=1,
            type_id=1,
            year=2020,
            consumption=100.5
        )
        
        # Check attributes
        assert consumption.consumption_id == 999
        assert consumption.borough_id == 1
        assert consumption.sector_id == 1
        assert consumption.type_id == 1
        assert consumption.year == 2020
        assert consumption.consumption == 100.5