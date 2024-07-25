from flask import Flask, render_template, request, redirect, url_for, send_file, Response
from flask_sqlalchemy import SQLAlchemy
from app.models import MissingPerson, WhatsAppSessions, db
import os
from dotenv import load_dotenv
from io import BytesIO
import re
import requests

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
        photo_url = request.form["photo"]
        occupation = request.form['occupation']
        last_known_location = request.form['last_known_location']
        contact_info = request.form['contact_info']

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
            "Name of the missing person e.g John Doe?",
            "Age of the missing person e.g 20?",
            "Upload a picture or video of the person",
            "What is the occupation of the lost person e.g student?",
            "What was his/her last known location e.g JKIA?",
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
            
            current_state = ""
            save_user_session(current_state, user_session["id"])

            try:
                response = requests.get(text[3])
                response.raise_for_status()
                photo_data = response.content

                new_person = MissingPerson(
                    name=text[1],
                    age=text[2],
                    photo=photo_data,
                    occupation=text[4],
                    last_known_location=text[5],
                    contact_info=text[6]
                )
                
                db.session.add(new_person)
                db.session.commit()

                # app.logger.debug(new_person)

                return Response(f"{triggerY} {menu_response['report_missing_person'][6]}\n\n{menu_response['back']}\n", status=200, mimetype='text/plain')
                
            except requests.RequestException as e:
                return Response(f"Error fetching the photo {text[3]}: {e}", status=200, mimetype='text/plain')
        
    current_state = ""
    save_user_session(current_state, user_session["id"])
    return Response(f"{triggerN} {menu_response['main']}\n\n{menu_response['back']}", status=200, mimetype='text/plain')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
