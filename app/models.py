from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class MissingPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.LargeBinary, nullable=True)
    occupation = db.Column(db.String(100), nullable=True)
    last_known_location = db.Column(db.String(200), nullable=False)
    contact_info = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<MissingPerson {self.name}>'

class WhatsAppSessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.Date, nullable=False, default=date.today)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    session_text = db.Column(db.String(10000), nullable=True)
    
    def __repr__(self):
        return f'<WhatsAppSessions {self.name}>'