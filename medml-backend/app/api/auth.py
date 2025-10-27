# HealthCare App/medml-backend/app/api/auth.py
from flask import request, jsonify, abort, current_app
from . import api_bp
from app.models import User, Patient
from app.extensions import db
from app.schemas import UserRegisterSchema, UserLoginSchema, PatientLoginSchema
from pydantic import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@api_bp.route('/auth/admin/register', methods=['POST'])
def register_admin():
    """
    Registers a new Admin (Healthcare Worker).
    """
    try:
        data = UserRegisterSchema(**request.json)
    except ValidationError as e:
        return jsonify(error="Validation Failed", messages=e.errors()), 422

    if User.query.filter_by(email=data.email).first():
        return jsonify(error="Email already exists"), 422

    new_user = User(
        name=data.name,
        email=data.email,
        designation=data.designation,
        contact_number=data.contact_number,
        role='admin' # Enforce admin role
    )
    new_user.set_password(data.password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error registering admin: {e}")
        return jsonify(error="Database error", message="Could not register admin."), 500

    current_app.logger.info(f"New admin registered: {new_user.email}")
    return jsonify(message="Admin registered successfully", user=new_user.to_dict()), 201

@api_bp.route('/auth/admin/login', methods=['POST'])
def login_admin():
    """
    Logs in an Admin (Healthcare Worker).
    """
    try:
        data = UserLoginSchema(**request.json)
    except ValidationError as e:
        return jsonify(error="Validation Failed", messages=e.errors()), 422

    user = User.query.filter_by(email=data.email).first()

    if user and user.check_password(data.password):
        # Create token with role identity
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        current_app.logger.info(f"Admin login successful: {user.email}")
        return jsonify(access_token=access_token), 200
    
    current_app.logger.warning(f"Failed admin login attempt for email: {data.email}")
    return jsonify(error="Invalid credentials"), 401

@api_bp.route('/auth/patient/login', methods=['POST'])
def login_patient():
    """
    Logs in a Patient using ABHA ID and password as per MVP.
    """
    try:
        data = PatientLoginSchema(**request.json)
    except ValidationError as e:
        return jsonify(error="Validation Failed", messages=e.errors()), 422

    patient = Patient.query.filter_by(abha_id=data.abha_id).first()

    if patient and patient.check_password(data.password):
        # Create token with role identity
        access_token = create_access_token(identity={"id": patient.id, "role": "patient"})
        current_app.logger.info(f"Patient login successful: {patient.abha_id}")
        return jsonify(access_token=access_token), 200
    
    current_app.logger.warning(f"Failed patient login attempt for ABHA ID: {data.abha_id}")
    return jsonify(error="Invalid credentials"), 401


@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_me():
    """
    Returns the profile of the currently authenticated user (Admin or Patient).
    """
    try:
        jwt_identity = get_jwt_identity()
        user_id = jwt_identity.get('id')
        user_role = jwt_identity.get('role')

        if not user_id or not user_role:
            return jsonify(error="Invalid token identity"), 401

        if user_role == 'admin':
            user = User.query.get_or_404(user_id)
            return jsonify(user.to_dict()), 200
        elif user_role == 'patient':
            patient = Patient.query.get_or_404(user_id)
            # Return patient data, including assessments and predictions
            return jsonify(patient.to_dict(include_assessments=True, include_predictions=True)), 200
        
        return jsonify(error="Unknown user role"), 401
        
    except Exception as e:
        current_app.logger.error(f"Error in /me endpoint: {e}")
        return jsonify(error="Internal server error"), 500