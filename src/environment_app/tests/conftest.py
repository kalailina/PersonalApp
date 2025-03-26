import os
import sys
import pytest

# Add the src directory to Python's path to help with imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

@pytest.fixture()
def app():
    """Create a Flask application configured for testing."""
    # Import the create_app function 
    from environment_app.flask_app import create_app
    
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test_environment.sqlite",
        "WTF_CSRF_ENABLED": False,
    })

    # Create test database tables
    with app.app_context():
        from environment_app.flask_app import db
        db.create_all()

    yield app

    # Clean up / reset resources
    with app.app_context():
        db.drop_all()

@pytest.fixture()
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()

@pytest.fixture()
def runner(app):
    """Create a CLI test runner for the Flask application."""
    return app.test_cli_runner()

@pytest.fixture(scope='function', autouse=True)
def db_session(app):
    """Creates a new database session for a test."""
    with app.app_context():
        from environment_app.flask_app import db
        connection = db.engine.connect()
        
        # Begin a non-ORM transaction
        transaction = connection.begin()
        
        # Create a session bound to the connection
        from sqlalchemy.orm import Session
        db_session = Session(bind=connection)
        
        # Replace the session in the app context
        old_session = db.session
        db.session = db_session
        
        yield db_session
        
        # Clean up
        db_session.close()
        transaction.rollback()
        connection.close()
        db.session = old_session