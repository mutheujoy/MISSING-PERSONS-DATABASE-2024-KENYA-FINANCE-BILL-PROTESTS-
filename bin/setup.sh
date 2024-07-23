#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
export FLASK_APP=App.py
flask run
