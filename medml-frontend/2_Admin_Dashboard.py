import streamlit as st
import api_client
import utils
import pandas as pd

st.set_page_config(page_title="Admin Dashboard", layout="wide")
utils.check_login(role="admin")

# --- State Management ---
if "admin_view" not in st.session_state:
    st.session_state.admin_view = "main" # main, add_user, view_patients, patient_detail, edit_patient
if "add_user_step" not in st.session_state:
    st.session_state.add_user_step = 1 # 1, 2, 'diabetes', 'liver', 'heart', 'mental_health'
if "new_patient_id" not in st.session_state:
    st.session_state.new_patient_id = None
if "new_patient_name" not in st.session_state: # Added
    st.session_state.new_patient_name = None
if "assessment_status" not in st.session_state:
    st.session_state.assessment_status = {"diabetes": False, "liver": False, "heart": False, "mental_health": False}
if "view_patient_id" not in st.session_state:
    st.session_state.view_patient_id = None
if "edit_patient_data" not in st.session_state: # Added
    st.session_state.edit_patient_data = None


# --- Navigation Callbacks ---
def set_view(view_name):
    st.session_state.admin_view = view_name
    
def go_to_patient_detail(patient_id):
    st.session_state.view_patient_id = patient_id
    st.session_state.admin_view = "patient_detail"

def go_to_edit_patient(patient_id): # Added
    patient_data = api_client.get_patient_details(patient_id)
    if patient_data:
        st.session_state.edit_patient_data = patient_data
        st.session_state.admin_view = "edit_patient"
    else:
        st.error("Could not load patient data for editing.")

def reset_add_user_flow():
    st.session_state.add_user_step = 1
    st.session_state.new_patient_id = None
    st.session_state.new_patient_name = None # Added
    st.session_state.assessment_status = {"diabetes": False, "liver": False, "heart": False, "mental_health": False}
    set_view("main")

# --- View: Main Dashboard ---
if st.session_state.admin_view == "main":
    st.title(f"Welcome, {st.session_state.user_name}! 👋")
    
    st.subheader("Primary Actions")
    col1, col2 = st.columns(2)
    col1.button("➕ Add New User", on_click=set_view, args=("add_user",), use_container_width=True)
    col2.button("👥 View Registered Patients", on_click=set_view, args=("view_patients",), use_container_width=True)
    
    st.divider()
    
    st.subheader("Analytics Dashboard")
    stats = api_client.get_dashboard_stats()
    
    if stats:
        utils.styled_metric("Today's Registrations", stats.get("today_registrations", 0))
        
        risk_cols = st.columns(4)
        with risk_cols[0]:
            utils.styled_metric("At Risk: Diabetes", stats.get("diabetes_risk_count", 0))
        with risk_cols[1]:
            utils.styled_metric("At Risk: Liver", stats.get("liver_risk_count", 0))
        with risk_cols[2]:
            utils.styled_metric("At Risk: Heart", stats.get("heart_risk_count", 0))
        with risk_cols[3]:
            utils.styled_metric("At Risk: Mental Health", stats.get("mental_health_risk_count", 0))
    else:
        st.warning("Could not load analytics.")

# --- View: Add New User ---
elif st.session_state.admin_view == "add_user":
    st.button("Back to Dashboard", on_click=set_view, args=("main",))
    st.title("➕ Add New Patient")
    
    # --- Step 1: Basic Info ---
    if st.session_state.add_user_step == 1:
        st.subheader("Step 1: Basic Information")
        with st.form("basic_info_form"):
            name = st.text_input("Name*")
            abha_id = st.text_input("ABHA ID (14 digits)*", max_chars=14)
            age = st.number_input("Age*", min_value=0, max_value=120, step=1)
            gender = st.selectbox("Gender*", ["Male", "Female"])
            height = st.number_input("Height (in cm)*", min_value=50.0, max_value=300.0, step=0.5)
            weight = st.number_input("Weight (in kg)*", min_value=10.0, max_value=300.0, step=0.1)
            state_name = st.selectbox("State*", utils.INDIAN_STATES)
            
            # Dummy password for now, as per backend model
            password = f"{abha_id}@default" 
            
            submitted = st.form_submit_button("Save and Proceed")
            
            if submitted:
                if len(abha_id) != 14 or not abha_id.isdigit():
                    st.error("ABHA ID must be 14 digits.")
                elif not all([name, age, gender, height, weight, state_name]):
                    st.error("Please fill all required fields.")
                else:
                    data = {
                        "name": name, "abha_id": abha_id, "password": password,
                        "age": age, "gender": gender, "height": height, 
                        "weight": weight, "state_name": state_name
                    }
                    new_patient = api_client.add_patient(data)
                    if new_patient:
                        st.session_state.new_patient_id = new_patient.get("patient_id")
                        st.session_state.new_patient_name = new_patient.get("name") # Added
                        st.session_state.add_user_step = 2
                        st.rerun()

    # --- Step 2: Assessment Hub ---
    elif st.session_state.add_user_step == 2:
        st.subheader("Step 2: Health Assessment Dashboard")
        patient_id = st.session_state.new_patient_id
        patient_name = st.session_state.new_patient_name
        # Updated to show patient name as per SRD
        st.info(f"Adding assessments for: **{patient_name}** (Patient ID: {patient_id})") 
        
        status = st.session_state.assessment_status
        def get_status(key):
            # SRD specifies Green tick ✓ and Yellow dot ●
            return "✓ Completed" if status[key] else "● Pending" 
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.button(f"Diabetes Assessment\n{get_status('diabetes')}", on_click=lambda: st.session_state.update(add_user_step='diabetes'), use_container_width=True)
        with col2:
            st.button(f"Liver Assessment\n{get_status('liver')}", on_click=lambda: st.session_state.update(add_user_step='liver'), use_container_width=True)
        with col3:
            st.button(f"Heart Assessment\n{get_status('heart')}", on_click=lambda: st.session_state.update(add_user_step='heart'), use_container_width=True)
        with col4:
            st.button(f"Mental Health Assessment\n{get_status('mental_health')}", on_click=lambda: st.session_state.update(add_user_step='mental_health'), use_container_width=True)
        
        st.divider()
        
        all_done = all(status.values())
        if st.button("Finish Survey & Trigger Prediction", disabled=not all_done, type="primary"):
            with st.spinner("Running risk analysis..."):
                result = api_client.trigger_prediction(patient_id)
            if result:
                st.success(f"Successfully added patient and triggered risk assessment! {result.get('message')}")
                reset_add_user_flow()
                st.balloons()
            else:
                st.error("Failed to trigger prediction.")

    # --- Step 3: Individual Forms ---
    def render_assessment_form(name, fields, api_key):
        st.subheader(f"Step 3: {name} Assessment")
        st.button("Back to Assessment Hub", on_click=lambda: st.session_state.update(add_user_step=2))
        
        with st.form(f"{api_key}_form"):
            form_data = {}
            for field, field_type, kwargs in fields:
                if field_type == "number":
                    form_data[field] = st.number_input(field, **kwargs)
                elif field_type == "bool":
                    form_data[field] = 1 if st.checkbox(field, **kwargs) else 0
                elif field_type == "select":
                    form_data[field] = st.selectbox(field, **kwargs)
            
            submitted = st.form_submit_button("Save Assessment")
            
            if submitted:
                result = api_client.add_assessment(st.session_state.new_patient_id, api_key, form_data)
                if result:
                    st.session_state.assessment_status[api_key] = True
                    st.session_state.add_user_step = 2
                    st.rerun()

    if st.session_state.add_user_step == 'diabetes':
        fields = [
            ("pregnancy", "bool", {}),
            ("glucose", "number", {"min_value": 0.0, "step": 1.0, "format": "%.1f", "label": "Glucose (mg/dL)"}),
            ("blood_pressure", "number", {"min_value": 0.0, "step": 1.0, "format": "%.1f", "label": "Blood Pressure (mm Hg)"}),
            ("skin_thickness", "number", {"min_value": 0.0, "step": 0.1, "format": "%.1f", "label": "Skin Thickness (mm)"}),
            ("insulin", "number", {"min_value": 0.0, "step": 1.0, "format": "%.1f", "label": "Insulin (μU/mL)"}),
            ("diabetes_history", "bool", {})
        ]
        render_assessment_form("Diabetes", fields, "diabetes")

    if st.session_state.add_user_step == 'liver':
        fields = [
            ("total_bilirubin", "number", {"min_value": 0.0, "step": 0.1, "format": "%.1f", "label": "Total Bilirubin (mg/dL)"}),
            ("direct_bilirubin", "number", {"min_value": 0.0, "step": 0.1, "format": "%.1f", "label": "Direct Bilirubin (mg/dL)"}),
            ("alkaline_phosphatase", "number", {"min_value": 0.0, "step": 1.0, "format": "%.1f", "label": "Alkaline Phosphatase (IU/L)"}),
            ("sgpt_alamine_aminotransferase", "number", {"min_value": 0.0, "step": 1.0, "format": "%.1f", "label": "SGPT (U/L)"}),
            ("sgot_aspartate_aminotransferase", "number", {"min_value": 0.0, "step": 1.0, "format": "%.1f", "label": "SGOT (U/L)"}),
            ("total_protein", "number", {"min_value": 0.0, "step": 0.1, "format": "%.1f", "label": "Total Protein (g/dL)"}),
            ("albumin", "number", {"min_value": 0.0, "step": 0.1, "format": "%.1f", "label": "Albumin (g/dL)"})
        ]
        render_assessment_form("Liver", fields, "liver")

    if st.session_state.add_user_step == 'heart':
        fields = [
            ("diabetes", "bool", {}), ("hypertension", "bool", {}), ("obesity", "bool", {}),
            ("smoking", "bool", {}), ("alcohol_consumption", "bool", {}), ("physical_activity", "bool", {}),
            ("family_history", "bool", {}), ("heart_attack_history", "bool", {}),
            ("diet_score", "number", {"min_value": 1, "max_value": 10, "step": 1, "label": "Diet Score (1-10)"}),
            ("cholesterol_level", "number", {"min_value": 0.0, "step": 1.0, "format": "%.1f", "label": "Cholesterol (mg/dL)"}),
            ("triglyceride_level", "number", {"min_value": 0.0, "step": 1.0, "format": "%.1f", "label": "Triglycerides (mg/dL)"}),
            ("ldl_level", "number", {"min_value": 0.0, "step": 1.0, "format": "%.1f", "label": "LDL (mg/dL)"}),
            ("hdl_level", "number", {"min_value": 0.0, "step": 1.0, "format": "%.1f", "label": "HDL (mg/dL)"}),
            ("systolic_bp", "number", {"min_value": 0, "step": 1, "label": "Systolic BP (mm Hg)"}),
            ("diastolic_bp", "number", {"min_value": 0, "step": 1, "label": "Diastolic BP (mm Hg)"}),
            ("air_pollution_exposure", "number", {"min_value": 0.0, "step": 0.1, "format": "%.1f", "label": "Air Pollution Exposure (Index)"}),
            ("stress_level", "number", {"min_value": 1, "max_value": 10, "step": 1, "label": "Stress Level (1-10)"}),
        ]
        render_assessment_form("Heart", fields, "heart")

    if st.session_state.add_user_step == 'mental_health':
        fields = [
            ("phq_score", "number", {"min_value": 0, "max_value": 27, "step": 1, "label": "PHQ-9 Score"}),
            ("gad_score", "number", {"min_value": 0, "max_value": 21, "step": 1, "label": "GAD-7 Score"}),
            ("depressiveness", "bool", {"label": "Shows Depressiveness"}),
            ("suicidal", "bool", {"label": "Shows Suicidal Tendencies"}),
            ("anxiousness", "bool", {"label": "Shows Anxiousness"}),
            ("sleepiness", "bool", {"label": "Shows Sleepiness"})
        ]
        render_assessment_form("Mental Health", fields, "mental_health")

# --- View: Edit Patient ---
elif st.session_state.admin_view == "edit_patient":
    st.button("Back to Patient List", on_click=set_view, args=("view_patients",))
    st.title("✏️ Edit Patient Details")

    p_data = st.session_state.edit_patient_data
    if not p_data:
        st.error("No patient data loaded for editing.")
        st.stop()

    st.subheader(f"Editing: {p_data.get('name')} (ID: {p_data.get('patient_id')})")

    try:
        state_index = utils.INDIAN_STATES.index(p_data.get('state_name'))
    except ValueError:
        state_index = 0
        
    try:
        gender_index = ["Male", "Female"].index(p_data.get('gender'))
    except ValueError:
        gender_index = 0

    with st.form("edit_patient_form"):
        name = st.text_input("Name*", value=p_data.get('name'))
        abha_id = st.text_input("ABHA ID (14 digits)*", value=p_data.get('abha_id'), max_chars=14)
        age = st.number_input("Age*", value=p_data.get('age'), min_value=0, max_value=120, step=1)
        gender = st.selectbox("Gender*", ["Male", "Female"], index=gender_index)
        height = st.number_input("Height (in cm)*", value=p_data.get('height'), min_value=50.0, max_value=300.0, step=0.5)
        weight = st.number_input("Weight (in kg)*", value=p_data.get('weight'), min_value=10.0, max_value=300.0, step=0.1)
        state_name = st.selectbox("State*", utils.INDIAN_STATES, index=state_index)
        
        submitted = st.form_submit_button("Save Changes")
        
        if submitted:
            if len(abha_id) != 14 or not abha_id.isdigit():
                st.error("ABHA ID must be 14 digits.")
            elif not all([name, age, gender, height, weight, state_name]):
                st.error("Please fill all required fields.")
            else:
                data = {
                    "name": name, "abha_id": abha_id,
                    "age": age, "gender": gender, "height": height, 
                    "weight": weight, "state_name": state_name
                }
                # Note: Password is not updated here, only basic info
                updated_patient = api_client.update_patient(p_data.get('patient_id'), data)
                if updated_patient:
                    st.success("Patient details updated successfully!")
                    st.session_state.edit_patient_data = None
                    set_view("view_patients")
                    st.rerun()


# --- View: View Registered Patients ---
elif st.session_state.admin_view == "view_patients":
    st.button("Back to Dashboard", on_click=set_view, args=("main",))
    st.title("👥 Registered Patients")
    
    tabs = st.tabs(["All Users", "Diabetes", "Liver", "Heart", "Mental Health"])
    categories = ["All Users", "Diabetes", "Liver", "Heart", "Mental Health"]
    
    for i, tab in enumerate(tabs):
        with tab:
            category = categories[i]
            sort_option = st.radio("Sort by", ["Recently added", "High risk", "Medium risk"], key=f"sort_{category}", horizontal=True)
            
            patients = api_client.get_patients(category=category, sort=sort_option)
            
            if not patients:
                st.write("No patients found for this category.")
                continue

            for p in patients:
                with st.container(border=True):
                    st.subheader(p.get('name'))
                    st.caption(f"ABHA ID: {p.get('abha_id')}")
                    
                    # Display relevant risk
                    if category != "All Users":
                        risk_key = f"{category.lower()}_risk_level"
                        level = p.get('latest_prediction', {}).get(risk_key, 'N/A')
                        color = utils.risk_color(level)
                        st.markdown(f"Risk: **<span style='color:{color};'>{level}</span>**", unsafe_allow_html=True)

                    col1, col2 = st.columns([1, 1])
                    col1.button("View Details", key=f"view_{p['patient_id']}", on_click=go_to_patient_detail, args=(p['patient_id'],), use_container_width=True)
                    # Enabled "Edit" button as per SRD
                    col2.button("Edit", key=f"edit_{p['patient_id']}", on_click=go_to_edit_patient, args=(p['patient_id'],), use_container_width=True)

# --- View: Patient Detail ---
elif st.session_state.admin_view == "patient_detail":
    st.button("Back to Patient List", on_click=set_view, args=("view_patients",))
    patient_id = st.session_state.view_patient_id
    
    if not patient_id:
        st.error("No patient selected.")
        st.stop()
        
    # Use @st.cache_data for patient details? Maybe not, admin needs fresh data.
    patient_data = api_client.get_patient_details(patient_id)
    risk_data = api_client.get_latest_prediction(patient_id)
    
    if not patient_data:
        st.error("Failed to load patient data.")
        st.stop()
        
    st.title(f"Patient Profile: {patient_data.get('name')}")
    st.caption(f"ABHA ID: {patient_data.get('abha_id')} | Age: {patient_data.get('age')} | Gender: {patient_data.get('gender')}")
    
    st.divider()
    
    utils.display_risk_table(risk_data)
    
    st.divider()

    # --- Added Patient Info & History as per SRD ---
    st.subheader("Patient Information")
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

    st.subheader("Patient Medical History")
    
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
    # --- End of Added Section ---

    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Consultation Actions")
        if not risk_data:
            st.info("No risk assessment found. Cannot book consultation.")
        else:
            consultations_booked = []
            
            def book_and_track(disease, level):
                with st.spinner(f"Booking for {disease}..."):
                    res = api_client.book_consultation(patient_id, disease, level)
                    if res:
                        # Dummy page confirmation as per SRD
                        st.success(f"Appointment Booked and details forwarded to Doctor! (Disease: {disease})")
                        consultations_booked.append(disease)
                    else:
                        st.error(f"Failed to book for {disease}.")

            for risk_key, disease_name in [
                ("diabetes_risk_level", "Diabetes"),
                ("liver_risk_level", "Liver"),
                ("heart_risk_level", "Heart"),
                ("mental_health_risk_level", "MentalHealth")
            ]:
                level = risk_data.get(risk_key)
                if level in ["High", "Medium"] and disease_name not in consultations_booked:
                    action = "Book In-Person" if level == "High" else "Book Teleconsultation"
                    st.button(f"{action} ({disease_name})", on_click=book_and_track, args=(disease_name, level), use_container_width=True)

    with col2:
        st.subheader("Notes for Doctor")
        # Text field title as per SRD
        notes = st.text_area("Symptoms (if any) or other notes:", height=150, key="consultation_notes")
        if st.button("Save & Send Notes"):
            res = api_client.add_consultation_notes(patient_id, notes)
            if res:
                st.success("Notes saved and forwarded to doctor!")
                # Clear text area after successful submission
                st.session_state.consultation_notes = ""
            else:
                st.error("Failed to save notes.")
        
        st.caption("Existing Notes:")
        notes_history = patient_data.get('consultation_notes', [])
        if notes_history:
            for note in reversed(notes_history): # Show most recent first
                st.text(f"- {note.get('notes')} (at {note.get('created_at')})")
        else:
            st.text("No notes yet.")