#!/usr/bin/env python
# app/__init__.py
from flask import Flask, app, config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)

    # Disable tracking modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 10
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 60
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20

    # Load configuration
    app.config.from_object(f'config.config.{config_name.capitalize()}Config')

    # Initialize the database
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints and other setup
    with app.app_context():
        from . import views  # Import views after initializing the app context
        from . import models  # Import models after initializing the app context

    return app
