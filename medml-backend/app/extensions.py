from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
cors = CORS()

# --- ADDED: Rate Limiter ---
# Use get_remote_address as the key function
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)