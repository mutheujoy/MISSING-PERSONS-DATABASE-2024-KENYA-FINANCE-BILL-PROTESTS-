import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.models import MissingPerson, MonitorPersons

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///:memory:")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
    persons = MissingPerson.query.all()
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
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        photo_url = request.form["photo_url"]
        occupation = request.form["occupation"]
        last_known_location = request.form["last_known_location"]
        contact_info = request.form["contact_info"]
        nickname = request.form.get("nickname", "N/A")
        gender = request.form.get("gender", "N/A")
        x_handle_full = request.form.get("x_handle_full", "N/A")
        x_handle = request.form.get("x_handle", "N/A")
        status = request.form.get("status", "N/A")
        holding_location = request.form.get("holding_location", "N/A")
        security_organ = request.form.get("security_organ", "N/A")
        time_taken = request.form.get("time_taken", "N/A")
        time_taken_formatted = request.form.get("time_taken_formatted", "N/A")
        notes = request.form.get("notes", "N/A")
        released_on = request.form.get("released_on", "N/A")

        new_person = MissingPerson(
            name=name,
            age=age,
            photo_url=photo_url,
            occupation=occupation,
            last_known_location=last_known_location,
            contact_info=contact_info,
            nickname=nickname,
            gender=gender,
            x_handle_full=x_handle_full,
            x_handle=x_handle,
            status=status,
            holding_location=holding_location,
            security_organ=security_organ,
            time_taken=time_taken,
            time_taken_formatted=time_taken_formatted,
            notes=notes,
            released_on=released_on
        )

        db.session.add(new_person)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register_users/add_person.html')

@app.route("/monitor", methods=["GET", "POST"])
def add_monitor_info():
    if request.method == "POST":
        print(request.form) 
        missing_person_monitor_id = request.form.get("missing_person_monitor_id")
        photo_url = request.form["photo_url"]
        last_known_location = request.form["last_known_location"]

        monitor_person = MonitorPersons(
            missing_person_monitor_id=missing_person_monitor_id,
            photo_url=photo_url,
            last_known_location=last_known_location,
        )

        db.session.add(monitor_person)
        db.session.commit()

        return redirect(url_for("index"))
    persons = MissingPerson.query.all()

    return render_template("monitor_person.html", persons=persons)

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)  # Initialize the SQLAlchemy object
        db.create_all()
    app.run(debug=True)
