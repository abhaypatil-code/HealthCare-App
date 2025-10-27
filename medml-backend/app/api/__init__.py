# HealthCare App/medml-backend/app/api/__init__.py
from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import routes to register them with the blueprint
from . import auth
from . import patients
from . import assessments
from . import predict
from . import dashboard
from . import recommendations
from . import consultations   # <-- ADDED
from . import reports         # <-- ADDED
from . import errors