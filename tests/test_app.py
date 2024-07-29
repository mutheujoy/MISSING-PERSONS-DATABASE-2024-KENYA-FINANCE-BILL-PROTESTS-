from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pytest
app = Flask(__name__)
db = SQLAlchemy(app)

@pytest.fixture
def app():
    app = app.create_app()
    app.config.update({
        "TESTING": True,
    })

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
