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
from . import create_app

app = create_app()


@app.route("/")
def index():
    persons = MissingPerson.query.all()
    return render_template("home.html", persons=persons)

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
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        photo_url = request.form["photo_url"]
        occupation = request.form["occupation"]
        last_known_location = request.form["last_known_location"]
        contact_info = request.form["contact_info"]

        new_person = MissingPerson(
            name=name,
            age=age,
            photo_url=photo_url,
            occupation=occupation,
            last_known_location=last_known_location,
            contact_info=contact_info,
        )

        db.session.add(new_person)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("add_person.html")
