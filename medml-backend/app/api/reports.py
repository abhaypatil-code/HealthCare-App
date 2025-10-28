# HealthCare App/medml-backend/app/api/reports.py
from flask import request, jsonify, current_app, send_file
from . import api_bp
from app.models import db, Patient
from app.services import get_gemini_recommendations
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
        col_width = self.w / 4.5
        self.cell(col_width, 10, 'Disease', 1)
        self.cell(col_width, 10, 'Risk Level', 1)
        self.cell(col_width, 10, 'Score (0-1)', 1)
        self.ln()
        
        self.set_font('Arial', '', 10)
        if risk_data:
            data = [
                ('Diabetes', risk_data.diabetes_risk_level, risk_data.diabetes_risk_score),
                ('Liver Disease', risk_data.liver_risk_level, risk_data.liver_risk_score),
                ('Heart Disease', risk_data.heart_risk_level, risk_data.heart_risk_score),
                ('Mental Health', risk_data.mental_health_risk_level, risk_data.mental_health_risk_score),
            ]
            for row in data:
                self.cell(col_width, 10, str(row[0] or 'N/A'), 1)
                self.cell(col_width, 10, str(row[1] or 'N/A'), 1)
                self.cell(col_width, 10, str(round(row[2], 3) if row[2] is not None else 'N/A'), 1)
                self.ln()
        else:
            self.cell(col_width * 3, 10, 'No prediction data available.', 1)
            self.ln()
        self.ln(5)
        
    def add_recommendations(self, rec_data):
        self.set_font('Arial', '', 10)
        if not rec_data or all(not v for v in rec_data.values()):
            self.multi_cell(0, 5, "No specific recommendations available at this time.")
            return

        for category in ['Diet', 'Exercise', 'Sleep', 'Lifestyle']:
            recs = rec_data.get(category.lower(), [])
            if recs:
                self.set_font('Arial', 'B', 11)
                self.cell(0, 8, category, 0, 1)
                self.set_font('Arial', '', 10)
                for rec in recs:
                    disease = rec.get('disease_type', 'General')
                    text = rec.get('recommendation_text', 'No text.')
                    self.multi_cell(0, 5, f"- ({disease}) {text}")
                self.ln(3)

@api_bp.route('/patients/<int:patient_id>/report/pdf', methods=['POST'])
@jwt_required()
def download_patient_report(patient_id):
    """
    [Admin/Patient] Generates a PDF report for a patient based on
    selected sections from the frontend.
    """
    try:
        # 1. Check permissions
        jwt_identity = get_jwt_identity()
        user_role = jwt_identity.get('role')
        user_id = jwt_identity.get('id')
        
        if user_role == 'patient' and user_id != patient_id:
            return jsonify(error="Forbidden", message="Patients can only access their own report"), 403
        
        patient = Patient.query.get_or_404(patient_id)
        
        # --- UPDATED: Get sections list from frontend ---
        report_options = request.json or {}
        sections = report_options.get('sections', []) # e.g., ["Overview", "Diabetes"]
        
        if not sections:
             return jsonify(error="Bad Request", message="Please select at least one section to include."), 400

        # --- UPDATED: Get LATEST prediction ---
        risk_prediction = patient.risk_predictions.first()
        
        # 3. Generate PDF
        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 10)
        
        pdf.cell(0, 5, f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1)
        pdf.ln(5)

        # --- Section: Patient Info (Part of Overview) ---
        if "Overview" in sections:
            pdf.chapter_title('Patient Information')
            demo_data = {
                "Full Name": patient.name,
                "ABHA ID": "..." + patient.abha_id[-4:], # Mask ABHA ID
                "Age": patient.age,
                "Gender": patient.gender,
                "Height (cm)": patient.height,
                "Weight (kg)": patient.weight,
                "BMI": patient.bmi,
                "State": patient.state_name
            }
            pdf.chapter_body(demo_data)
            
            pdf.chapter_title('Overall Disease Risk Summary')
            pdf.risk_table(risk_prediction)
            
            # Also add lifestyle recs to overview
            pdf.chapter_title('Personalized Lifestyle Recommendations')
            risk_map = {}
            if risk_prediction:
                risk_map = {
                    'diabetes': risk_prediction.diabetes_risk_level,
                    'liver': risk_prediction.liver_risk_level,
                    'heart': risk_prediction.heart_risk_level,
                    'mental_health': risk_prediction.mental_health_risk_level
                }
            recommendations = get_gemini_recommendations(risk_map)
            pdf.add_recommendations(recommendations)

        # --- Section: Individual Diseases ---
        # (This is a simplified version; a full implementation would
        # add the factors and guidance from the frontend tabs)
        
        def add_disease_section(title, level, score):
            if title in sections and risk_prediction:
                pdf.add_page()
                pdf.chapter_title(f'{title} Risk Details')
                pdf.chapter_body({
                    "Risk Level": level or 'N/A',
                    "Risk Score": str(round(score, 3) if score is not None else 'N/A')
                })
                pdf.ln(5)
                # In a real report, we would add factors and specific recs here
                pdf.set_font('Arial', 'I', 10)
                pdf.multi_cell(0, 5, "Detailed contributing factors and guidance would be listed here.")
                pdf.ln(5)
        
        if risk_prediction:
            add_disease_section("Diabetes", risk_prediction.diabetes_risk_level, risk_prediction.diabetes_risk_score)
            add_disease_section("Liver", risk_prediction.liver_risk_level, risk_prediction.liver_risk_score)
            add_disease_section("Heart", risk_prediction.heart_risk_level, risk_prediction.heart_risk_score)
            add_disease_section("MentalHealth", risk_prediction.mental_health_risk_level, risk_prediction.mental_health_risk_score)

        # 4. Create in-memory file
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        pdf_buffer = BytesIO(pdf_bytes)
        
        current_app.logger.info(f"Generated PDF report for patient {patient_id}")

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f"Health_Report_{patient.abha_id}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        current_app.logger.error(f"Error generating PDF for patient {patient_id}: {e}")
        return jsonify(error="Internal server error", message="Could not generate PDF report."), 500