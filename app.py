from flask import Flask, render_template, request, redirect, url_for, send_file, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.models import MissingPerson, WhatsAppSessions, db
import os
from dotenv import load_dotenv
from io import BytesIO
import re
import requests
import datetime

load_dotenv()

app = Flask(__name__)

# Get environment variables
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_DB_HOST')
db_port = os.getenv('POSTGRES_PORT', '5432')
db_name = os.getenv('POSTGRES_DB')
application_port=int(os.getenv('APP_PORT'))

# Configure SQLAlchemy to use PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

# /api/victim-statistics
@app.route('/api/victim-statistics', methods = ["GET"])
def api_victim_statistics():
    persons = MissingPerson.query.all()

    data = {
        "data": {
            "gender": {
                "Male": 0,
                "Female": 0
            },
            "status": {
                "Arrested":0,
                "Abducted":0,
                "Missing":0,
                "Charged":0,
                "Free": 0,
                "Fallen":0
            },
            "security_organs": {
                "Police Service (PS)":0,
                "Directorate of Criminal Investigations (DCI)":0,
                "Kenya Prisons Service (KPS)":0,
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
                "Uknown":0
            }
        }
    }

    for person in persons:
        if person.gender == "Male":
            data["data"]["gender"]["Male"] += 1

        if person.gender == "Female":
            data["data"]["gender"]["Female"] += 1

        if person.status == "Abducted":
            data["data"]["status"]["Abducted/Kidnapped"] += 1

        if person.status == "Missing":
            data["data"]["status"]["Missing"] += 1
        
        if person.status == "Charged":
            data["data"]["status"]["Charged"] += 1

        if person.status == "Free":
            data["data"]["status"]["Free"] += 1

        if person.status == "Fallen":
            data["data"]["status"]["Fallen"] += 1

    return jsonify(data)

@app.route('/api/victims', methods = ["GET"])
def api_victims():
    per_page = request.args.get('per_page', 100)
    page = request.args.get('page', 1)

    person_data = []
    persons = MissingPerson.query.all()
    
    data = {
        "data": [
    
        ],
        "links": {
            "first": "/api/victims?per_page="+str(per_page)+"&page="+str(page),
            "last": "/api/victims?per_page="+str(per_page)+"&page="+str(page),
            "prev": None,
            "next": None
        },
        "meta": {
            "current_page": 1,
            "from": 1,
            "last_page": 1,
            "links": [
            {
                "url": None,
                "label": "&laquo; Previous",
                "active": False
            },
            {
                "url": "/api/victims?per_page=10&page=1",
                "label": "1",
                "active": True
            },
            {
                "url": None,
                "label": "Next &raquo;",
                "active": False
            }
            ],
            "path": "/api/victims",
            "per_page": per_page,
            "to": 0,
            "total": 0
        }
    }

    for person in persons:
        data["data"].append({
            "id": person.id,
            "name": person.name,
            "nickname": person.nickname,
            "gender": person.gender,
            "x_handle_full": person.x_handle_full,
            "x_handle": person.x_handle,
            "photo_url": "/image/"+str(person.id),
            "status": person.status,
            "holding_location": person.holding_location,
            "last_known_location": person.last_known_location,
            "security_organ": person.security_organ,
            "time_taken": person.time_taken,
            "time_taken_formatted": person.time_taken_formatted,
            "notes": person.notes,
            "released_on": person.released_on
        })
        data["meta"]["to"] += 1
        data["meta"]["total"] += 1

    return jsonify(data)

@app.route('/add', methods=['GET', 'POST'])
def add_person():
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
    
    return render_template('add_person.html')

@app.route('/image/<int:person_id>')
def get_image(person_id):
    person = MissingPerson.query.get_or_404(person_id)
    if person.photo_url:
        return send_file(BytesIO(person.photo_url), mimetype='image/jpeg')  # Adjust MIME type as needed
    else:
        return redirect(url_for('static', filename='default_image.jpg'))

def is_url(s: str) -> bool:
    return s.lower().startswith(('http://', 'https://', 'ftp://'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def read_user_session(phone: str):
    whatsapp_session = WhatsAppSessions.query.filter_by(phone=phone).first()

    if not whatsapp_session:

        whatsapp_session = WhatsAppSessions(
            phone=phone,
            session_text="",
        )
        
        db.session.add(whatsapp_session)
        db.session.commit()
    
    return {   
        "id":whatsapp_session.id,
        "phone":whatsapp_session.phone,
        "date_created":whatsapp_session.date_created,
        "session_text":whatsapp_session.session_text
    }


def save_user_session(state, id):
    whatsapp_session = WhatsAppSessions.query.filter_by(id=id).first()
    if whatsapp_session:
        whatsapp_session.session_text = state
        db.session.commit()

        return {   
            "id":whatsapp_session.id,
            "phone":whatsapp_session.phone,
            "date_created":whatsapp_session.date_created,
            "session_text":whatsapp_session.session_text
        }
    
    return ""


@app.route("/whatsapp-ussd", methods=['POST'])
def process_response():
    form_data = name = request.form

    text = ""
    phone = ""
    triggerY = ""
    triggerN = ""
    incoming_text = ""
    current_state = ""
    
    if "text" in form_data and "phoneNumber" in form_data:
        incoming_text = form_data.get("text") if form_data.get("text") is not None else ""
        incoming_text = incoming_text.split("*")
        incoming_text = incoming_text[len(incoming_text)-1]

        phone = form_data.get("phoneNumber")
        triggerY = "CON"
        triggerN = "END"
    elif "Body" in form_data and "From" in form_data:
        
        if form_data.get("MessageType") == "location":
            incoming_text = form_data.get("Longitude")+"<=>"+form_data.get("Latitude")
        elif form_data.get("MessageType") == "text":
            incoming_text = form_data.get("Body")
        elif form_data.get("MessageType") == "video" or form_data.get("MessageType") == "image":
            incoming_text = form_data.get("MediaUrl0")

        phone = re.search(r'\+\d[\d\s]+', form_data.get("From")).group().replace(" ", "")

    user_session = read_user_session(phone)

    if len(user_session) > 0 and "session_text" in user_session:
        current_state = user_session["session_text"]

    if incoming_text.lower() in ["back", "home", "hello", "hi", "#"]:
        if incoming_text.lower() == "back" or incoming_text == "#":
            if "*" in current_state:
                current_state = "*".join(current_state.split("*")[:-1])
            else:
                current_state = ""

        else:
            current_state = ""
    else:
        current_state = f"{current_state}*{incoming_text}" if current_state else incoming_text

    save_token = save_user_session(current_state, user_session["id"])

    if "session_text" in user_session:
        text = save_token["session_text"]

    menu_response = {
        "greeting":"Welcome to Gerathen AI",
        "main_zero":"0. Signup\n",
        "main":"1. Report a lost person\n2. Provide updates on a lost person\n3. General news\n4. Chat with AI assistant",
        "report_missing_person":[
            "Name of the victim e.g John Doe?",
            "Select gender of the victim\n1. Male\n2. Female?",
            "What is the situation\n1. Arrested\n2. Abducted\n3. Charged\n4. Missing\n5. Fallen",
            "Whom do you allege is involved\n1. National Police Service (NPS)\n2. DCI\n3. Kenya Prisons (KPS)\n4. Unknown",
            "When was did it happen e.g 12:00 12-10-2023?",
            "Age of the victim e.g 20?",
            "Upload a picture or video of the person",
            "What is the occupation of the victim e.g student?",
            "What was the victim's last known location e.g JKIA?",
            "How can someone with information reach you e.g 07xxxxxxxx?",
            "Your request has been received and uploaded to https://lostinkenya.org",
        ],
        "feature_not_complete":[
            "The feature is not complete at the moment, thank you for your interest. Check back soon"
        ],
        "back":"#) Back"
    }

    if '*' in text:
        text = text.split("*")
    else:
        text = text.split()

    if text == "" or len(text) == 0:
        return Response(f"{triggerY} Dear esteemed user, {menu_response['greeting']}\n{menu_response['main']})\n", status=200, mimetype='text/plain')
    elif text[0] == "1":
        # report a missing person
        # app.logger.debug(text)

        if len(text) == 1:
            return Response(f"{triggerY} {menu_response['report_missing_person'][0]}\n\n{menu_response['back']}", status=200, mimetype='text/plain')
        elif len(text) == 2:
            return Response(f"{triggerY} {menu_response['report_missing_person'][1]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
        elif len(text) == 3:
            return Response(f"{triggerY} {menu_response['report_missing_person'][2]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
        elif len(text) == 4:
            return Response(f"{triggerY} {menu_response['report_missing_person'][3]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
        elif len(text) == 5:
            return Response(f"{triggerY} {menu_response['report_missing_person'][4]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
        elif len(text) == 6:
            return Response(f"{triggerY} {menu_response['report_missing_person'][5]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
        elif len(text) == 7:
            return Response(f"{triggerY} {menu_response['report_missing_person'][6]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
        elif len(text) == 8:
            return Response(f"{triggerY} {menu_response['report_missing_person'][7]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
        elif len(text) == 9:
            return Response(f"{triggerY} {menu_response['report_missing_person'][8]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
        elif len(text) == 10:
            return Response(f"{triggerY} {menu_response['report_missing_person'][9]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
        elif len(text) == 11:
            
            current_state = ""
            save_user_session(current_state, user_session["id"])

            try:
                response = requests.get(text[7])
                response.raise_for_status()
                photo_data = response.content

                new_person = MissingPerson(
                    name=text[1],
                    gender=text[2],
                    status=["Arrested", "Abducted", "Charged", "Missing", "Fallen"][int(text[3])-1],
                    security_organ=["Police Service (PS)", "Directorate of Criminal Investigations (DCI)", "Kenya Prisons Service (KPS)", "Unknown"][int(text[4])-1],
                    time_taken=text[5],
                    age=text[6],
                    photo_url=photo_data,
                    occupation=text[8],
                    last_known_location=text[9],
                    contact_info=text[10],
                    time_taken_formatted = datetime.datetime.strptime(text[5], '%H:%M %d-%m-%Y').strftime('%a, %b %d, %Y %I:%M %p')
                )
                
                db.session.add(new_person)
                db.session.commit()

                return Response(f"{triggerY} {menu_response['report_missing_person'][10]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
                
            except requests.RequestException as e:
                return Response(f"Error fetching the photo {text[3]}: {e}", status=200, mimetype='text/plain')
        
    current_state = ""
    save_user_session(current_state, user_session["id"])
    return Response(f"{triggerN} {menu_response['main']}\n\n{menu_response['back']}", status=200, mimetype='text/plain')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=application_port, debug=True)
