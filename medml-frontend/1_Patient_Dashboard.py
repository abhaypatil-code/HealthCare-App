import streamlit as st
import api_client
import utils
import pandas as pd
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Patient Dashboard", layout="wide")
utils.check_login(role="patient")

# --- Data Loading ---
@st.cache_data(ttl=300) # Cache for 5 minutes
def load_patient_data():
    patient_id = st.session_state.user_id
    patient_data = api_client.get_patient_details(patient_id)
    risk_data = api_client.get_latest_prediction(patient_id)
    recommendations = api_client.get_recommendations(patient_id)
    return patient_data, risk_data, recommendations

patient_data, risk_data, recommendations = load_patient_data()

if not patient_data:
    st.error("Could not load patient data. Please try again later.")
    st.stop()

# --- Sidebar Navigation ---
with st.sidebar:
    st.title(f"Hi, {st.session_state.user_name}")
    
    selected_page = option_menu(
        menu_title="My Health",
        options=["Overview", "Diabetes", "Liver", "Heart", "Mental Health", "Profile & Reports"],
        icons=["house", "activity", "droplet", "heart", "person-check", "person-badge"],
        menu_icon="clipboard2-pulse",
        default_index=0,
    )

# --- Page: Overview ---
if selected_page == "Overview":
    st.title("📋 Health Overview")
    
    # --- Health Metrics ---
    st.subheader("Key Health Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        utils.styled_metric("Body Mass Index (BMI)", f"{patient_data.get('bmi', 'N/A'):.2f}")
    with col2:
        utils.styled_metric("Height", f"{patient_data.get('height', 'N/A')} cm")
    with col3:
        utils.styled_metric("Weight", f"{patient_data.get('weight', 'N/A')} kg")
    
    st.divider()
    
    # --- Risk Assessment ---
    utils.display_risk_table(risk_data)
    
    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        # --- Healthcare Worker ---
        st.subheader("Your Healthcare Worker")
        if patient_data.get('created_by_admin'):
            admin = patient_data['created_by_admin']
            st.write(f"**Name:** {admin.get('name', 'N/A')}")
            st.write(f"**Designation:** {admin.get('designation', 'N/A')}")
            st.write(f"**Contact:** {admin.get('contact_number', 'N/A')}")
        else:
            st.write("Information not available.")

        st.divider()

        # --- Upcoming Appointments (Dummy) ---
        st.subheader("Upcoming Appointments")
        st.info("""
        - **Consult a Cardiologist** for Heart Disease on **Nov 15, 2025** at **10:00 AM** - City Hospital
        - **Teleconsultation (Diabetes)** on **Nov 20, 2025** at **2:30 PM** - Virtual
        """)

    with col2:
        # --- Medication Schedule (Dummy) ---
        st.subheader("Medication Schedule")
        med_data = {
            "Medication": ["Metformin", "Atorvastatin"],
            "Morning": ["● (AF)", "○"],
            "Afternoon": ["○", "○"],
            "Evening": ["● (AF)", "● (AF)"]
        }
        med_df = pd.DataFrame(med_data)
        st.dataframe(med_df, use_container_width=True, hide_index=True)
        st.caption("● = Take | ○ = Don't Take | (AF) = After Food / (BF) = Before Food")

    st.divider()

    # --- Lifestyle Recommendations ---
    st.subheader("Personalized Lifestyle Recommendations")
    rec_cols = st.columns(4)
    categories = ["Diet", "Exercise", "Sleep", "Lifestyle"]
    rec_data = recommendations if recommendations else {}
    
    for i, cat in enumerate(categories):
        with rec_cols[i]:
            st.markdown(f"**{cat}**")
            rec_list = rec_data.get(cat.lower(), [])
            if rec_list:
                for rec in rec_list:
                    st.markdown(f"- {rec['recommendation_text']}")
            else:
                st.write("No specific recommendations.")

# --- Page: Individual Disease Tabs ---
def render_disease_tab(title, risk_key, score_key, factors_list, rec_key):
    st.title(f"{title} Risk Details")
    
    if not risk_data:
        st.warning("Risk assessment has not been performed yet.")
        st.stop()
        
    risk_level = risk_data.get(risk_key, "N/A")
    risk_score = risk_data.get(score_key, 0)
    color = utils.risk_color(risk_level)

    st.markdown(f"Your risk level is **<span style='color:{color};'>{risk_level}</span>** with a score of **{risk_score*100:.2f}%**.", unsafe_allow_html=True)
    
    st.subheader("Contributing Factors")
    st.write("Your risk score was calculated based on factors including:")
    factors_md = "\n".join([f"- {factor}" for factor in factors_list])
    st.markdown(factors_md)
    
    st.divider()
    st.subheader("Next Recommended Action Steps")

    if risk_level == "High":
        st.error("**Urgent Care Required:** Please schedule a consultation with a specialist immediately. Your healthcare worker may have already contacted you.")
        st.markdown("- **Strict** dietary restrictions are necessary.")
        st.markdown("- **Mandatory** lifestyle changes are required.")
        st.markdown("- Follow all medication adherence guidelines.")
    elif risk_level == "Medium":
        st.warning("**Monitoring Recommended:** You should book a teleconsultation to discuss these results.")
        st.markdown("- Follow enhanced monitoring recommendations from your doctor.")
        st.markdown("- Adhere to specific dietary restrictions and exercise protocols.")
    elif risk_level == "Low":
        st.success("**Preventive Measures:** You are at low risk. Continue maintaining a healthy lifestyle.")
        st.markdown("- Follow dietary suggestions for health maintenance.")
        st.markdown("- Continue regular physical activity.")
    else:
        st.info("No risk level determined.")

    # Show specific recommendations for this disease
    st.divider()
    st.subheader(f"Specific Recommendations for {title}")
    rec_data = recommendations if recommendations else {}
    all_recs = rec_data.get('diet', []) + rec_data.get('exercise', []) + rec_data.get('sleep', []) + rec_data.get('lifestyle', [])
    
    disease_recs = [rec['recommendation_text'] for rec in all_recs if rec['disease_type'] == title]
    if disease_recs:
         for rec in disease_recs:
            st.markdown(f"- {rec}")
    else:
        st.write("No specific recommendations for this category.")


if selected_page == "Diabetes":
    render_disease_tab(
        title="Diabetes",
        risk_key="diabetes_risk_level",
        score_key="diabetes_risk_score",
        factors_list=["Pregnancies", "Glucose", "Blood Pressure", "Skin Thickness", "Insulin", "BMI", "Age", "Diabetes History"],
        rec_key="Diabetes"
    )

if selected_page == "Liver":
    render_disease_tab(
        title="Liver",
        risk_key="liver_risk_level",
        score_key="liver_risk_score",
        factors_list=["Total Bilirubin", "Direct Bilirubin", "Alkaline Phosphatase", "SGPT", "SGOT", "Total Protein", "Albumin", "A/G Ratio", "Age", "Gender"],
        rec_key="Liver"
    )

if selected_page == "Heart":
    render_disease_tab(
        title="Heart",
        risk_key="heart_risk_level",
        score_key="heart_risk_score",
        factors_list=["Age", "Gender", "BMI", "Diabetes", "Hypertension", "Obesity", "Smoking", "Alcohol", "Physical Activity", "Cholesterol", "LDL", "HDL", "Systolic BP", "Diastolic BP", "Family History"],
        rec_key="Heart"
    )

if selected_page == "Mental Health":
    render_disease_tab(
        title="Mental Health",
        risk_key="mental_health_risk_level",
        score_key="mental_health_risk_score",
        factors_list=["PHQ-9 Score (Depression)", "GAD-7 Score (Anxiety)", "Depressiveness", "Suicidal Thoughts", "Anxiousness", "Sleepiness", "Age", "Gender"],
        rec_key="MentalHealth"
    )


# --- Page: Profile & Reports ---
if selected_page == "Profile & Reports":
    st.title("👤 My Profile & Reports")
    
    st.subheader("My Information")
    p = patient_data
    st.text(f"Name: {p.get('name')}")
    st.text(f"ABHA ID: {p.get('abha_id')}")
    st.text(f"Age: {p.get('age')}")
    st.text(f"Gender: {p.get('gender')}")
    st.text(f"Height: {p.get('height')} cm")
    st.text(f"Weight: {p.get('weight')} kg")
    st.text(f"BMI: {p.get('bmi', 0):.2f}")
    st.text(f"State: {p.get('state_name')}")
    
    st.divider()
    
    st.subheader("My Medical History (as entered by worker)")
    
    with st.expander("Diabetes Assessment History"):
        if p.get('diabetes_assessments'):
            st.dataframe(p['diabetes_assessments'])
        else:
            st.write("No diabetes assessment data found.")
            
    with st.expander("Liver Assessment History"):
        if p.get('liver_assessments'):
            st.dataframe(p['liver_assessments'])
        else:
            st.write("No liver assessment data found.")

    with st.expander("Heart Assessment History"):
        if p.get('heart_assessments'):
            st.dataframe(p['heart_assessments'])
        else:
            st.write("No heart assessment data found.")

    with st.expander("Mental Health Assessment History"):
        if p.get('mental_health_assessments'):
            st.dataframe(p['mental_health_assessments'])
        else:
            st.write("No mental health assessment data found.")
            
    st.divider()

    # --- Download & Share ---
    st.subheader("Download or Share My Report")
    st.write("Select the sections you wish to include in your PDF report.")
    
    with st.form("pdf_form"):
        sel_overview = st.checkbox("Overview & Risk Summary", value=True)
        sel_diabetes = st.checkbox("Diabetes Details", value=True)
        sel_liver = st.checkbox("Liver Details", value=True)
        sel_heart = st.checkbox("Heart Details", value=True)
        sel_mental = st.checkbox("Mental Health Details", value=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            pdf_submitted = st.form_submit_button("Download PDF", use_container_width=True)
        with col2:
            share_submitted = st.form_submit_button("Share Details", use_container_width=True)

        if pdf_submitted:
            sections = []
            if sel_overview: sections.append("Overview")
            if sel_diabetes: sections.append("Diabetes")
            if sel_liver: sections.append("Liver")
            if sel_heart: sections.append("Heart")
            if sel_mental: sections.append("MentalHealth")
            
            if not sections:
                st.error("Please select at least one section to download.")
            else:
                pdf_content = api_client.get_pdf_report(st.session_state.user_id, sections)
                if pdf_content:
                    st.download_button(
                        label="Click to Download PDF",
                        data=pdf_content,
                        file_name=f"HealthReport_{st.session_state.user_id}.pdf",
                        mime="application/pdf"
                    )
        
        if share_submitted:
            # This is a dummy action as per the SRD
            st.success("Report sharing link generated! (This is a dummy action)")