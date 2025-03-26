import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create a SQLAlchemy object
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Get the absolute path to your existing database
    project_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    db_path = os.path.join(project_dir, 'instance', 'environment.db')
    
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI="sqlite:///" + db_path,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is not None:
        app.config.update(test_config)
    else:
        app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    with app.app_context():
        from environment_app.flask_app import models  
        from environment_app.flask_app.routes import main
        app.register_blueprint(main)

    return app