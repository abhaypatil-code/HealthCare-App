# HealthCare App/medml-backend/app/config.py
import os
from datetime import timedelta

# This is the 'app' directory
basedir = os.path.abspath(os.path.dirname(__file__))
# This is the project's root directory (medml-backend)
BASE_DIR = os.path.abspath(os.path.join(basedir, '..'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'medml.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Base directory for the application
    BASE_DIR = BASE_DIR
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 1)))
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Add production-specific settings here (e.g., PostgreSQL DB)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}