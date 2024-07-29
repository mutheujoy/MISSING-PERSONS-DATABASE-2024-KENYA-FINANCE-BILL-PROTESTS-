import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a_secret_key"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "sqlite:///missing_persons.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 600
    SESSION_REFRESH_EACH_REQUEST = True
