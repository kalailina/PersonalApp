"""
Minimal conftest.py file for testing the Flask app.
"""
import os
import sys
import pytest
from flask import Flask

# Add the project root to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

@pytest.fixture
def app():
    """Create a test Flask application."""
    # Create a minimal Flask app for testing
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
    })
    
    # Add routes for testing
    @app.route('/')
    def index():
        return "Home Page"
    
    @app.route('/dashboard')
    def dashboard():
        return "Dashboard Page"
    
    @app.route('/prediction', methods=['GET', 'POST'])
    def prediction():
        return "Prediction Page"
    
    @app.route('/feedback', methods=['GET', 'POST'])
    def feedback():
        return "Feedback Page"
    
    return app

@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()