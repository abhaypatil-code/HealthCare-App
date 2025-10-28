# HealthCare App/medml-backend/app/api/predict.py
from flask import jsonify, current_app
from . import api_bp
from app.models import db, Patient, RiskPrediction
from app.models import DiabetesAssessment, LiverAssessment, HeartAssessment, MentalHealthAssessment
from app.api.decorators import admin_required
from flask_jwt_extended import jwt_required
from app import services

def _map_risk_level(score: float) -> str:
    """Maps a prediction score (0.0 - 1.0) to Low, Medium, or High using app config."""
    thresholds = current_app.config.get('RISK_THRESHOLDS', {'medium': 0.35, 'high': 0.70})

    if score >= thresholds['high']:
        return 'High'
    elif score >= thresholds['medium']:
        return 'Medium'
    else:
        return 'Low'

def _run_and_save_prediction(patient_id: int, assessment_type: str):
    """
    Internal helper to run prediction and save results to the database.
    This is called by the assessment endpoints.
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        current_app.logger.warning(f"Prediction skipped: Patient {patient_id} not found.")
        return

    assessment = None
    input_data = {}
    
    try:
        # 1. Get the correct assessment model
        if assessment_type == 'diabetes':
            assessment = patient.diabetes_assessment
        elif assessment_type == 'liver':
            assessment = patient.liver_assessment
        elif assessment_type == 'heart':
            assessment = patient.heart_assessment
        elif assessment_type == 'mental_health':
            assessment = patient.mental_health_assessment
        
        if not assessment:
            current_app.logger.info(f"Prediction skipped: No {assessment_type} assessment for patient {patient_id}.")
            return

        # 2. Prepare the feature dictionary for the model
        input_data = assessment.to_dict()
        
        # 3. Add required Patient data (age, gender, bmi)
        #    This is critical as models depend on these.
        input_data['age'] = patient.age
        input_data['gender'] = patient.gender
        input_data['bmi'] = patient.bmi

        # 4. Run the prediction
        result = services.run_prediction(assessment_type, input_data)
        
        prediction_score = result.get('probability', 0.0)
        risk_level = _map_risk_level(prediction_score)
        
        # 5. Save the result
        # Find or create the patient's risk prediction record
        risk_record = patient.risk_prediction
        if not risk_record:
            risk_record = RiskPrediction(patient_id=patient_id)
            db.session.add(risk_record)
            
        # Update the specific fields for this assessment
        setattr(risk_record, f"{assessment_type}_score", prediction_score)
        setattr(risk_record, f"{assessment_type}_level", risk_level)
        
        # (Optional) Add model version tracking here if needed
        # risk_record.model_version = ...

        db.session.commit()
        current_app.logger.info(f"Successfully ran prediction for {assessment_type} for patient {patient_id}. Result: {risk_level}")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error during prediction for {assessment_type} for patient {patient_id}: {e}")

# This endpoint can be used for manual re-triggering if needed
@api_bp.route('/patients/<int:patient_id>/predict/<string:assessment_type>', methods=['POST'])
@jwt_required()
@admin_required
def trigger_prediction(patient_id, assessment_type):
    """
    [Admin Only] Manually triggers a prediction for a specific assessment.
    """
    if assessment_type not in ['diabetes', 'liver', 'heart', 'mental_health']:
        return jsonify(error="Invalid assessment type"), 400
    
    try:
        _run_and_save_prediction(patient_id, assessment_type)
        patient = Patient.query.get_or_404(patient_id)
        
        return jsonify(
            message=f"{assessment_type.capitalize()} prediction updated successfully",
            risk_prediction=patient.risk_prediction.to_dict()
        ), 200
    except Exception as e:
        current_app.logger.error(f"Failed to trigger prediction: {e}")
        return jsonify(error="Prediction failed", message=str(e)), 500