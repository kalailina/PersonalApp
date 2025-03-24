import sys
import os

# Get the current directory of this script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (environment_app)
parent_dir = os.path.dirname(current_dir)
# Get the parent of parent directory (src)
src_dir = os.path.dirname(parent_dir)
# Get the root directory of your project
project_dir = os.path.dirname(src_dir)

# Add these directories to Python's path
sys.path.append(project_dir)

# Now try to import using relative paths
from environment_app import create_app, db
from environment_app.flask_app.models import Feedback

print("Imports successful!")
app = create_app()

with app.app_context():
    print("Creating database tables...")
    
    # Create all tables
    db.create_all()
    print("Tables created successfully!")
    
    # Verify that the table was created
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")