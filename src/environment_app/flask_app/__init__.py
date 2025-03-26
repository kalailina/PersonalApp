import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Explicitly set the absolute path to the database
DB_PATH = "/Users/linakalai/Desktop/UCL/PersonalApp/src/environment_app/instance/environment.db"

# Create a SQLAlchemy object
db = SQLAlchemy()

def create_app(test_config=None):
    """Create and configure the Flask application."""
    # Determine the base directory for the instance folder
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    app = Flask(__name__, 
                instance_path=os.path.join(base_dir, '..', 'instance'),
                instance_relative_config=True)
    
    # Validate database path
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file not found at {DB_PATH}")
    
    # Configure the app with full absolute path
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{DB_PATH}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # If test config is provided, update the configuration
    if test_config is not None:
        app.config.update(test_config)
    else:
        # Optionally load config from a file if it exists
        app.config.from_pyfile('config.py', silent=True)

    # Initialize the database
    db.init_app(app)

    # Create application context
    with app.app_context():
        # Import models to ensure they are known to SQLAlchemy
        from . import models
        
        # Import routes
        from .routes import main
        app.register_blueprint(main)

    return app