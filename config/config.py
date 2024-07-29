#!/usr/bin/env python3

# config/config.py
import os

class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or '2b5840e9e7922a8757fffcd9a8341a7bd99ceedb7b53edc5'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:pa55word@localhost:5432/missing_persons'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:pa55word@localhost/missing_persons'
    # SQLALCHEMY_BINDS is not needed if you are using one database URI

class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret_key_y0u_never_guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:pa55word@localhost/missing_persons'
    # SQLALCHEMY_BINDS is not needed if you are using one database URI
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    CSRF_ENABLED = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}

