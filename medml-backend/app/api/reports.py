# HealthCare App/medml-backend/app/api/reports.py
from flask import request, jsonify, current_app, send_file
from . import api_bp
from app.models import Patient
from app.extensions import db
from app.services import get_gemini_recommendations
from app.api.decorators import admin_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from fpdf import FPDF
from io import BytesIO
from datetime import datetime
from .responses import forbidden, bad_request, server_error

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(15, 15, 15)  # Left, Top, Right margins
    
    def header(self):
        # Header with logo and title
        self.set_font('Arial', 'B', 16)
        self.set_text_color(37, 99, 235)  # Blue color
        self.cell(0, 12, 'HealthCare System', 0, 1, 'C')
        
        self.set_font('Arial', 'B', 14)
        self.set_text_color(0, 0, 0)  # Black
        self.cell(0, 8, 'Patient Health Report', 0, 1, 'C')
        
        # Add a line separator
        self.set_draw_color(37, 99, 235)
        self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Page {self.page_no()} | Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(37, 99, 235)  # Blue color
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def chapter_body(self, data):
        self.set_font('Arial', '', 10)
        for key, val in data.items():
            # Ensure text fits within page width
            text = f"{key}: {val}"
            self.multi_cell(0, 5, text, 0, 'L', False)
        self.ln()
        
    def risk_table(self, risk_data):
        """Create a risk assessment table that ensures it stays on a single page."""
        # Calculate required space for the table
        table_height = 10 + (5 * 10) + 5  # Header + 5 rows + spacing
        
        # Check if we need a new page to fit the table
        if self.get_y() + table_height > self.h - 20:  # Leave margin for footer
            self.add_page()
        
        # Table title
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, 'Disease Risk Assessment Scores', 0, 1, 'C')
        self.ln(3)
        
        # Table header
        self.set_font('Arial', 'B', 10)
        col_width = self.w / 4.5
        self.cell(col_width, 10, 'Disease', 1, 0, 'C')
        self.cell(col_width, 10, 'Risk Level', 1, 0, 'C')
        self.cell(col_width, 10, 'Score (0-1)', 1, 0, 'C')
        self.ln()
        
        # Table data
        self.set_font('Arial', '', 10)
        if risk_data:
            data = [
                ('Diabetes', risk_data.diabetes_risk_level, risk_data.diabetes_risk_score),
                ('Liver Disease', risk_data.liver_risk_level, risk_data.liver_risk_score),
                ('Heart Disease', risk_data.heart_risk_level, risk_data.heart_risk_score),
                ('Mental Health', risk_data.mental_health_risk_level, risk_data.mental_health_risk_score),
            ]
            for row in data:
                # Format risk level with color coding
                risk_level = str(row[1] or 'N/A')
                if risk_level == 'High':
                    self.set_text_color(220, 20, 60)  # Red
                elif risk_level == 'Medium':
                    self.set_text_color(255, 140, 0)  # Orange
                elif risk_level == 'Low':
                    self.set_text_color(34, 139, 34)  # Green
                else:
                    self.set_text_color(0, 0, 0)  # Black
                
                self.cell(col_width, 10, str(row[0] or 'N/A'), 1, 0, 'C')
                self.cell(col_width, 10, risk_level, 1, 0, 'C')
                self.cell(col_width, 10, str(round(row[2], 3) if row[2] is not None else 'N/A'), 1, 0, 'C')
                self.ln()
                
                # Reset text color
                self.set_text_color(0, 0, 0)
        else:
            self.cell(col_width * 3, 10, 'No prediction data available.', 1, 0, 'C')
            self.ln()
        
        self.ln(8)  # Extra spacing after table
        
    def add_recommendations(self, rec_data):
        """Add lifestyle recommendations with improved formatting."""
        self.set_font('Arial', 'B', 12)
        self.set_text_color(37, 99, 235)  # Blue color
        self.cell(0, 8, 'Lifestyle Recommendations', 0, 1, 'L')
        self.ln(3)
        
        self.set_font('Arial', '', 10)
        self.set_text_color(0, 0, 0)  # Reset to black
        
        if not rec_data or all(not v for v in rec_data.values()):
            self.multi_cell(0, 5, "No specific recommendations available at this time.")
            return

        for category in ['Diet', 'Exercise', 'Sleep', 'Lifestyle']:
            recs = rec_data.get(category.lower(), [])
            if recs:
                # Category header without emoji icons (to avoid Unicode issues)
                self.set_font('Arial', 'B', 11)
                self.set_text_color(37, 99, 235)  # Blue color
                self.cell(0, 8, f"{category}", 0, 1, 'L')
                
                self.set_font('Arial', '', 10)
                self.set_text_color(0, 0, 0)  # Reset to black
                
                for rec in recs:
                    disease = rec.get('disease_type', 'General')
                    text = rec.get('recommendation_text', 'No text.')
                    risk_level = rec.get('risk_level', 'Medium')
                    
                    # Color code based on risk level
                    if risk_level == 'High':
                        self.set_text_color(220, 20, 60)  # Red
                    elif risk_level == 'Medium':
                        self.set_text_color(255, 140, 0)  # Orange
                    else:
                        self.set_text_color(0, 0, 0)  # Black
                    
                    # Ensure text fits within page width and handle long text
                    recommendation_text = f"- ({disease}) {text}"
                    self.multi_cell(0, 5, recommendation_text, 0, 'L', False)
                    self.set_text_color(0, 0, 0)  # Reset to black
                
                self.ln(3)

@api_bp.route('/patients/<int:patient_id>/report/pdf', methods=['POST'])
@jwt_required()
def download_patient_report(patient_id):
    """
    [Admin/Patient] Generates a text report for a patient based on
    selected sections from the frontend.
    """
    try:
        # 1. Check permissions
        from .decorators import parse_jwt_identity
        jwt_identity = parse_jwt_identity()
        user_role = jwt_identity.get('role')
        user_id = jwt_identity.get('id')
        
        if user_role == 'patient' and user_id != patient_id:
            return forbidden("Patients can only access their own report")
        
        patient = Patient.query.get_or_404(patient_id)
        
        # --- UPDATED: Get sections list from frontend ---
        report_options = request.json or {}
        sections = report_options.get('sections', []) # e.g., ["Overview", "Diabetes"]
        
        if not sections:
            return bad_request("Please select at least one section to include.")

        # --- UPDATED: Get LATEST prediction ---
        risk_prediction = patient.risk_predictions.first()
        
        # 3. Generate PDF report
        pdf = PDF()
        pdf.add_page()

        # Section: Overview
        if "Overview" in sections:
            pdf.chapter_title("Patient Information")
            overview_data = {
                "Name": patient.name,
                "Age": patient.age,
                "Gender": patient.gender,
                "Height": f"{patient.height} cm",
                "Weight": f"{patient.weight} kg",
                "BMI": patient.bmi,
                "State": patient.state_name,
                "Generated": datetime.now().strftime('%Y-%m-%d %H:%M')
            }
            pdf.chapter_body(overview_data)

            # Risk table for overview
            pdf.risk_table(risk_prediction)

        # Optional disease-specific sections: render headers if selected
        section_map = [
            ("Diabetes", "Diabetes"),
            ("Liver", "Liver Disease"),
            ("Heart", "Heart Disease"),
            ("Mental Health", "Mental Health")
        ]

        if any(sec in sections for sec, _ in section_map):
            # Ensure risk table already shows overall numbers; can add small notes per disease
            for sec_key, sec_title in section_map:
                if sec_key in sections:
                    pdf.chapter_title(f"{sec_title} Details")
                    if risk_prediction:
                        level = getattr(risk_prediction, f"{sec_key.lower().replace(' ', '_')}_risk_level", None)
                        score = getattr(risk_prediction, f"{sec_key.lower().replace(' ', '_')}_risk_score", None)
                        pdf.chapter_body({
                            "Risk Level": level or 'N/A',
                            "Risk Score": round(score, 3) if score is not None else 'N/A'
                        })
                    else:
                        pdf.chapter_body({"Info": "No prediction data available."})

        # Recommendations section
        try:
            if risk_prediction:
                risk_map = {
                    'diabetes': risk_prediction.diabetes_risk_level,
                    'liver': risk_prediction.liver_risk_level,
                    'heart': risk_prediction.heart_risk_level,
                    'mental_health': risk_prediction.mental_health_risk_level
                }
                recs = get_gemini_recommendations(risk_map)
            else:
                recs = {"diet": [], "exercise": [], "sleep": [], "lifestyle": []}
        except Exception as e:
            current_app.logger.warning(f"Failed to get AI recommendations: {e}")
            recs = {"diet": [], "exercise": [], "sleep": [], "lifestyle": []}

        pdf.add_recommendations(recs)

        # Output PDF to bytes
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        buffer = BytesIO(pdf_bytes)

        current_app.logger.info(f"Generated PDF report for patient {patient_id}")

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"Health_Report_{patient.abha_id}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        current_app.logger.error(f"Error generating report for patient {patient_id}: {e}")
        return server_error("Could not generate report.")


# --- Share Details Endpoint ---
@api_bp.route('/patients/<int:patient_id>/share', methods=['POST'])
@jwt_required()
def share_patient_details(patient_id):
    """
    [Admin/Patient] Generates a shareable link with selected sections.
    MVP: returns a dummy URL containing a short token; frontend handles link display.
    """
    try:
        from .decorators import parse_jwt_identity
        jwt_identity = parse_jwt_identity()
        user_role = jwt_identity.get('role')
        user_id = jwt_identity.get('id')

        if user_role == 'patient' and user_id != patient_id:
            return forbidden("Patients can only share their own details")

        # Validate patient exists
        _ = Patient.query.get_or_404(patient_id)

        payload = request.json or {}
        sections = payload.get('sections', [])
        if not sections:
            return bad_request("Please select at least one section to share.")

        # Create a lightweight, non-persistent token
        import secrets
        token = secrets.token_urlsafe(8)
        share_url = f"https://healthcare-app.local/share/{patient_id}/{','.join(sections)}?t={token}"

        return jsonify({"share_url": share_url}), 200
    except Exception as e:
        current_app.logger.error(f"Error generating share link for patient {patient_id}: {e}")
        return server_error("Could not generate share link.")

    