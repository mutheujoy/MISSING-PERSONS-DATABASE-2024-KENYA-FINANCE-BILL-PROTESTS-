from flask_sqlalchemy import SQLAlchemy

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