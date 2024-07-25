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
