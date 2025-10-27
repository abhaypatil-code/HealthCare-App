# HealthCare App/medml-backend/app/api/assessments.py
from flask import request, jsonify, current_app
from . import api_bp
from app.models import db, Patient
from app.models import DiabetesAssessment, LiverAssessment, HeartAssessment, MentalHealthAssessment
from app.schemas import (
    DiabetesAssessmentSchema, LiverAssessmentSchema, 
    HeartAssessmentSchema, MentalHealthAssessmentSchema
)
from app.api.decorators import admin_required, get_current_admin_id
from pydantic import ValidationError
from flask_jwt_extended import jwt_required
from .predict import _run_and_save_prediction  # <-- IMPORT PREDICTION HELPER

def _create_or_update_assessment(patient_id, AssessmentModel, SchemaModel, assessment_type_key):
    """
    Internal helper function to create or update an assessment for a patient.
    Fulfills MVP: "save independently"
    FIX: Now also triggers prediction automatically.
    """
    patient = Patient.query.get_or_404(patient_id)
    
    try:
        # Validate incoming JSON data
        data = SchemaModel(**request.json)
    except ValidationError as e:
        return jsonify(error="Validation Failed", messages=e.errors()), 422

    # Find existing assessment or create a new one (1:1 relationship)
    assessment = AssessmentModel.query.filter_by(patient_id=patient_id).first()
    
    if not assessment:
        assessment = AssessmentModel(patient_id=patient_id, **data.model_dump())
        db.session.add(assessment)
        message = f"{AssessmentModel.__name__} created successfully"
        status_code = 201
    else:
        # Update existing assessment fields
        for key, value in data.model_dump().items():
            setattr(assessment, key, value)
        message = f"{AssessmentModel.__name__} updated successfully"
        status_code = 200

    try:
        db.session.commit()
        current_app.logger.info(f"{message} for patient {patient_id} by admin {get_current_admin_id()}")
        
        # --- MVP REQUIREMENT: Trigger Prediction ---
        # After saving the assessment, trigger the ML prediction
        try:
            _run_and_save_prediction(patient_id, assessment_type_key)
        except Exception as pred_e:
            # Log the prediction error, but don't fail the assessment save
            current_app.logger.error(f"Prediction trigger failed for {assessment_type_key} on patient {patient_id}: {pred_e}")
        # --- End Prediction Trigger ---

        # Return the *full* patient object, including all assessments AND predictions
        return jsonify(
            message=message, 
            patient=patient.to_dict(include_assessments=True, include_predictions=True)
        ), status_code
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error saving {AssessmentModel.__name__} for patient {patient_id}: {e}")
        return jsonify(error="Internal server error"), 500

# --- Public API Endpoints ---

@api_bp.route('/patients/<int:patient_id>/assessments/diabetes', methods=['POST'])
@jwt_required()
@admin_required
def submit_diabetes_assessment(patient_id):
    """
    [Admin Only] Creates or updates the diabetes assessment for a patient.
    """
    return _create_or_update_assessment(patient_id, DiabetesAssessment, DiabetesAssessmentSchema, 'diabetes')

@api_bp.route('/patients/<int:patient_id>/assessments/liver', methods=['POST'])
@jwt_required()
@admin_required
def submit_liver_assessment(patient_id):
    """
    [Admin Only] Creates or updates the liver assessment for a patient.
    """
    return _create_or_update_assessment(patient_id, LiverAssessment, LiverAssessmentSchema, 'liver')

@api_bp.route('/patients/<int:patient_id>/assessments/heart', methods=['POST'])
@jwt_required()
@admin_required
def submit_heart_assessment(patient_id):
    """
    [Admin Only] Creates or updates the heart assessment for a patient.
    """
    return _create_or_update_assessment(patient_id, HeartAssessment, HeartAssessmentSchema, 'heart')

@api_bp.route('/patients/<int:patient_id>/assessments/mental_health', methods=['POST'])
@jwt_required()
@admin_required
def submit_mental_health_assessment(patient_id):
    """
    [Admin Only] Creates or updates the mental health assessment for a patient.
    """
    return _create_or_update_assessment(patient_id, MentalHealthAssessment, MentalHealthAssessmentSchema, 'mental_health')

@api_bp.route('/patients/<int:patient_id>/assessments', methods=['GET'])
@jwt_required()
@admin_required
def get_all_assessments(patient_id):
    """
    [Admin Only] Gets the status of all 4 assessments for a single patient.
    """
    patient = Patient.query.get_or_404(patient_id)
    
    assessments_data = {
        "diabetes": patient.diabetes_assessment.to_dict() if patient.diabetes_assessment else None,
        "liver": patient.liver_assessment.to_dict() if patient.liver_assessment else None,
        "heart": patient.heart_assessment.to_dict() if patient.heart_assessment else None,
        "mental_health": patient.mental_health_assessment.to_dict() if patient.mental_health_assessment else None,
    }
    
    return jsonify(patient_id=patient_id, assessments=assessments_data), 200