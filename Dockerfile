FROM python:3.9-slim

WORKDIR /app

RUN pip install virtualenv

RUN virtualenv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
