# HealthCare App/medml-backend/app/config.py
import os
from datetime import timedelta

# This is the 'app' directory
basedir = os.path.abspath(os.path.dirname(__file__))
# This is the project's root directory (medml-backend)
BASE_DIR = os.path.abspath(os.path.join(basedir, '..'))

class Config:
    # --- FIX: Remove hardcoded fallbacks for security ---
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for Flask application")

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'medml.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Base directory for the application
    BASE_DIR = BASE_DIR
    
    # --- FIX: JWT Configuration ---
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("No JWT_SECRET_KEY set for Flask application")
        
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES_MIN', 15)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES_DAYS', 30)))
    
    # --- ADDED: Externalize Risk Thresholds (for Batch 3) ---
    RISK_THRESHOLDS = {
        'medium': 0.35,
        'high': 0.70
    }

class DevelopmentConfig(Config):
    DEBUG = True
    # Allow missing env vars in dev
    if not Config.SECRET_KEY:
        Config.SECRET_KEY = 'dev-secret-key'
    if not Config.JWT_SECRET_KEY:
        Config.JWT_SECRET_KEY = 'dev-jwt-secret-key'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret'
    JWT_SECRET_KEY = 'test-jwt-secret'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # In production, SECRET_KEY and JWT_SECRET_KEY *must* be set
    # The check in Config class enforces this.

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}