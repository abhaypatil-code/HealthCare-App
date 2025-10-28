# HealthCare App/medml-backend/app/api/predict.py
from flask import jsonify, current_app
from . import api_bp
from app.models import db, Patient, RiskPrediction
from app.services import run_prediction
from app.api.decorators import admin_required, get_current_admin_id
from flask_jwt_extended import jwt_required

def _run_and_save_prediction(patient_id):
    """
    Internal helper to run all predictions for a patient (based on latest
    assessments) and save a new prediction record.
    """
    patient = Patient.query.get_or_404(patient_id)
    if not patient:
        raise Exception("Patient not found")

    # --- UPDATED: Get features from latest assessments ---
    try:
        diabetes_data = patient.get_latest_diabetes_features()
        liver_data = patient.get_latest_liver_features()
        heart_data = patient.get_latest_heart_features()
        mental_health_data = patient.get_latest_mental_health_features()
    except ValueError as e:
        current_app.logger.error(f"Missing assessment for patient {patient_id}: {e}")
        raise Exception(f"Cannot run prediction: {e}")

    current_app.logger.info(f"Running all predictions for patient {patient_id}...")

    # --- 1. Run Predictions ---
    diabetes_score = run_prediction('diabetes', diabetes_data)
    liver_score = run_prediction('liver', liver_data)
    heart_score = run_prediction('heart', heart_data)
    mental_health_score = run_prediction('mental_health', mental_health_data)

    # --- 2. UPDATED: Always Create New Prediction Record (1:N) ---
    prediction = RiskPrediction(patient_id=patient_id)
    db.session.add(prediction)
    
    # --- 3. Save All Scores and Levels ---
    prediction.update_risk(
        model_key='diabetes', 
        score=diabetes_score,
        model_version='1.0' # Placeholder
    )
    prediction.update_risk(
        model_key='liver', 
        score=liver_score,
        model_version='1.0' # Placeholder
    )
    prediction.update_risk(
        model_key='heart', 
        score=heart_score,
        model_version='1.0' # Placeholder
    )
    prediction.update_risk(
        model_key='mental_health',
        score=mental_health_score, 
        model_version='1.0' # Placeholder
    )

    try:
        db.session.commit()
        current_app.logger.info(f"Successfully saved new prediction {prediction.id} for patient {patient_id}")
        return prediction
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error saving predictions for patient {patient_id}: {e}")
        raise Exception(f"Database error saving predictions: {e}")


@api_bp.route('/patients/<int:patient_id>/predict', methods=['POST'])
@jwt_required()
@admin_required
def trigger_all_predictions(patient_id):
    """
    [Admin Only] Triggers a full risk assessment for all 4 diseases.
    This is called by the "Finish Survey" button in the frontend.
    It creates a new RiskPrediction record.
    """
    try:
        prediction = _run_and_save_prediction(patient_id)
        return jsonify(
            message="Risk prediction completed successfully.",
            predictions=prediction.to_dict()
        ), 200
    except Exception as e:
        current_app.logger.error(f"Prediction trigger failed for patient {patient_id}: {e}")
        return jsonify(error="Prediction Failed", message=str(e)), 400 # 400 for bad request (e.g., missing assessment)

# --- ADDED: Endpoint for frontend client ---
@api_bp.route('/patients/<int:patient_id>/predictions/latest', methods=['GET'])
@jwt_required()
def get_latest_prediction(patient_id):
    """
    [Admin/Patient] Gets the single *most recent* risk prediction.
    This is required by the frontend's api_client.
    """
    # Check permissions
    from flask_jwt_extended import get_jwt_identity
    jwt_identity = get_jwt_identity()
    user_role = jwt_identity.get('role')
    user_id = jwt_identity.get('id')
    
    if user_role == 'patient' and user_id != patient_id:
        return jsonify(error="Forbidden", message="Patients can only access their own data"), 403

    patient = Patient.query.get_or_404(patient_id)
    
    # Get the first item from the ordered 1:N relationship
    latest_prediction = patient.risk_predictions.first()
    
    if not latest_prediction:
        return jsonify(error="Not Found", message="No predictions found for this patient"), 404
        
    return jsonify(latest_prediction.to_dict()), 200