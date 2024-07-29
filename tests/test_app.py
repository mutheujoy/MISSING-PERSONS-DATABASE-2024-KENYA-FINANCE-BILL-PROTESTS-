import os
import sys
from flask import Flask
from flask_migrate import migrate
import pytest

# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import MissingPerson, WhatsAppSessions, MonitorPersons

@pytest.fixture
def create_app(config_name='development'):
    app = Flask(__name__)
    # Default configuration
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        # Assume you have other configurations for 'development', 'production', etc.
        app.config.from_object(f'config.{config_name.capitalize()}Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints and other setup
    with app.app_context():
        from . import views  # Import views after initializing the app context
        from . import models  # Import models after initializing the app context

    return app


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

def test_create_missing_person(init_database):
    missing_person = MissingPerson(
        name="John Doe",
        nickname="Johnny",
        gender="Male",
        x_handle_full="JohnDoeHandle",
        x_handle="johndoe",
        status="Missing",
        holding_location="Nairobi",
        last_known_location="Nairobi",
        photo_url=b"fake-image-data",
        security_organ="Nairobi Police",
        time_taken="2024-07-29T10:00:00",
        time_taken_formatted="29th July 2024, 10:00 AM",
        notes="Last seen at the mall.",
        released_on="N/A",
        age=30,
        occupation="Engineer",
        contact_info="john.doe@example.com"
    )
    db.session.add(missing_person)
    db.session.commit()

    assert missing_person.id is not None

def test_retrieve_missing_person(init_database):
    missing_person = MissingPerson(
        name="Jane Doe",
        nickname="Janey",
        gender="Female",
        x_handle_full="JaneDoeHandle",
        x_handle="janedoe",
        status="Missing",
        holding_location="Mombasa",
        last_known_location="Mombasa",
        photo_url=b"fake-image-data",
        security_organ="Mombasa Police",
        time_taken="2024-07-28T10:00:00",
        time_taken_formatted="28th July 2024, 10:00 AM",
        notes="Seen boarding a bus.",
        released_on="N/A",
        age=25,
        occupation="Doctor",
        contact_info="jane.doe@example.com"
    )
    db.session.add(missing_person)
    db.session.commit()

    retrieved_person = MissingPerson.query.filter_by(name="Jane Doe").first()
    assert retrieved_person is not None
    assert retrieved_person.name == "Jane Doe"
    assert retrieved_person.nickname == "Janey"
    assert retrieved_person.status == "Missing"

def test_delete_missing_person(init_database):
    missing_person = MissingPerson(
        name="Alice Smith",
        nickname="Ali",
        gender="Female",
        x_handle_full="AliceSmithHandle",
        x_handle="alicesmith",
        status="Missing",
        holding_location="Kisumu",
        last_known_location="Kisumu",
        photo_url=b"fake-image-data",
        security_organ="Kisumu Police",
        time_taken="2024-07-27T10:00:00",
        time_taken_formatted="27th July 2024, 10:00 AM",
        notes="Last seen at work.",
        released_on="N/A",
        age=40,
        occupation="Teacher",
        contact_info="alice.smith@example.com"
    )
    db.session.add(missing_person)
    db.session.commit()

    db.session.delete(missing_person)
    db.session.commit()

    deleted_person = MissingPerson.query.filter_by(name="Alice Smith").first()
    assert deleted_person is None

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_create_whatsapp_session(init_database):
    whatsapp_session = WhatsAppSessions(
        phone="+1234567890",
        session_text="This is a test session."
    )
    db.session.add(whatsapp_session)
    db.session.commit()

    assert whatsapp_session.id is not None

def test_retrieve_whatsapp_session(init_database):
    whatsapp_session = WhatsAppSessions(
        phone="+1987654321",
        session_text="Another test session."
    )
    db.session.add(whatsapp_session)
    db.session.commit()

    retrieved_session = WhatsAppSessions.query.filter_by(phone="+1987654321").first()
    assert retrieved_session is not None
    assert retrieved_session.phone == "+1987654321"

def test_create_monitor_person(init_database):
    missing_person = MissingPerson(
        name="Chris Brown",
        nickname="Chris",
        gender="Male",
        status="Missing",
        contact_info="chris.brown@example.com"
    )
    db.session.add(missing_person)
    db.session.commit()

    monitor_person = MonitorPersons(
        missing_person_monitor_id=missing_person.id,
        photo_url="http://example.com/photo.jpg",
        last_known_location="New York"
    )
    db.session.add(monitor_person)
    db.session.commit()

    assert monitor_person.id is not None

def test_retrieve_monitor_person(init_database):
    missing_person = MissingPerson(
        name="Emily Clark",
        nickname="Em",
        gender="Female",
        status="Missing",
        contact_info="emily.clark@example.com"
    )
    db.session.add(missing_person)
    db.session.commit()

    monitor_person = MonitorPersons(
        missing_person_monitor_id=missing_person.id,
        photo_url="http://example.com/photo.jpg",
        last_known_location="Los Angeles"
    )
    db.session.add(monitor_person)
    db.session.commit()

    retrieved_monitor = MonitorPersons.query.filter_by(missing_person_monitor_id=missing_person.id).first()
    assert retrieved_monitor is not None
    assert retrieved_monitor.last_known_location == "Los Angeles"
