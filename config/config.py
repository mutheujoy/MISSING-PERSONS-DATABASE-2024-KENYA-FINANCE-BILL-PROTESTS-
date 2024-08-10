import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '2b5840e9e7922a8757fffcd9a8341a7bd99ceedb7b53edc5')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:pa55word@localhost/missing_persons')
    SQLALCHEMY_BINDS = {
        'missing_persons': os.getenv('SQLALCHEMY_BINDS', 'sqlite:///missing_persons.sqlite3')
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection Pool Settings
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_timeout': 30,
        'pool_recycle': 3600,
        'max_overflow': 20
    }
    
    # Mail server settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.example.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'your-email@example.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'your-email-password')
    ADMINS = [os.getenv('ADMINS', 'admin@example.com')]
    
    # Pagination and internationalization
    POSTS_PER_PAGE = int(os.getenv('POSTS_PER_PAGE', 25))
    LANGUAGES = os.getenv('LANGUAGES', 'en,es').split(',')
    
    # Translation and search
    MS_TRANSLATOR_KEY = os.getenv('MS_TRANSLATOR_KEY', 'your-translator-key')
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
    
    # Redis configuration
    REDIS_URL = os.getenv('REDIS_URL', 'redis://')
    
    # Logging
    LOG_TO_STDOUT = os.getenv('LOG_TO_STDOUT', 'False') == 'True'
    
    # Search settings
    MAX_SEARCH_RESULTS = int(os.getenv('MAX_SEARCH_RESULTS', 50))
    
    # Application settings
    SERVER_NAME = os.getenv('SERVER_NAME', 'localhost')
    APP_PORT = int(os.getenv('APP_PORT', 5000))
    
    # PostgreSQL settings
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'pa55word')
    POSTGRES_DB_HOST = os.getenv('POSTGRES_DB_HOST', 'localhost')
    POSTGRES_PORT = int(os.getenv('POSTGRES_PORT', 5432))
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'missing_persons')

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    
class TestingConfig(Config):
    FLASK_ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class ProductionConfig(Config):
    FLASK_ENV = 'production'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
