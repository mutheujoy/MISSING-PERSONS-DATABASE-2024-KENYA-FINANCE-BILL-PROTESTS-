import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #connecting tests folder with root path to allow imports
from app import db, create_app

@pytest.fixture
def app():
    app = create_app(config_name="test")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
