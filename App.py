from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///missing_persons.db'
db = SQLAlchemy(app)

from app.models import MissingPerson
 
@app.route('/')
def index():
    persons = MissingPerson.query.all()
    return render_template('index.html', persons=persons)

@app.route('/add', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        photo_url = request.form['photo_url']
        occupation = request.form['occupation']
        last_known_location = request.form['last_known_location']
        contact_info = request.form['contact_info']
        
        new_person = MissingPerson(
            name=name,
            age=age,
            photo_url=photo_url,
            occupation=occupation,
            last_known_location=last_known_location,
            contact_info=contact_info
        )
        
        db.session.add(new_person)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_person.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
