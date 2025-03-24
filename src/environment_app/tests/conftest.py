import os
import sys
import pytest

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

@pytest.fixture()
def app():
    """Create a Flask application configured for testing."""
    from environment_app.flask_app import create_app
    
    app = create_app()
    
    # Location for the temporary testing database
    db_path = os.path.join(os.path.dirname(__file__), "test_environment.sqlite")
    db_path_str = str(db_path)

    # Update the app config for testing
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_path_str,
        "WTF_CSRF_ENABLED": False,
    })

    # Other setup can go here
    with app.app_context():
        from environment_app.flask_app import db
        db.create_all()  # Create test database tables

    yield app

    # Clean up / reset resources here
    with app.app_context():
        from environment_app.flask_app import db
        db.drop_all()  # Clean up after tests
    
    # Remove the test database file if it exists
    if os.path.exists(db_path):
        os.unlink(db_path)

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
    """Creates a new database session for a test.
    
    Creates a new database session for each test function.
    Begins a transaction before each test and rolls it back afterward to ensure no changes persist between tests.
    """
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