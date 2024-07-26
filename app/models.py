from . import db

class MissingPerson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    photo_url = db.Column(db.String(200), nullable=True)
    occupation = db.Column(db.String(100), nullable=True)
    last_known_location = db.Column(db.String(200), nullable=False)
    contact_info = db.Column(db.String(200), nullable=False)
    monitor_persons = db.relationship('MonitorPersons', backref='monitor')

    
    def __repr__(self):
        return f'<MissingPerson {self.name}>'

class MonitorPersons(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    missing_person_monitor_id = db.Column(db.Integer, db.ForeignKey('missing_person.id'))
    photo_url = db.Column(db.String(200), nullable=True)
    last_known_location = db.Column(db.String(200), nullable=False)


