from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

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
    notes = db.Column(db.String(2000), nullable=True,  default='N/A')
    released_on = db.Column(db.String(200), nullable=False, default='N/A')
    age = db.Column(db.Integer, nullable=True)
    occupation = db.Column(db.String(250), nullable=True)
    contact_info = db.Column(db.String(250), nullable=False)
    sightings = db.relationship('Sightings', back_populates='missing_person', cascade="all, delete-orphan")

    
    def __repr__(self):
        return f'<MissingPerson {self.name}>'

class WhatsAppSessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    session_text = db.Column(db.String(10000), nullable=True)
    
    def __repr__(self):
        return f'<WhatsAppSessions {self.name}>'
    
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(50))
    record_id = db.Column(db.Integer, db.ForeignKey('missing_person.id'))
    operation = db.Column(db.String(10)) 
    old_data = db.Column(db.Text, nullable=True)  
    new_data = db.Column(db.Text, nullable=True )
    changed_at = db.Column(db.DateTime, default=datetime.now)
    changed_by = db.Column(db.String(100), nullable=True) 


class Sightings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    missing_person_id = db.Column(db.Integer, db.ForeignKey('missing_person.id'))
    photo_url = db.Column(db.String(200), nullable=True)
    last_known_location = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(200), default='pending')
    timestamp = db.Column(db.DateTime, default=datetime.now())
    reporter_contact = db.Column(db.String(250), nullable=True)
    missing_person = db.relationship("MissingPerson", back_populates="sightings")


