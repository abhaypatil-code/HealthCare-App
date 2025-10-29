import streamlit as st
import api_client
import utils
import pandas as pd
from datetime import datetime, timedelta
from theme import apply_light_theme, create_navbar, create_metric_card

st.set_page_config(
    page_title="Patient Dashboard", 
    layout="wide",
    page_icon="👤"
)

# Apply enhanced light theme with compact spacing
apply_light_theme()

utils.check_login(role="patient")

# Create top navigation bar
create_navbar(st.session_state.user_name, st.session_state.user_role)

# --- State Management ---
if "patient_view" not in st.session_state:
    st.session_state.patient_view = "overview"  # overview, diabetes, liver, heart, mental_health

# Get patient data with feedback
with st.spinner("Loading your data..."):
    patient_data = api_client.get_patient_details(st.session_state.user_id)
    risk_data = api_client.get_latest_prediction(st.session_state.user_id)
    recommendations = api_client.get_recommendations(st.session_state.user_id)

if not patient_data:
    st.error("Failed to load patient data.")
    st.stop()

# --- Compact Top Navigation ---
st.markdown("""
<div class="navbar" style="margin-bottom: 1rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; max-width: 1200px; margin: 0 auto; padding: 0 1rem;">
        <div style="display: flex; gap: 1rem; align-items: center;">
            <h2 style="margin: 0; color: var(--primary-color); font-size: 1.5rem;">👤 Patient Portal</h2>
        </div>
        <div style="display: flex; gap: 0.75rem; align-items: center;">
            <span style="color: var(--text-secondary); font-size: 0.9rem;">Welcome, {st.session_state.user_name}!</span>
            <button onclick="window.location.href='app.py'" style="background: var(--error-color); color: white; border: none; padding: 0.4rem 0.8rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem;">Logout</button>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

tab_labels = ["📊 Overview", "🩺 Diabetes", "🫀 Liver", "❤️ Heart", "🧠 Mental Health"]
tabs = st.tabs(tab_labels)

# --- Main Content Area ---

# --- View: Overview ---
with tabs[0]:
    st.markdown('<h1 style="margin-bottom: 0.5rem; font-size: 1.8rem;">📊 Health Overview</h1>', unsafe_allow_html=True)
    
    # Enhanced Health Metrics Display
    st.markdown('<h3 style="margin-bottom: 0.75rem; font-size: 1.2rem;">📏 Health Metrics</h3>', unsafe_allow_html=True)
    
    # Create styled metric cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card(
            "BMI", 
            f"{patient_data.get('bmi', 0):.1f}", 
            "Body Mass Index",
            "primary"
        )
    with col2:
        create_metric_card(
            "Height", 
            f"{patient_data.get('height', 0):.0f} cm", 
            "Height in centimeters",
            "secondary"
        )
    with col3:
        create_metric_card(
            "Weight", 
            f"{patient_data.get('weight', 0):.1f} kg", 
            "Weight in kilograms",
            "success"
        )
    
    st.markdown('<hr style="margin: 0.75rem 0;">', unsafe_allow_html=True)
    
    # Disease Risk Assessment Table
    st.markdown('<h3 style="margin-bottom: 0.75rem; font-size: 1.2rem;">🚨 Disease Risk Assessment</h3>', unsafe_allow_html=True)
    utils.display_risk_table(risk_data)
    
    # Retry Prediction Section (if no risk data available)
    if not risk_data:
        st.warning("⚠️ No risk assessment data available. Contact your healthcare worker to complete assessments.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Request New Assessment", use_container_width=True, type="secondary"):
                st.info("📞 Please contact your healthcare worker to schedule a new assessment.")
        with col2:
            if st.button("📊 View Assessment History", use_container_width=True):
                st.info("📋 Assessment history will be displayed here once assessments are completed.")
    
    st.markdown('<hr style="margin: 0.75rem 0;">', unsafe_allow_html=True)
    
    # Assessment History Section
    st.markdown('<h3 style="margin-bottom: 0.75rem; font-size: 1.2rem;">📋 Assessment History</h3>', unsafe_allow_html=True)
    
    # Display assessment history if available
    if patient_data.get('diabetes_assessments') or patient_data.get('liver_assessments') or patient_data.get('heart_assessments') or patient_data.get('mental_health_assessments'):
        assessment_tabs = st.tabs(["Diabetes", "Liver", "Heart", "Mental Health"])
        
        with assessment_tabs[0]:
            if patient_data.get('diabetes_assessments'):
                st.dataframe(patient_data['diabetes_assessments'], use_container_width=True)
            else:
                st.info("No diabetes assessments completed yet.")
        
        with assessment_tabs[1]:
            if patient_data.get('liver_assessments'):
                st.dataframe(patient_data['liver_assessments'], use_container_width=True)
            else:
                st.info("No liver assessments completed yet.")
        
        with assessment_tabs[2]:
            if patient_data.get('heart_assessments'):
                st.dataframe(patient_data['heart_assessments'], use_container_width=True)
            else:
                st.info("No heart assessments completed yet.")
        
        with assessment_tabs[3]:
            if patient_data.get('mental_health_assessments'):
                st.dataframe(patient_data['mental_health_assessments'], use_container_width=True)
            else:
                st.info("No mental health assessments completed yet.")
    else:
        st.info("📭 No assessment history available. Contact your healthcare worker to schedule assessments.")
    
    st.markdown('<hr style="margin: 0.75rem 0;">', unsafe_allow_html=True)
    
    # Healthcare Worker Information
    st.markdown('<h3 style="margin-bottom: 0.75rem; font-size: 1.2rem;">👨‍⚕️ Healthcare Worker Information</h3>', unsafe_allow_html=True)
    admin_info = patient_data.get('created_by_admin', {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"**Name:** {admin_info.get('name', 'N/A')}")
    with col2:
        st.info(f"**Designation:** {admin_info.get('designation', 'N/A')}")
    with col3:
        st.info(f"**Contact:** {admin_info.get('contact_number', 'N/A')}")
    
    st.markdown('<hr style="margin: 0.75rem 0;">', unsafe_allow_html=True)
    
    # Upcoming Appointments (Dummy/Static)
    st.markdown('<h3 style="margin-bottom: 0.75rem; font-size: 1.2rem;">📅 Upcoming Appointments</h3>', unsafe_allow_html=True)
    
    # Generate dummy appointments based on risk levels
    appointments = []
    if risk_data:
        for risk_key, disease_name in [
            ("diabetes_risk_level", "Diabetes"),
            ("liver_risk_level", "Liver Disease"),
            ("heart_risk_level", "Heart Disease"),
            ("mental_health_risk_level", "Mental Health")
        ]:
            level = risk_data.get(risk_key)
            if level in ["Medium", "High"]:
                appointment_date = datetime.now() + timedelta(days=7)
                appointment_time = "10:00 AM"
                
                if level == "High":
                    consultation_type = "In-Person Consultation"
                    location = "Specialist Clinic"
                else:
                    consultation_type = "Teleconsultation"
                    location = "Virtual"
                
                appointments.append({
                    "Disease": disease_name,
                    "Date": appointment_date.strftime("%Y-%m-%d"),
                    "Time": appointment_time,
                    "Type": consultation_type,
                    "Location": location
                })
    
    if appointments:
        for appointment in appointments:
            st.markdown(f"""
            <div style="background: var(--color-bg-white); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--color-primary); margin: 0.75rem 0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <h4 style="margin: 0; color: var(--color-primary); font-size: 1.1rem;">📅 {appointment['Disease']} Consultation</h4>
                <p style="margin: 0.75rem 0; color: var(--color-text-secondary); line-height: 1.5;">
                    <strong>Date:</strong> {appointment['Date']} at {appointment['Time']}<br>
                    <strong>Type:</strong> {appointment['Type']}<br>
                    <strong>Location:</strong> {appointment['Location']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No upcoming appointments scheduled.")
    
    st.markdown('<hr style="margin: 0.75rem 0;">', unsafe_allow_html=True)
    
    # Enhanced Lifestyle Recommendations - Friendly & Encouraging
    st.markdown('<h3 style="margin-bottom: 0.75rem; font-size: 1.2rem;">💡 Your Personalized Health Tips</h3>', unsafe_allow_html=True)
    
    if recommendations and any(recommendations.values()):
        st.markdown("""
        <div style="background: var(--color-primary-light); padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">
            <p style="margin: 0; color: var(--color-text-primary); font-size: 0.95rem; line-height: 1.5;">
                🌟 <strong>Great news!</strong> Based on your health assessment, here are some personalized tips to help you stay healthy and feel your best.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        for category, recs in recommendations.items():
            if recs:
                # Friendly category headers
                category_icons = {
                    'diet': '🥗',
                    'exercise': '🏃‍♂️',
                    'lifestyle': '🌱',
                    'general': '💚',
                    'medication': '💊',
                    'monitoring': '📊'
                }
                
                icon = category_icons.get(category.lower(), '💡')
                st.markdown(f"""
                <div style="background: var(--color-bg-white); padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border: 1px solid var(--color-border);">
                    <h4 style="margin: 0; color: var(--color-primary); font-size: 1.1rem;">{icon} {category.title()} Tips</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for rec in recs:
                    disease_type = rec.get('disease_type', 'General')
                    text = rec.get('recommendation_text', '')
                    risk_level = rec.get('risk_level', 'Medium')
                    
                    # Friendly, encouraging styling based on priority
                    if risk_level == 'High':
                        priority_style = """
                        <div style="background: linear-gradient(135deg, #fff5f5, #fef2f2); padding: 1.25rem; border-radius: 12px; margin: 0.75rem 0; border-left: 4px solid #f87171; box-shadow: 0 2px 8px rgba(248, 113, 113, 0.1);">
                            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                                <div style="background: #f87171; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0;">⭐</div>
                                <div>
                                    <h5 style="margin: 0 0 0.5rem 0; color: #dc2626; font-size: 1rem; font-weight: 600;">Priority Action</h5>
                                    <p style="margin: 0; color: var(--color-text-primary); line-height: 1.5; font-size: 0.95rem;"><strong>{disease_type}:</strong> {text}</p>
                                </div>
                            </div>
                        </div>
                        """
                    elif risk_level == 'Medium':
                        priority_style = """
                        <div style="background: linear-gradient(135deg, #fffbeb, #fef3c7); padding: 1.25rem; border-radius: 12px; margin: 0.75rem 0; border-left: 4px solid #fbbf24; box-shadow: 0 2px 8px rgba(251, 191, 36, 0.1);">
                            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                                <div style="background: #fbbf24; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0;">💪</div>
                                <div>
                                    <h5 style="margin: 0 0 0.5rem 0; color: #d97706; font-size: 1rem; font-weight: 600;">Helpful Tip</h5>
                                    <p style="margin: 0; color: var(--color-text-primary); line-height: 1.5; font-size: 0.95rem;"><strong>{disease_type}:</strong> {text}</p>
                                </div>
                            </div>
                        </div>
                        """
                    else:
                        priority_style = """
                        <div style="background: linear-gradient(135deg, #f0fdf4, #dcfce7); padding: 1.25rem; border-radius: 12px; margin: 0.75rem 0; border-left: 4px solid #4ade80; box-shadow: 0 2px 8px rgba(74, 222, 128, 0.1);">
                            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                                <div style="background: #4ade80; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0;">🌱</div>
                                <div>
                                    <h5 style="margin: 0 0 0.5rem 0; color: #16a34a; font-size: 1rem; font-weight: 600;">Wellness Boost</h5>
                                    <p style="margin: 0; color: var(--color-text-primary); line-height: 1.5; font-size: 0.95rem;"><strong>{disease_type}:</strong> {text}</p>
                                </div>
                            </div>
                        </div>
                        """
                    
                    st.markdown(priority_style.format(disease_type=disease_type, text=text), unsafe_allow_html=True)
        
        # Encouraging footer message
        st.markdown("""
        <div style="background: linear-gradient(135deg, var(--color-primary-light), #e0f2fe); padding: 1.5rem; border-radius: 12px; margin-top: 1.5rem; text-align: center; border: 1px solid var(--color-border);">
            <h4 style="margin: 0 0 0.75rem 0; color: var(--color-primary); font-size: 1.1rem;">🎯 You're on the right track!</h4>
            <p style="margin: 0; color: var(--color-text-secondary); font-size: 0.95rem; line-height: 1.5;">
                Small, consistent changes can make a big difference in your health. Remember, every step forward is progress! 💚
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: var(--color-bg-light-gray); padding: 2rem; border-radius: 12px; text-align: center; border: 1px solid var(--color-border);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🌟</div>
            <h4 style="margin: 0 0 0.75rem 0; color: var(--color-primary);">Keep up the great work!</h4>
            <p style="margin: 0; color: var(--color-text-secondary); line-height: 1.5;">
                Your health assessment looks great! Continue maintaining your healthy lifestyle, and we'll provide personalized tips as needed.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr style="margin: 0.75rem 0;">', unsafe_allow_html=True)
    
    # Medication Schedule (Dummy/Static)
    st.markdown('<h3 style="margin-bottom: 0.75rem; font-size: 1.2rem;">💊 Medication Schedule</h3>', unsafe_allow_html=True)
    
    medication_data = {
        "Medication": ["Metformin", "Atorvastatin", "Multivitamin"],
        "Morning": ["✓", "", "✓"],
        "Afternoon": ["", "", ""],
        "Evening": ["✓", "✓", ""]
    }
    
    df_meds = pd.DataFrame(medication_data)
    st.dataframe(df_meds, use_container_width=True)
    
    st.caption("✓ = Take medication | BF = Before Food | AF = After Food")

# --- View: Individual Disease Tabs ---
def render_disease_tab(disease_name, risk_key, score_key):
    st.markdown(f'<h1 style="margin-bottom: 0.5rem; font-size: 1.8rem;">{disease_name} Assessment</h1>', unsafe_allow_html=True)
    
    if not risk_data:
        st.warning("No risk assessment data available.")
        return
    
    risk_level = risk_data.get(risk_key, 'N/A')
    risk_score = risk_data.get(score_key, 0)
    
    # Risk Score Display
    st.markdown('<h3 style="margin-bottom: 0.75rem; font-size: 1.2rem;">📊 Risk Score</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Risk Score", f"{risk_score:.3f}", help="Score between 0 and 1")
    with col2:
        color = utils.risk_color(risk_level)
        st.markdown(f"""
        <div style="background: {color}20; padding: 15px; border-radius: 8px; border-left: 4px solid {color}; text-align: center;">
            <h3 style="margin: 0; color: {color};">Risk Level: {risk_level.upper()}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr style="margin: 0.75rem 0;">', unsafe_allow_html=True)
    
    # Next Recommended Action Steps
    st.markdown('<h3 style="margin-bottom: 0.75rem; font-size: 1.2rem;">🎯 Next Recommended Action Steps</h3>', unsafe_allow_html=True)
    
    if risk_level == "High":
        st.error("🚨 **URGENT CARE REQUIRED**")
        st.markdown("""
        **Immediate Actions:**
        - Schedule in-person consultation with specialist
        - Follow strict dietary restrictions
        - Adhere to medication schedule
        - Monitor symptoms closely
        - Seek emergency care if symptoms worsen
        """)
    elif risk_level == "Medium":
        st.warning("⚠️ **MONITORING RECOMMENDED**")
        st.markdown("""
        **Recommended Actions:**
        - Schedule teleconsultation with doctor
        - Implement lifestyle modifications
        - Regular health monitoring
        - Follow dietary guidelines
        - Increase physical activity
        """)
    else:
        st.success("✅ **LOW RISK - PREVENTIVE CARE**")
        st.markdown("""
        **Preventive Measures:**
        - Maintain healthy lifestyle
        - Regular health checkups
        - Balanced diet
        - Regular exercise
        - Stress management
        """)
    
    st.markdown('<hr style="margin: 0.75rem 0;">', unsafe_allow_html=True)
    
    # Disease-specific recommendations - Friendly & Encouraging
    st.markdown('<h3 style="margin-bottom: 0.75rem; font-size: 1.2rem;">💡 Your Personalized Tips</h3>', unsafe_allow_html=True)
    
    disease_recs = []
    if recommendations:
        for category, recs in recommendations.items():
            for rec in recs:
                if rec.get('disease_type', '').lower() == disease_name.lower():
                    disease_recs.append(rec)
    
    if disease_recs:
        st.markdown("""
        <div style="background: var(--color-primary-light); padding: 1rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">
            <p style="margin: 0; color: var(--color-text-primary); font-size: 0.95rem; line-height: 1.5;">
                🌟 <strong>Personalized guidance</strong> tailored specifically for your {disease_name} assessment results.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        for rec in disease_recs:
            category = rec.get('category', 'General')
            text = rec.get('recommendation_text', '')
            risk_level = rec.get('risk_level', 'Medium')
            
            # Friendly, encouraging styling based on priority
            if risk_level == 'High':
                priority_style = """
                <div style="background: linear-gradient(135deg, #fff5f5, #fef2f2); padding: 1.25rem; border-radius: 12px; margin: 0.75rem 0; border-left: 4px solid #f87171; box-shadow: 0 2px 8px rgba(248, 113, 113, 0.1);">
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <div style="background: #f87171; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0;">⭐</div>
                        <div>
                            <h5 style="margin: 0 0 0.5rem 0; color: #dc2626; font-size: 1rem; font-weight: 600;">Priority Action</h5>
                            <p style="margin: 0; color: var(--color-text-primary); line-height: 1.5; font-size: 0.95rem;"><strong>{category}:</strong> {text}</p>
                        </div>
                    </div>
                </div>
                """
            elif risk_level == 'Medium':
                priority_style = """
                <div style="background: linear-gradient(135deg, #fffbeb, #fef3c7); padding: 1.25rem; border-radius: 12px; margin: 0.75rem 0; border-left: 4px solid #fbbf24; box-shadow: 0 2px 8px rgba(251, 191, 36, 0.1);">
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <div style="background: #fbbf24; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0;">💪</div>
                        <div>
                            <h5 style="margin: 0 0 0.5rem 0; color: #d97706; font-size: 1rem; font-weight: 600;">Helpful Tip</h5>
                            <p style="margin: 0; color: var(--color-text-primary); line-height: 1.5; font-size: 0.95rem;"><strong>{category}:</strong> {text}</p>
                        </div>
                    </div>
                </div>
                """
            else:
                priority_style = """
                <div style="background: linear-gradient(135deg, #f0fdf4, #dcfce7); padding: 1.25rem; border-radius: 12px; margin: 0.75rem 0; border-left: 4px solid #4ade80; box-shadow: 0 2px 8px rgba(74, 222, 128, 0.1);">
                    <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                        <div style="background: #4ade80; color: white; border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0;">🌱</div>
                        <div>
                            <h5 style="margin: 0 0 0.5rem 0; color: #16a34a; font-size: 1rem; font-weight: 600;">Wellness Boost</h5>
                            <p style="margin: 0; color: var(--color-text-primary); line-height: 1.5; font-size: 0.95rem;"><strong>{category}:</strong> {text}</p>
                        </div>
                    </div>
                </div>
                """
            
            st.markdown(priority_style.format(category=category, text=text), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: var(--color-bg-light-gray); padding: 2rem; border-radius: 12px; text-align: center; border: 1px solid var(--color-border);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🌟</div>
            <h4 style="margin: 0 0 0.75rem 0; color: var(--color-primary);">Looking great!</h4>
            <p style="margin: 0; color: var(--color-text-secondary); line-height: 1.5;">
                Your {disease_name} assessment results are encouraging. Keep maintaining your healthy habits!
            </p>
        </div>
        """, unsafe_allow_html=True)

with tabs[1]:
    render_disease_tab("Diabetes", "diabetes_risk_level", "diabetes_risk_score")

with tabs[2]:
    render_disease_tab("Liver Disease", "liver_risk_level", "liver_risk_score")

with tabs[3]:
    render_disease_tab("Heart Disease", "heart_risk_level", "heart_risk_score")

with tabs[4]:
    render_disease_tab("Mental Health", "mental_health_risk_level", "mental_health_risk_score")

# --- PDF Download Modal ---
if st.session_state.get("show_pdf_download", False):
    st.markdown("---")
    st.subheader("📄 Download Health Report")
    
    st.markdown("Select the sections you want to include in your health report:")
    
    sections = ["Overview", "Diabetes", "Liver", "Heart", "Mental Health"]
    selected_sections = []
    
    for section in sections:
        if st.checkbox(section, key=f"pdf_{section}"):
            selected_sections.append(section)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download PDF", use_container_width=True, type="primary"):
            if selected_sections:
                with st.spinner("Generating PDF..."):
                    pdf_content = api_client.get_pdf_report(st.session_state.user_id, selected_sections)
                    if pdf_content:
                        st.download_button(
                            label="💾 Download PDF Report",
                            data=pdf_content,
                            file_name=f"Health_Report_{patient_data.get('abha_id', 'patient')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("PDF generated successfully!")
                    else:
                        st.error("Failed to generate PDF.")
            else:
                st.warning("Please select at least one section.")
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_pdf_download = False
            st.rerun()

# --- Share Details Modal ---
if st.session_state.get("show_share_options", False):
    st.markdown("---")
    st.subheader("📤 Share Health Details")
    
    st.markdown("Select the sections you want to share:")
    
    sections = ["Overview", "Diabetes", "Liver", "Heart", "Mental Health"]
    selected_sections = []
    
    for section in sections:
        if st.checkbox(section, key=f"share_{section}"):
            selected_sections.append(section)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📤 Generate Share Link", use_container_width=True, type="primary"):
            if selected_sections:
                with st.spinner("Generating share link..."):
                    share = api_client.share_patient_details(st.session_state.user_id, selected_sections)
                if share and share.get("share_url"):
                    st.success("Share link generated successfully!")
                    st.code(share.get("share_url"))
                else:
                    st.error("Failed to generate share link.")
            else:
                st.warning("Please select at least one section.")
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_share_options = False
            st.rerun()
