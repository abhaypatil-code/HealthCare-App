# HealthCare App/medml-backend/app/api/recommendations.py
from flask import jsonify, current_app, request
from . import api_bp
from app.models import db, LifestyleRecommendation, Patient
from app.api.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity

@api_bp.route('/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    """
    [Admin/Patient] Fetches lifestyle recommendations based on risk.
    Fulfills MVP: "Lifestyle recommendations (diet, exercise, sleep, habits)"
    
    This implementation fetches *static* recommendations from the DB
    based on the patient's *highest* risk level.
    
    Query params (for Admin): ?patient_id=<id>
    No params (for Patient): Fetches for the logged-in patient.
    """
    try:
        patient = None
        jwt_identity = get_jwt_identity()
        user_role = jwt_identity.get('role')

        if user_role == 'admin':
            patient_id = request.args.get('patient_id')
            if not patient_id:
                return jsonify(error="Bad Request", message="patient_id query parameter is required for admins"), 400
            patient = Patient.query.get_or_404(patient_id)
        
        elif user_role == 'patient':
            patient_id = jwt_identity.get('id')
            patient = Patient.query.get_or_404(patient_id)
        
        if not patient:
            return jsonify(error="Not Found", message="Patient not found"), 404

        risk_prediction = patient.risk_prediction
        if not risk_prediction:
            # No predictions yet, return empty list
            return jsonify(recommendations=[]), 200

        # Find all recommendations that match the patient's risk levels
        risk_map = {
            'diabetes': risk_prediction.diabetes_level,
            'liver': risk_prediction.liver_level,
            'heart': risk_prediction.heart_level,
            'mental_health': risk_prediction.mental_health_level
        }

        # Create a query to find recommendations for any of the patient's conditions
        # We only fetch recommendations for 'Medium' or 'High' risk levels
        recommendations_query = db.session.query(LifestyleRecommendation).filter(
            LifestyleRecommendation.risk_level.in_(['Medium', 'High'])
        )

        # Filter by the specific disease/risk combinations
        filters = []
        for disease, level in risk_map.items():
            if level in ['Medium', 'High']:
                filters.append(
                    (LifestyleRecommendation.disease_type == disease) &
                    (LifestyleRecommendation.risk_level == level)
                )
        
        if not filters:
            # If no medium/high risks, fetch 'Low' risk (general) recommendations
            recommendations = db.session.query(LifestyleRecommendation).filter(
                LifestyleRecommendation.risk_level == 'Low'
            ).all()
        else:
            # Combine filters with an OR condition
            from sqlalchemy import or_
            recommendations = recommendations_query.filter(or_(*filters)).all()

        
        recommendations_data = [
            {
                "id": rec.id,
                "disease_type": rec.disease_type,
                "risk_level": rec.risk_level,
                "recommendation_text": rec.recommendation_text,
                "category": rec.category # <-- ADDED 'category' based on MVP
            }
            for rec in recommendations
        ]

        return jsonify(recommendations=recommendations_data), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching recommendations: {e}")
        return jsonify(error="Internal server error", message=str(e)), 500