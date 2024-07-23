from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from app.models import MissingPerson, db
import os
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

app = Flask(__name__)

# Get environment variables
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = 'lstdb'
db_port = os.getenv('POSTGRES_PORT', '5432')
db_name = os.getenv('POSTGRES_DB')

# Configure SQLAlchemy to use PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

db.init_app(app)

@app.route('/')
def index():
    persons = MissingPerson.query.all()
    return render_template('index.html', persons=persons)

@app.route('/add', methods=['GET', 'POST'])
def add_person():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        photo = request.files['photo']
        occupation = request.form['occupation']
        last_known_location = request.form['last_known_location']
        contact_info = request.form['contact_info']

        photo_data = None
        if photo and allowed_file(photo.filename):
            photo_data = photo.read()  # Read the file data as binary

        new_person = MissingPerson(
            name=name,
            age=age,
            photo=photo_data,  # Store the binary data in the database
            occupation=occupation,
            last_known_location=last_known_location,
            contact_info=contact_info
        )
        
        db.session.add(new_person)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('add_person.html')

@app.route('/image/<int:person_id>')
def get_image(person_id):
    person = MissingPerson.query.get_or_404(person_id)
    if person.photo:
        return send_file(BytesIO(person.photo), mimetype='image/jpeg')  # Adjust MIME type as needed
    else:
        return redirect(url_for('static', filename='default_image.jpg')) 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
