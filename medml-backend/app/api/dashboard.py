# HealthCare App/medml-backend/app/api/dashboard.py
from flask import jsonify, current_app
from . import api_bp
from app.models import db, Patient, RiskPrediction
from app.api.decorators import admin_required
from flask_jwt_extended import jwt_required
from sqlalchemy import func, cast, Date
from datetime import date

@api_bp.route('/dashboard/stats', methods=['GET']) # Renamed route
@jwt_required()
@admin_required
def get_dashboard_stats(): # Renamed function
    """
    [Admin Only] Provides analytics for the admin dashboard.
    Returns counts as per frontend api_client.
    """
    try:
        # 1. Today's Registrations
        today = date.today()
        todays_registrations_count = db.session.query(func.count(Patient.id)).filter(
            cast(Patient.created_at, Date) == today
        ).scalar()

        # 2. Count by disease risk (Medium OR High)
        diabetes_risk_count = db.session.query(func.count(RiskPrediction.id)).filter(
            RiskPrediction.diabetes_risk_level.in_(['Medium', 'High'])
        ).scalar()
        
        liver_risk_count = db.session.query(func.count(RiskPrediction.id)).filter(
            RiskPrediction.liver_risk_level.in_(['Medium', 'High'])
        ).scalar()
        
        heart_risk_count = db.session.query(func.count(RiskPrediction.id)).filter(
            RiskPrediction.heart_risk_level.in_(['Medium', 'High'])
        ).scalar()
        
        mental_health_risk_count = db.session.query(func.count(RiskPrediction.id)).filter(
            RiskPrediction.mental_health_risk_level.in_(['Medium', 'High'])
        ).scalar()
        
        # Total registered patients
        total_patients_count = db.session.query(func.count(Patient.id)).scalar()

        # --- UPDATED: Flattened response for api_client ---
        stats_data = {
            "today_registrations": todays_registrations_count,
            "total_patients": total_patients_count,
            "diabetes_risk_count": diabetes_risk_count,
            "liver_risk_count": liver_risk_count,
            "heart_risk_count": heart_risk_count,
            "mental_health_risk_count": mental_health_risk_count
        }
        
        return jsonify(stats_data), 200 # Return flat JSON

    except Exception as e:
        current_app.logger.error(f"Error fetching dashboard stats: {e}")
        return jsonify(error="Internal server error"), 500