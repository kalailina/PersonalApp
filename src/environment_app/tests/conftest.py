import pytest
import sys
import os

# Add the project directory to the path so imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

@pytest.fixture
def client():
    """Create a test client for simple route testing without database access.
    
    This fixture specifically avoids using database-related functionality
    to prevent SQLAlchemy conflicts.
    """
    # Import create_app inside the fixture to avoid importing models globally
    from environment_app.flask_app import create_app
    
    # Configure the app for testing
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })
    
    # Create a test client
    with app.test_client() as test_client:
        yield test_client