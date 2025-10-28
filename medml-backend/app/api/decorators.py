# HealthCare App/medml-backend/app/api/decorators.py
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def admin_required(fn):
    """
    Decorator to ensure the user is an admin.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        jwt_identity = get_jwt_identity()
        if jwt_identity.get('role') != 'admin':
            return jsonify(error="Forbidden", message="Admin access required"), 403
        return fn(*args, **kwargs)
    return wrapper

def get_current_admin_id():
    """
    Helper function to get the ID of the currently logged-in admin.
    Assumes this is called from within an @admin_required route.
    """
    try:
        jwt_identity = get_jwt_identity()
        if jwt_identity.get('role') == 'admin':
            return jwt_identity.get('id')
    except Exception:
        pass # Will return None
    return None