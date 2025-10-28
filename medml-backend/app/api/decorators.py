# HealthCare App/medml-backend/app/api/decorators.py
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def admin_required(fn):
    """
    Custom decorator to ensure a route is accessed only by a user with
    the 'admin' role, as stored in the JWT.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            jwt_identity = get_jwt_identity()
            if not jwt_identity:
                return jsonify(error="Unauthorized", message="Missing or invalid token"), 401
            user_role = jwt_identity.get('role')
            
            if user_role != 'admin':
                return jsonify(error="Forbidden", message="Admin access required"), 403
            
            return fn(*args, **kwargs)
        except Exception as e:
            # This can catch issues if the token is malformed
            return jsonify(error="Invalid token", message=str(e)), 401
    return wrapper

def get_current_admin_id():
    """
    Helper function to safely get the ID of the currently logged-in admin
    from the JWT identity.
    """
    try:
        return get_jwt_identity().get('id')
    except:
        return None