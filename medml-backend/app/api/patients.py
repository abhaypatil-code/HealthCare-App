# HealthCare App/medml-backend/app/api/patients.py
from flask import request, jsonify, current_app
from . import api_bp
from app.models import db, Patient, User
from app.schemas import PatientCreateSchema
from app.api.decorators import admin_required, get_current_admin_id
from pydantic import ValidationError
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

@api_bp.route('/patients', methods=['POST'])
@jwt_required()
@admin_required
def create_patient():
    """
    [Admin Only] Creates a new patient record.
    Fulfills MVP: Admin adds patient info (name, age, sex, height, weight, state, ABHA ID).
    """
    try:
        # Validate incoming data against the schema
        data = PatientCreateSchema(**request.json)
    except ValidationError as e:
        return jsonify(error="Validation Failed", messages=e.errors()), 422
    
    admin_id = get_current_admin_id()
    
    # MVP Requirement: Check for existing ABHA ID
    if Patient.query.filter_by(abha_id=data.abha_id).first():
        return jsonify(error="Conflict", message="Patient with this ABHA ID already exists"), 409

    new_patient = Patient(
        full_name=data.full_name,
        age=data.age,
        gender=data.gender,
        height_cm=data.height_cm,
        weight_kg=data.weight_kg,
        abha_id=data.abha_id,
        state_name=data.state_name,
        created_by_user_id=admin_id
    )
    # Admin sets the patient's initial password for their login
    new_patient.set_password(data.password) 

    try:
        db.session.add(new_patient)
        db.session.commit()
        current_app.logger.info(f"Admin {admin_id} created patient {new_patient.id} with ABHA ID {new_patient.abha_id}")
        
        # Return full patient data, including auto-calculated BMI
        return jsonify(message="Patient created successfully", patient=new_patient.to_dict()), 201
    
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(f"IntegrityError creating patient: {e}")
        return jsonify(error="Database error", message="Could not create patient. ABHA ID may be taken."), 409
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating patient: {e}")
        return jsonify(error="Internal server error", message="An unexpected error occurred."), 500

@api_bp.route('/patients', methods=['GET'])
@jwt_required()
@admin_required
def get_patients():
    """
    [Admin Only] Gets a list of all patients.
    Fulfills MVP: View Registered Patients, with filtering.
    """
    try:
        query = Patient.query
        
        # MVP Requirement: Filter by risk
        risk_filter = request.args.get('risk_filter') # 'diabetes', 'liver', 'heart', 'mental_health'
        risk_level = request.args.get('risk_level') # 'Low', 'Medium', 'High'
        
        if risk_filter and risk_level:
            from app.models import RiskPrediction
            query = query.join(RiskPrediction)
            
            if risk_filter == 'diabetes':
                query = query.filter(RiskPrediction.diabetes_level == risk_level)
            elif risk_filter == 'liver':
                query = query.filter(RiskPrediction.liver_level == risk_level)
            elif risk_filter == 'heart':
                query = query.filter(RiskPrediction.heart_level == risk_level)
            elif risk_filter == 'mental_health':
                query = query.filter(RiskPrediction.mental_health_level == risk_level)

        # MVP Requirement: Sorting by recency (default)
        sort_by = request.args.get('sort_by', 'recency')
        if sort_by == 'recency':
            query = query.order_by(Patient.created_at.desc())
        # Add other sorting logic here if needed (e.g., 'risk_level')

        patients = query.all()
        
        # Return list of patients, including their prediction data for the dashboard view
        patients_data = [p.to_dict(include_predictions=True) for p in patients]
        
        return jsonify(patients=patients_data), 200
    
    except Exception as e:
        current_app.logger.error(f"Error fetching patients: {e}")
        return jsonify(error="Internal server error"), 500


@api_bp.route('/patients/<int:patient_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_patient(patient_id):
    """
    [Admin Only] Gets detailed info for a single patient.
    Fulfills MVP: Patient Detail Page
    """
    patient = Patient.query.get_or_404(patient_id)
    
    # Return full details including all assessments and predictions
    return jsonify(patient.to_dict(include_assessments=True, include_predictions=True)), 200


@api_bp.route('/patients/<int:patient_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_patient(patient_id):
    """
    [Admin Only] Updates a patient's basic info.
    Fulfills MVP: Edit patient details.
    """
    patient = Patient.query.get_or_404(patient_id)
    data = request.json

    try:
        # Update mutable fields
        patient.full_name = data.get('full_name', patient.full_name)
        patient.age = data.get('age', patient.age)
        patient.gender = data.get('gender', patient.gender)
        patient.state_name = data.get('state_name', patient.state_name)

        # MVP Requirement: Auto-BMI recalculation on data updates.
        patient.height_cm = data.get('height_cm', patient.height_cm)
        patient.weight_kg = data.get('weight_kg', patient.weight_kg)
        
        # Note: ABHA ID and password changes are *not* included in this
        # simple update endpoint for security.

        db.session.commit()
        current_app.logger.info(f"Patient {patient_id} updated by admin {get_current_admin_id()}")
        
        # Return updated data, which will include the new BMI
        return jsonify(message="Patient updated successfully", patient=patient.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating patient {patient_id}: {e}")
        return jsonify(error="Internal server error"), 500