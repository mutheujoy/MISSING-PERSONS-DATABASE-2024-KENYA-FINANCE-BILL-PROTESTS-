#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for, send_file, Response, jsonify
from app.models import MissingPerson, WhatsAppSessions, db
from dotenv import load_dotenv
from io import BytesIO
import re
import requests
import datetime
import os
from flask import current_app as app

# Route to display analytics page
@app.route('/')
def index():
    title = "Abducted & Missing Persons in Kenya"
    return render_template('index.html', title=title)

# Route to display analytics page
@app.route('/analytics')
def analytics():
    title = "Reports and Summary"
    return render_template('analytics.html', title=title)

# Route to display cookies policy page
@app.route('/cookies')
def cookies():
    title = "Cookies and Cache"
    return render_template('cookies.html', title=title)

# Route to display privacy policy page
@app.route('/policies')
def policies():
    title = "Privacy Policy"
    return render_template('policies.html', title=title)


# API endpoint to fetch victim statistics
@app.route('/api/victim-statistics', methods=["GET"])
def api_victim_statistics():
    title =  "Victims Statics"
    """Fetch statistics of victims based on gender, status, and security organs."""
    persons = MissingPerson.query.all()

    data = {
        "data": {
            "gender": {
                "Male": 0,
                "Female": 0
            },
            "status": {
                "Arrested": 0,
                "Abducted": 0,
                "Missing": 0,
                "Charged": 0,
                "Free": 0,
                "Fallen": 0
            },
            "security_organs": {
                "Police Service (PS)": 0,
                "Directorate of Criminal Investigations (DCI)": 0,
                "Kenya Prisons Service (KPS)": 0,
                "Unknown": 1,
            },
            "holding_locations": {
                "Lang'ata Prison": 0,
                "Unknown": 0,
                "Industrial Area Prison": 0,
                "Central Police Station": 0,
                "Karen Police Station": 0,
                "Muthangari Police Station": 0,
                "DCI HQ Kiambu": 0,
                "Unknown": 0
            }
        }
    }

    for person in persons:
        if person.gender in data["data"]["gender"]:
            data["data"]["gender"][person.gender] += 1
        if person.status in data["data"]["status"]:
            data["data"]["status"][person.status] += 1

    return jsonify(data)

# API endpoint to list victims
@app.route('/api/victims', methods=["GET"])
def api_victims():
    title = "Victims API"
    """Fetch a paginated list of victims."""
    per_page = request.args.get('per_page', 100, type=int)
    page = request.args.get('page', 1, type=int)

    persons = MissingPerson.query.paginate(page, per_page, error_out=False).items

    data = {
        "data": [{
            "id": person.id,
            "name": person.name,
            "nickname": person.nickname,
            "gender": person.gender,
            "x_handle_full": person.x_handle_full,
            "x_handle": person.x_handle,
            "photo_url": url_for('get_image', person_id=person.id),
            "status": person.status,
            "holding_location": person.holding_location,
            "last_known_location": person.last_known_location,
            "security_organ": person.security_organ,
            "time_taken": person.time_taken,
            "time_taken_formatted": person.time_taken_formatted,
            "notes": person.notes,
            "released_on": person.released_on
        } for person in persons],
        "links": {
            "first": url_for('api_victims', per_page=per_page, page=1),
            "last": url_for('api_victims', per_page=per_page, page=-1),  # Placeholder for last page
            "prev": url_for('api_victims', per_page=per_page, page=page-1) if page > 1 else None,
            "next": url_for('api_victims', per_page=per_page, page=page+1) if len(persons) == per_page else None
        },
        "meta": {
            "current_page": page,
            "per_page": per_page,
            "total": MissingPerson.query.count()
        }
    }

    return jsonify(data, title=title)

# Route to add a new missing person
@app.route('/add', methods=['GET', 'POST'])
def add_person():
    title = "Register Missing Person"
    if request.method == 'POST':
        name = request.form.get('name')
        nickname = request.form.get('nickname')
        gender = request.form.get('gender')
        x_handle = request.form.get('x_handle')
        x_handle_full = "https://x.com/"+x_handle
        status = request.form.get('status')
        holding_location = request.form.get('holding_location')
        last_known_location = request.form.get('last_known_location')
        security_organ = request.form.get('security_organ')
        time_taken = request.form.get('time_taken')
        age = request.form.get('age')
        photo = request.files.get('photo')
        photo_url = request.form.get("photo")
        occupation = request.form.get('occupation')
        last_known_location = request.form.get('last_known_location')
        contact_info = request.form.get('contact_info')
        

        if time_taken:
            time_taken = datetime.datetime.strptime(time_taken, '%Y-%m-%dT%H:%M').strftime('%H:%M %d-%m-%Y')
            time_taken_formatted = datetime.datetime.strptime(time_taken, '%H:%M %d-%m-%Y').strftime('%a, %b %d, %Y %I:%M %p')
        else:
            time_taken_formatted = None

        photo_data = None
        if photo_url:
            try:
                response = requests.get(photo_url)
                response.raise_for_status()
                photo_data = response.content
            except requests.RequestException as e:
                print(f"Error fetching the photo: {e}")

        elif photo and allowed_file(photo.filename):
            photo_data = photo.read()

        new_person = MissingPerson(
            name=name,
            nickname=nickname,
            gender=gender,
            x_handle_full=x_handle_full,
            x_handle=x_handle,
            status=status,
            holding_location=holding_location,
            security_organ=security_organ,
            time_taken=time_taken,
            time_taken_formatted=time_taken_formatted,
            age=age,
            photo_url=photo_data,  # Store the binary data in the database
            occupation=occupation,
            last_known_location=last_known_location,
            contact_info=contact_info
        )

        db.session.add(new_person)
        db.session.commit()

        return redirect(url_for('index'))
    # 
    return render_template('register_users/add_person.html', title=title)

# Route to fetch the image of a person by their ID
@app.route('/image/<int:person_id>')
def get_image(person_id):
    username = MissingPerson.query.get(person_id)
    title = f"Gallery {MissingPerson.querry.get(username)}"
    """Retrieve the image of a missing person."""
    person = MissingPerson.query.get_or_404(person_id)
    if person.photo_url:
        return send_file(BytesIO(person.photo_url), mimetype='image/jpeg')  # Adjust MIME type as needed
    else:
        return redirect(url_for('static', filename='default_image.jpg'), title=title)

def is_url(s: str) -> bool:
    """Check if a string is a URL."""
    return s.lower().startswith(('http://', 'https://', 'ftp://'))

def allowed_file(filename: str) -> bool:
    """Check if the uploaded file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def read_user_session(phone: str) -> dict:
    """Retrieve or create a new user session for a phone number."""
    whatsapp_session = WhatsAppSessions.query.filter_by(phone=phone).first()

    if not whatsapp_session:
        whatsapp_session = WhatsAppSessions(phone=phone, session_text="")
        db.session.add(whatsapp_session)
        db.session.commit()
    
    return {   
        "id": whatsapp_session.id,
        "phone": whatsapp_session.phone,
        "date_created": whatsapp_session.date_created,
        "session_text": whatsapp_session.session_text
    }

def save_user_session(state: str, session_id: int) -> dict:
    """Save the current state of a user session."""
    whatsapp_session = WhatsAppSessions.query.filter_by(id=session_id).first()
    if whatsapp_session:
        whatsapp_session.session_text = state
        db.session.commit()

        return {   
            "id": whatsapp_session.id,
            "phone": whatsapp_session.phone,
            "date_created": whatsapp_session.date_created,
            "session_text": whatsapp_session.session_text
        }
    
    return {}

@app.route("/whatsapp-ussd", methods=['POST'])
def process_response():
    """Handle incoming USSD/WhatsApp requests and provide menu-based responses."""
    form_data = request.form

    text, phone, triggerY, triggerN, incoming_text, current_state = "", "", "", "", "", ""

    if "text" in form_data and "phoneNumber" in form_data:
        incoming_text = form_data.get("text", "").split("*")[-1]
        phone = form_data.get("phoneNumber")
        triggerY, triggerN = "CON", "END"
    elif "Body" in form_data and "From" in form_data:
        message_type = form_data.get("MessageType")
        if message_type == "location":
            incoming_text = f"{form_data.get('Longitude')}<=>{form_data.get('Latitude')}"
        elif message_type == "text":
            incoming_text = form_data.get("Body")
        elif message_type in {"video", "image"}:
            incoming_text = form_data.get("MediaUrl0")

        phone_match = re.search(r'\+\d[\d\s]+', form_data.get("From"))
        phone = phone_match.group().replace(" ", "") if phone_match else ""

    user_session = read_user_session(phone)

    if user_session and "session_text" in user_session:
        current_state = user_session["session_text"]

    if incoming_text.lower() in ["back", "home", "hello", "hi", "#"]:
        if incoming_text.lower() in ["back", "#"]:
            current_state = "*".join(current_state.split("*")[:-1]) if "*" in current_state else ""
        else:
            current_state = ""
    else:
        current_state = f"{current_state}*{incoming_text}" if current_state else incoming_text

    save_token = save_user_session(current_state, user_session["id"])

    if "session_text" in user_session:
        text = save_token["session_text"]

    menu_response = {
        "greeting": "Welcome to Gerathen AI",
        "main_zero": "0. Signup\n",
        "main": "1. Report a lost person\n2. Provide updates on a lost person\n3. General news\n4. Find hospital and morgue\n5. Human Rights Tips\n6. Donate to Missing Persons Fund\n7. Privacy Policy\n8. Terms and Conditions\n9. Disclaimer",
        "back": "### Type # to go back\n",
        "signup": "Thank you for opting in, someone from our team will get back to you",
        "report_lost_person": "Please provide the name of the missing person:",
        "provide_updates": "Provide the update details here:",
        "general_news": "Please check our website for the latest news updates.",
        "find_hospital": "Please visit our website to locate hospitals and morgues near you.",
        "human_rights_tips": "Know your rights! Visit our website for more information.",
        "donate": "Thank you for considering a donation. Please visit our website to donate.",
        "privacy_policy": "Read our privacy policy at [URL].",
        "terms_and_conditions": "Read our terms and conditions at [URL].",
        "disclaimer": "Read our disclaimer at [URL]."
    }

    option_map = {
        "0": menu_response["signup"],
        "1": menu_response["report_lost_person"],
        "2": menu_response["provide_updates"],
        "3": menu_response["general_news"],
        "4": menu_response["find_hospital"],
        "5": menu_response["human_rights_tips"],
        "6": menu_response["donate"],
        "7": menu_response["privacy_policy"],
        "8": menu_response["terms_and_conditions"],
        "9": menu_response["disclaimer"]
    }

    selected_option = text.split('*')[-1] if text else ""

    if selected_option.isdigit() and int(selected_option) in option_map:
        response_message = option_map[selected_option]
        response_prefix = triggerN if selected_option in {"0", "7", "8", "9"} else triggerY
    else:
        response_message = f"{menu_response['greeting']}\n{menu_response['main']}\n{menu_response['back']}"
        response_prefix = triggerY

    response = f"{response_prefix} {response_message}"

    return response, 200

if __name__ == "__main__":
    app.run(debug=True)
