# HealthCare App/medml-backend/app/api/reports.py
from flask import request, jsonify, current_app, send_file
from . import api_bp
from app.models import db, Patient, LifestyleRecommendation
from app.api.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from fpdf import FPDF
from io import BytesIO
from datetime import datetime

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Patient Health Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def chapter_body(self, data):
        self.set_font('Arial', '', 10)
        for key, val in data.items():
            self.multi_cell(0, 5, f"{key}: {val}")
        self.ln()

    def risk_table(self, risk_data):
        self.set_font('Arial', 'B', 10)
        self.cell(45, 10, 'Disease', 1)
        self.cell(45, 10, 'Risk Level', 1)
        self.cell(45, 10, 'Score', 1)
        self.ln()
        
        self.set_font('Arial', '', 10)
        if risk_data:
            data = [
                ('Diabetes', risk_data.diabetes_level, risk_data.diabetes_score),
                ('Liver', risk_data.liver_level, risk_data.liver_score),
                ('Heart', risk_data.heart_level, risk_data.heart_score),
                ('Mental Health', risk_data.mental_health_level, risk_data.mental_health_score),
            ]
            for row in data:
                self.cell(45, 10, str(row[0] or 'N/A'), 1)
                self.cell(45, 10, str(row[1] or 'N/A'), 1)
                self.cell(45, 10, str(round(row[2], 3) if row[2] is not None else 'N/A'), 1)
                self.ln()
        else:
            self.cell(135, 10, 'No prediction data available.', 1)
            self.ln()
        self.ln(5)


@api_bp.route('/reports/patient/<int:patient_id>/download', methods=['POST'])
@jwt_required()
def download_patient_report(patient_id):
    """
    [Admin/Patient] Generates a PDF report for a patient.
    Fulfills MVP: "Download/share profile (selective section export to PDF)"
    
    Admins can access any patient. Patients can only access their own.
    The POST body should contain which sections to include:
    {
        "include_demographics": true,
        "include_risk_summary": true,
        "include_recommendations": true
    }
    """
    try:
        # 1. Check permissions
        jwt_identity = get_jwt_identity()
        user_role = jwt_identity.get('role')
        user_id = jwt_identity.get('id')
        
        if user_role == 'patient' and user_id != patient_id:
            return jsonify(error="Forbidden", message="Patients can only access their own report"), 403
        
        patient = Patient.query.get_or_404(patient_id)
        
        # 2. Get section preferences from POST body
        report_options = request.json or {}
        include_demographics = report_options.get('include_demographics', True)
        include_risk_summary = report_options.get('include_risk_summary', True)
        include_recommendations = report_options.get('include_recommendations', True)
        
        # 3. Generate PDF
        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 10)
        
        pdf.cell(0, 5, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
        pdf.ln(5)

        # --- Section: Patient Demographics ---
        if include_demographics:
            pdf.chapter_title('Patient Information')
            demo_data = {
                "Full Name": patient.full_name,
                "ABHA ID": "..." + patient.abha_id[-4:], # Mask ABHA ID
                "Age": patient.age,
                "Gender": patient.gender,
                "Height (cm)": patient.height_cm,
                "Weight (kg)": patient.weight_kg,
                "BMI": patient.bmi,
                "State": patient.state_name
            }
            pdf.chapter_body(demo_data)

        # --- Section: Risk Summary ---
        if include_risk_summary:
            pdf.chapter_title('Disease Risk Summary')
            pdf.risk_table(patient.risk_prediction)

        # --- Section: Lifestyle Recommendations ---
        if include_recommendations and patient.risk_prediction:
            pdf.chapter_title('Lifestyle Recommendations')
            
            # Fetch relevant recommendations
            risk_map = {
                'diabetes': patient.risk_prediction.diabetes_level,
                'liver': patient.risk_prediction.liver_level,
                'heart': patient.risk_prediction.heart_level,
                'mental_health': patient.risk_prediction.mental_health_level
            }
            filters = []
            for disease, level in risk_map.items():
                if level in ['Medium', 'High']:
                    filters.append(
                        (LifestyleRecommendation.disease_type == disease) &
                        (LifestyleRecommendation.risk_level == level)
                    )
            
            if filters:
                from sqlalchemy import or_
                recommendations = db.session.query(LifestyleRecommendation).filter(or_(*filters)).all()
            else:
                recommendations = db.session.query(LifestyleRecommendation).filter(
                    LifestyleRecommendation.risk_level == 'Low'
                ).all()

            if not recommendations:
                pdf.multi_cell(0, 5, "No specific recommendations available at this time.")
            else:
                for rec in recommendations:
                    pdf.set_font('Arial', 'B', 10)
                    pdf.multi_cell(0, 5, f"[{rec.disease_type.capitalize()} - {rec.category.capitalize()}]")
                    pdf.set_font('Arial', '', 10)
                    pdf.multi_cell(0, 5, rec.recommendation_text)
                    pdf.ln(2)
            pdf.ln(5)

        # 4. Create in-memory file
        pdf_buffer = BytesIO()
        pdf.output(pdf_buffer)
        pdf_buffer.seek(0)
        
        current_app.logger.info(f"Generated PDF report for patient {patient_id}")

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"Patient_Report_{patient.abha_id}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        current_app.logger.error(f"Error generating PDF for patient {patient_id}: {e}")
        return jsonify(error="Internal server error", message="Could not generate PDF report."), 500