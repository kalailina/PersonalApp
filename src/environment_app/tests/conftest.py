import os
import sys
import pytest
import tempfile

# Add the src directory to Python's path to help with imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

@pytest.fixture(scope='session')
def app():
    """Create a Flask application configured for testing."""
    # Import the create_app function 
    from environment_app import create_app
    
    # Create a temporary file for the test database in the tests directory
    test_dir = os.path.dirname(os.path.abspath(__file__))
    db_fd, db_path = tempfile.mkstemp(suffix='.sqlite', dir=test_dir)
    
    # Configuration for testing
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "WTF_CSRF_ENABLED": False,
    }
    
    # Create app with test configuration
    app = create_app(test_config)

    # Create test database tables
    with app.app_context():
        from environment_app.flask_app import db
        db.create_all()

        # Populate with initial data if needed
        from environment_app.flask_app.models import Borough, Sector, Type
        
        # Add some sample boroughs if not exists
        if not Borough.query.first():
            sample_boroughs = [
                Borough(borough_name=f"Borough {i}") 
                for i in range(1, 5)
            ]
            db.session.add_all(sample_boroughs)
        
        # Add some sample sectors if not exists
        if not Sector.query.first():
            sample_sectors = [
                Sector(sector_name=f"Sector {i}") 
                for i in range(1, 4)
            ]
            db.session.add_all(sample_sectors)
        
        db.session.commit()

    yield app

    # Clean up resources
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture()
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """Create a CLI test runner for the Flask application."""
    return app.test_cli_runner()

@pytest.fixture(scope='function')
def db_session(app):
    """Creates a new database session for a test."""
    with app.app_context():
        from environment_app.flask_app import db
        
        # Create a new session
        connection = db.engine.connect()
        transaction = connection.begin()
        session = db.session
        
        yield session
        
        # Clean up
        transaction.rollback()
        connection.close()