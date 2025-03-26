# Import the create_app function from flask_app
from .flask_app import create_app, db

# Export the function and db
__all__ = ['create_app', 'db']