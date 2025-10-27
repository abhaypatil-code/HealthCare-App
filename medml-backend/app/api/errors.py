from flask import jsonify
from . import api_bp
from pydantic import ValidationError

@api_bp.app_errorhandler(400)
def bad_request(error):
    return jsonify(error="Bad Request", message=str(error)), 400

@api_bp.app_errorhandler(401)
def unauthorized(error):
    return jsonify(error="Unauthorized", message=str(error)), 401

@api_bp.app_errorhandler(404)
def not_found(error):
    return jsonify(error="Not Found", message=str(error)), 404

@api_bp.app_errorhandler(422)
def unprocessable_entity(error):
    # This will be triggered by pydantic validation errors
    if isinstance(error.description, ValidationError):
        return jsonify(error="Validation Failed", messages=error.description.errors()), 422
    return jsonify(error="Unprocessable Entity", message=str(error)), 422

@api_bp.app_errorhandler(500)
def internal_server_error(error):
    return jsonify(error="Internal Server Error", message=str(error)), 500