# HealthCare App/medml-backend/app/api/errors.py
from flask import jsonify
from . import api_bp
from pydantic import ValidationError

@api_bp.app_errorhandler(404)
def not_found_error(error):
    return jsonify(error="Not Found", message=str(error)), 404

@api_bp.app_errorhandler(500)
def internal_error(error):
    # db.session.rollback() # Rollback in case of DB errors
    return jsonify(error="Internal Server Error", message="An unexpected error occurred."), 500

@api_bp.app_errorhandler(400)
def bad_request_error(error):
    return jsonify(error="Bad Request", message=str(error)), 400

@api_bp.app_errorhandler(422)
def validation_error(error):
    # This handler can catch Pydantic's ValidationError if raised
    if isinstance(error.description, ValidationError):
        return jsonify(error="Validation Failed", messages=error.description.errors()), 422
    return jsonify(error="Unprocessable Entity", message=str(error)), 422

@api_bp.app_errorhandler(401)
def unauthorized_error(error):
    return jsonify(error="Unauthorized", message=str(error)), 401

@api_bp.app_errorhandler(403)
def forbidden_error(error):
    return jsonify(error="Forbidden", message=str(error)), 403