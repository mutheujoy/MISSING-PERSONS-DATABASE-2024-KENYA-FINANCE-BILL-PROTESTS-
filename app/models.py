from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pa55word@localhost/missing_persons'
db = SQLAlchemy(app)

class MissingPerson(db.Model):
    __tablename__ = 'missing_person'  # Make sure this matches the table name in your database

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    photo_url = db.Column(db.String(200))
    occupation = db.Column(db.String(100))
    last_known_location = db.Column(db.String(200))
    contact_info = db.Column(db.String(100))

    def __repr__(self):
        return f'<MissingPerson {self.name}>'
