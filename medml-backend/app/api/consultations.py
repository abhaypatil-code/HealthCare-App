# HealthCare App/medml-backend/app/api/consultations.py
from flask import request, jsonify, current_app
from . import api_bp
from app.models import db, Patient, Consultation
from app.api.decorators import admin_required, get_current_admin_id
from pydantic import BaseModel, constr
from pydantic.error_wrappers import ValidationError
from flask_jwt_extended import jwt_required
from datetime import datetime
class ConsultationSchema(BaseModel):
    """ Validates consultation booking data """
    patient_id: int
    consultation_type: constr(pattern=r'^(Teleconsultation|In-Person)$')
    consultation_datetime_str: str # Expecting ISO format string e.g. "2025-10-30T10:00:00"
    notes: str | None = None

@api_bp.route('/consultations', methods=['POST'])
@jwt_required()
@admin_required
def book_consultation():
    """
    [Admin Only] Books a dummy consultation for a patient.
    Fulfills MVP: "Book dummy teleconsultation (medium risk) or in-person (high risk)"
    """
    try:
        data = ConsultationSchema(**request.json)
    except ValidationError as e:
        return jsonify(error="Validation Failed", messages=e.errors()), 422
    
    admin_id = get_current_admin_id()
    
    patient = Patient.query.get(data.patient_id)
    if not patient:
        return jsonify(error="Not Found", message="Patient not found"), 404

    try:
        consultation_dt = datetime.fromisoformat(data.consultation_datetime_str)
    except ValueError:
        return jsonify(error="Validation Failed", message="Invalid datetime format. Use ISO format."), 422

    new_consultation = Consultation(
        patient_id=data.patient_id,
        admin_id=admin_id,
        consultation_type=data.consultation_type,
        consultation_datetime=consultation_dt,
        notes=data.notes,
        status='Booked'
    )
    
    try:
        db.session.add(new_consultation)
        db.session.commit()
        current_app.logger.info(f"Admin {admin_id} booked {data.consultation_type} for patient {data.patient_id}")
        
        return jsonify(
            message="Consultation booked successfully", 
            consultation=new_consultation.to_dict()
        ), 201
    
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error booking consultation: {e}")
        return jsonify(error="Internal server error", message="Could not book consultation."), 500

@api_bp.route('/consultations/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
@admin_required
def get_patient_consultations(patient_id):
    """
    [Admin Only] Gets all consultations for a specific patient.
    """
    patient = Patient.query.get_or_404(patient_id)
    consultations = [c.to_dict() for c in patient.consultations]
    return jsonify(consultations=consultations), 200