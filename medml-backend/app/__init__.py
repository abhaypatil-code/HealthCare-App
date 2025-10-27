# HealthCare App/medml-backend/app/__init__.py
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from app.config import config  # <-- Corrected import path
from .extensions import db, jwt, bcrypt, cors
from .api import api_bp
from . import services  # <-- FIX: Changed from 'ml_service' to 'services' to match provided file
from .db_seeder import seed_static_recommendations

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Extension initializations
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    Migrate(app, db)
    
    # --- Load ML Models & Seed DB ---
    with app.app_context():
        services.load_models(app) # <-- FIX: Changed from 'ml_service' to 'services'
        seed_static_recommendations()
    # --- End ---

    # Register Blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    # Import models to ensure they are registered
    from . import models

    # --- Add Logging ---
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/medml.log', maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('MedML backend startup')
    # --- End Logging ---

    # Global error handler for 500
    @app.errorhandler(500)
    def internal_server_error(e):
        app.logger.error(f"Internal Server Error: {e}", exc_info=True)
        return jsonify(error="Internal Server Error", message="An unexpected error occurred"), 500
    
    @app.errorhandler(404)
    def not_found_error(e):
        # Use str(e) to get the default "Not Found" message or a custom one
        return jsonify(error="Not Found", message=str(e).replace("404 Not Found: ", "")), 404

    return app