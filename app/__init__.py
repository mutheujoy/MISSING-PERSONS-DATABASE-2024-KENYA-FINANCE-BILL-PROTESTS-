from flask import Flask
from flask_migrate import Migrate
from app.models import db
from config.config import config

migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize the database
    db.init_app(app)
    migrate.init_app(app, db)
    #  Debug URI
    print(f"Using database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    # Register blueprints and other setup
    with app.app_context():
        from . import views  # Import views after initializing the app context
        from . import models  # Import models after initializing the app context

    return app
