import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# Now import the create_app function
from environment_app import create_app

# Create the app
app = create_app()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)