from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class MissingPerson(db.Model):
    __tablename__ = 'missing_person'  # Make sure this matches the table name in your database

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nickname = db.Column(db.String(100), nullable=True, default='N/A')
    gender = db.Column(db.String(100), nullable=False)
    x_handle_full = db.Column(db.String(1000), nullable=True, default='N/A')
    x_handle = db.Column(db.String(200), nullable=True, default='N/A')
    status = db.Column(db.String(100), nullable=False)
    holding_location = db.Column(db.String(100), nullable=True, default='N/A')
    last_known_location = db.Column(db.String(200), nullable=True, default='N/A')
    photo_url = db.Column(db.LargeBinary, nullable=True)
    security_organ = db.Column(db.String(200), nullable=True, default='N/A')
    time_taken = db.Column(db.String(200), nullable=True)
    time_taken_formatted = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.String(2000), nullable=True, default='N/A')
    released_on = db.Column(db.String(200), nullable=False, default='N/A')
    age = db.Column(db.Integer, nullable=True)
    occupation = db.Column(db.String(250), nullable=True)
    contact_info = db.Column(db.String(250), nullable=False)
    monitor_persons = db.relationship('MonitorPersons', backref='monitor')
    
    def __repr__(self):
        return f'<MissingPerson {self.name}>'

class WhatsAppSessions(db.Model):
    __tablename__ = 'whatsapp_sessions'

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    session_text = db.Column(db.String(10000), nullable=True)
    
    def __repr__(self):
        return f'<WhatsAppSessions {self.phone}>'

class MonitorPersons(db.Model):
    __tablename__ = 'monitor_persons'

    id = db.Column(db.Integer, primary_key=True)
    missing_person_monitor_id = db.Column(db.Integer, db.ForeignKey('missing_person.id'))
    photo_url = db.Column(db.String(200), nullable=True)
    last_known_location = db.Column(db.String(200), nullable=False)

