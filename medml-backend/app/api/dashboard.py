# HealthCare App/medml-backend/app/api/dashboard.py
from flask import jsonify, current_app
from . import api_bp
from app.models import db, Patient, RiskPrediction
from app.api.decorators import admin_required
from flask_jwt_extended import jwt_required
from sqlalchemy import func, cast, Date
from datetime import date

@api_bp.route('/dashboard/analytics', methods=['GET'])
@jwt_required()
@admin_required
def get_dashboard_analytics():
    """
    [Admin Only] Provides analytics for the admin dashboard.
    Fulfills MVP: "Metrics: Today’s registrations + count by disease risk"
    """
    try:
        # 1. Today's Registrations
        today = date.today()
        todays_registrations_count = db.session.query(func.count(Patient.id)).filter(
            cast(Patient.created_at, Date) == today
        ).scalar()

        # 2. Count by disease risk (High risk only)
        # This provides a count of patients marked as 'High' risk for each disease
        risk_counts = {
            'diabetes_high': db.session.query(func.count(RiskPrediction.id)).filter(
                RiskPrediction.diabetes_level == 'High'
            ).scalar(),
            
            'liver_high': db.session.query(func.count(RiskPrediction.id)).filter(
                RiskPrediction.liver_level == 'High'
            ).scalar(),
            
            'heart_high': db.session.query(func.count(RiskPrediction.id)).filter(
                RiskPrediction.heart_level == 'High'
            ).scalar(),
            
            'mental_health_high': db.session.query(func.count(RiskPrediction.id)).filter(
                RiskPrediction.mental_health_level == 'High'
            ).scalar(),
        }
        
        # Total registered patients
        total_patients_count = db.session.query(func.count(Patient.id)).scalar()

        analytics_data = {
            "todays_registrations": todays_registrations_count,
            "total_patients": total_patients_count,
            "risk_counts": risk_counts
        }
        
        return jsonify(analytics=analytics_data), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching dashboard analytics: {e}")
        return jsonify(error="Internal server error"), 500