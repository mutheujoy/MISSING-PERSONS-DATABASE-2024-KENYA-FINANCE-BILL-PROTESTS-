#!/usr/bin/env python3

import os
# from flask import render_template, request, redirect, url_for
# from werkzeug.utils import secure_filename
# import os
# from . import db
# from .models import MissingPerson
# from . import create_app

# app = create_app()

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# @app.route('/')
# def index():
#     persons = MissingPerson.query.all()
#     return render_template('index.html', persons=persons)

# @app.route('/add', methods=['GET', 'POST'])
# def add_person():
#     if request.method == 'POST':
#         name = request.form['name']
#         age = request.form['age']
#         photo = request.files['photo']
#         occupation = request.form['occupation']
#         last_known_location = request.form['last_known_location']
#         contact_info = request.form['contact_info']

#         photo_data = None
#         if photo and allowed_file(photo.filename):
#             photo_data = photo.read()  # Read the file data as binary

#         new_person = MissingPerson(
#             name=name,
#             age=age,
#             photo=photo_data,  # Store the binary data in the database
#             occupation=occupation,
#             last_known_location=last_known_location,
#             contact_info=contact_info
#         )
        
#         db.session.add(new_person)
#         db.session.commit()
        
#         return redirect(url_for('index'))
    
#     return render_template('add_person.html')
from flask import render_template, request, redirect, url_for
from . import db
from .models import MissingPerson
from flask import current_app as app


@app.route("/")
def index():
    """Display a list of all missing persons."""
    template_path = os.path.join(app.root_path, 'templates', 'index.html')
    print(f"Looking for template at: {template_path}")
    try:
        persons = MissingPerson.query.all()
    except Exception as e:
        app.logger.error(f"Error retrieving missing persons: {e}")
        persons = []
    return render_template('app/index.html', persons=persons)


@app.route("/all")
def all_listing():
    persons = MissingPerson.query.all()
    return render_template("all-missing-persons.html", persons=persons)

@app.route("/gallery")
def gallery():
    persons = MissingPerson.query.all()
    return render_template("gallery.html", persons=persons)

@app.route("/add", methods=["GET", "POST"])
def add_person():
    """Add a new missing person."""
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            age = request.form.get('age', type=int)
            photo_url = request.form.get('photo_url')
            occupation = request.form.get('occupation')
            last_known_location = request.form.get('last_known_location')
            contact_info = request.form.get('contact_info')
            
            if not all([name, age, last_known_location, contact_info]):
                app.logger.error("Missing required form fields.")
                return redirect(url_for('add_person'))

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
            app.logger.info(f"Added new missing person: {name}")
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error adding person: {e}")
            return redirect(url_for('add_person'))
    
    return render_template('register_users/add_person.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
