import streamlit as st
import time
import api_client
import utils
import pandas as pd
from theme import apply_light_theme, create_navbar, create_metric_card

st.set_page_config(
    page_title="Admin Dashboard", 
    layout="wide",
    page_icon="👨‍⚕️"
)

# Apply enhanced light theme with compact spacing
apply_light_theme()

utils.check_login(role="admin")

# Create top navigation bar
create_navbar(st.session_state.user_name, st.session_state.user_role)

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
    # Enhanced header with Welcome Message
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, var(--color-primary), var(--color-primary-dark)); color: white; padding: 2rem; border-radius: 16px; margin-bottom: 1.5rem; box-shadow: 0 8px 24px rgba(0, 103, 165, 0.3);">
        <h1 style="margin: 0; text-align: center; font-size: 2rem; font-weight: 700;">Healthcare Management Dashboard</h1>
        <p style="margin: 0.75rem 0 0 0; text-align: center; font-size: 1.1em; opacity: 0.9;">Comprehensive patient care and analytics platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Top Action Buttons
    st.subheader("🎯 Primary Actions")
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.button("➕ Add New User", on_click=set_view, args=("add_user",), use_container_width=True, type="primary")
    with col2:
        st.button("👁️ View Registered Patients", on_click=set_view, args=("view_patients",), use_container_width=True, type="secondary")
    with col3:
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            utils.logout()
    
    st.divider()
    
    # Analytics Section
    st.subheader("📊 System Overview")
    stats = api_client.get_dashboard_stats()
    
    if stats:
        # Registration metrics in a more intuitive layout
        st.markdown("### 📈 Patient Registration Trends")
        
        # Registration metrics in columns
        reg_col1, reg_col2, reg_col3, reg_col4 = st.columns(4)
        
        with reg_col1:
            st.markdown(f"""
            <div style="background: var(--color-bg-white); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--color-primary); text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <h4 style="margin: 0; color: var(--color-primary); font-size: 0.9rem; font-weight: 600;">📅 Today</h4>
                <h2 style="margin: 0.75rem 0; color: var(--color-primary); font-size: 2.5rem; font-weight: 700;">{stats.get("today_registrations", 0)}</h2>
                <p style="margin: 0; color: var(--color-text-secondary); font-size: 0.8rem;">New registrations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with reg_col2:
            st.markdown(f"""
            <div style="background: var(--color-bg-white); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--color-primary); text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <h4 style="margin: 0; color: var(--color-primary); font-size: 0.9rem; font-weight: 600;">📆 This Week</h4>
                <h2 style="margin: 0.75rem 0; color: var(--color-primary); font-size: 2.5rem; font-weight: 700;">{stats.get("this_week_registrations", 0)}</h2>
                <p style="margin: 0; color: var(--color-text-secondary); font-size: 0.8rem;">Weekly registrations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with reg_col3:
            st.markdown(f"""
            <div style="background: var(--color-bg-white); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--color-primary); text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <h4 style="margin: 0; color: var(--color-primary); font-size: 0.9rem; font-weight: 600;">📊 This Month</h4>
                <h2 style="margin: 0.75rem 0; color: var(--color-primary); font-size: 2.5rem; font-weight: 700;">{stats.get("this_month_registrations", 0)}</h2>
                <p style="margin: 0; color: var(--color-text-secondary); font-size: 0.8rem;">Monthly registrations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with reg_col4:
            st.markdown(f"""
            <div style="background: var(--color-bg-white); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--color-primary); text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <h4 style="margin: 0; color: var(--color-primary); font-size: 0.9rem; font-weight: 600;">👥 Total Patients</h4>
                <h2 style="margin: 0.75rem 0; color: var(--color-primary); font-size: 2.5rem; font-weight: 700;">{stats.get("total_patients", 0)}</h2>
                <p style="margin: 0; color: var(--color-text-secondary); font-size: 0.8rem;">All-time registrations</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Risk Assessment Cards with better organization
        st.markdown("### 🚨 Health Risk Monitoring")
        st.markdown("Patients requiring immediate attention based on risk assessments")
        
        risk_cols = st.columns(4)
        
        risk_data = [
            ("Diabetes", stats.get("diabetes_risk_count", 0), "var(--color-danger)", "🩺"),
            ("Liver", stats.get("liver_risk_count", 0), "var(--color-warning)", "🫀"),
            ("Heart", stats.get("heart_risk_count", 0), "var(--color-danger)", "❤️"),
            ("Mental Health", stats.get("mental_health_risk_count", 0), "var(--color-primary)", "🧠")
        ]
        
        for i, (disease, count, color, icon) in enumerate(risk_data):
            with risk_cols[i]:
                st.markdown(f"""
                <div style="background: var(--color-bg-white); padding: 1.5rem; border-radius: 12px; border-left: 4px solid {color}; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                    <h4 style="margin: 0; color: {color}; font-size: 0.9rem; font-weight: 600;">{icon} {disease}</h4>
                    <h2 style="margin: 0.75rem 0; color: {color}; font-size: 2.5rem; font-weight: 700;">{count}</h2>
                    <p style="margin: 0; color: var(--color-text-secondary); font-size: 0.8rem;">At-risk patients</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Could not load analytics.")

# --- View: Add New User ---
elif st.session_state.admin_view == "add_user":
    # Navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("🏠 Home", on_click=set_view, args=("main",), use_container_width=True)
    
    st.title("➕ Add New Patient")
    
    # Progress indicator
    steps = ["Basic Info", "Health Assessment", "Complete"]
    current_step = st.session_state.add_user_step
    
    # Convert current_step to integer for progress indicator
    if isinstance(current_step, str):
        # If it's a string (assessment type), we're in step 2
        progress_step = 2
    else:
        # If it's an integer, use it directly
        progress_step = current_step
    
    progress_cols = st.columns(3)
    
    for i, step in enumerate(steps):
        with progress_cols[i]:
            if i + 1 <= progress_step:
                st.markdown(f"✅ **{step}**")
            else:
                st.markdown(f"⏳ {step}")
    
    st.divider()
    
    # --- Step 1: Basic Info ---
    if st.session_state.add_user_step == 1:
        st.subheader("📋 Step 1: Basic Information")
        st.markdown("Enter the patient's basic demographic information:")
        
        with st.form("basic_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("👤 Full Name*", placeholder="Enter patient's full name")
                abha_id = st.text_input("🆔 ABHA ID (14 digits)*", placeholder="Enter 14-digit ABHA ID", max_chars=14)
                age = st.number_input("🎂 Age*", min_value=0, max_value=120, step=1, help="Patient's age in years")
                gender = st.selectbox("⚥ Gender*", ["Male", "Female"])
            
            with col2:
                height = st.number_input("📏 Height (cm)*", min_value=50.0, max_value=300.0, step=0.5, help="Height in centimeters")
                weight = st.number_input("⚖️ Weight (kg)*", min_value=10.0, max_value=300.0, step=0.1, help="Weight in kilograms")
                state_name = st.selectbox("🗺️ State*", utils.INDIAN_STATES, help="Patient's state of residence")
            
            # Calculate and display BMI
            if height > 0 and weight > 0:
                height_m = height / 100.0
                bmi = weight / (height_m ** 2)
                st.info(f"📊 **Calculated BMI**: {bmi:.2f}")
            
            # Generate a compliant password for the patient
            password = f"{abha_id}@Default123" 
            
            st.markdown("---")
            submitted = st.form_submit_button("💾 Save and Proceed to Health Assessment", use_container_width=True, type="primary")
            
            if submitted:
                # Validation checks
                if len(abha_id) != 14 or not abha_id.isdigit():
                    st.error("ABHA ID must be exactly 14 digits.")
                elif not name or len(name.strip()) < 2:
                    st.error("Name must be at least 2 characters long.")
                elif age <= 0 or age > 120:
                    st.error("Age must be between 1 and 120.")
                elif height <= 0 or height > 300:
                    st.error("Height must be between 0.1 and 300 cm.")
                elif weight <= 0 or weight > 300:
                    st.error("Weight must be between 0.1 and 300 kg.")
                elif not state_name:
                    st.error("Please select a state.")
                else:
                    # Prepare data with proper validation
                    data = {
                        "name": name.strip(),
                        "abha_id": abha_id.strip(),
                        "password": password,
                        "age": int(age),
                        "gender": gender,
                        "height": float(height),
                        "weight": float(weight),
                        "state_name": state_name
                    }
                    
                    # Debug: Show the data being sent (remove in production)
                    st.write("🔍 Debug - Sending patient data:", data)
                    
                    with st.spinner("Saving patient..."):
                        new_patient = api_client.add_patient(data)
                    if new_patient:
                        st.session_state.new_patient_id = new_patient.get("patient_id")
                        st.session_state.new_patient_name = new_patient.get("name")
                        st.toast("✅ Patient created", icon="✅")
                        st.session_state.add_user_step = 2
                        st.rerun()
                    else:
                        st.error("Failed to create patient. Please check the error message above.")

    # --- Step 2: Assessment Hub ---
    elif st.session_state.add_user_step == 2:
        st.subheader("📊 Step 2: Health Assessment Dashboard")
        patient_id = st.session_state.new_patient_id
        patient_name = st.session_state.new_patient_name
        
        # Enhanced patient info display
        st.markdown(f"""
        <div style="background: var(--color-bg-white); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--color-primary); margin-bottom: 1.5rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
            <h4 style="margin: 0; color: var(--color-primary); font-size: 1.1rem; font-weight: 600;">👤 Patient Information</h4>
            <p style="margin: 0.75rem 0 0 0; color: var(--color-text-secondary); line-height: 1.5;"><strong>Name:</strong> {patient_name} | <strong>ID:</strong> {patient_id}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("Complete all 4 health assessments to proceed with risk analysis:")
        
        status = st.session_state.assessment_status
        
        # Enhanced assessment cards
        assessment_cols = st.columns(4)
        assessments = [
            ("diabetes", "🩺", "Diabetes Assessment", "#dc3545"),
            ("liver", "🫀", "Liver Assessment", "#fd7e14"),
            ("heart", "❤️", "Heart Assessment", "#e83e8c"),
            ("mental_health", "🧠", "Mental Health Assessment", "#6f42c1")
        ]
        
        for i, (key, icon, title, color) in enumerate(assessments):
            with assessment_cols[i]:
                is_complete = status[key]
                if is_complete:
                    st.markdown(f"""
                    <div style="background: var(--color-bg-white); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--color-success); text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                        <h4 style="margin: 0; color: var(--color-success); font-size: 1rem; font-weight: 600;">✅ {title}</h4>
                        <p style="margin: 0.75rem 0 0 0; color: var(--color-success); font-size: 0.9rem;">Completed</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: var(--color-bg-white); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--color-warning); text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                        <h4 style="margin: 0; color: var(--color-warning); font-size: 1rem; font-weight: 600;">⏳ {title}</h4>
                        <p style="margin: 0.75rem 0 0 0; color: var(--color-warning); font-size: 0.9rem;">Pending</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.button(f"Complete {title}", key=f"btn_{key}", use_container_width=True):
                    st.session_state.add_user_step = key
                    st.rerun()
        
        st.divider()
        
        # Finish Survey button with enhanced styling
        all_done = all(status.values())
        if all_done:
            st.success("🎉 All assessments completed! Ready for risk analysis.")
            st.markdown("""
            <div style="background: #d1ecf1; padding: 15px; border-radius: 8px; border-left: 4px solid #17a2b8;">
                <h4 style="margin: 0; color: #0c5460;">🤖 AI-Powered Risk Analysis Ready</h4>
                <p style="margin: 5px 0 0 0; color: #0c5460;">Click "Finish Survey" to run comprehensive risk analysis on all collected data.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🎯 Finish Survey & Run Risk Analysis", use_container_width=True, type="primary"):
                with st.spinner("🤖 Running AI-powered risk analysis..."):
                    result = api_client.trigger_prediction(patient_id)
                if result:
                    st.success(f"✅ Successfully added patient and triggered risk assessment!")
                    st.balloons()
                    reset_add_user_flow()
                else:
                    st.error("❌ Failed to trigger prediction. This could be due to:")
                    st.markdown("""
                    - Missing ML model files
                    - Backend server issues
                    - Incomplete assessment data
                    - Model processing errors
                    """)
                    st.info("💡 **Solution**: The patient has been saved successfully. You can retry the prediction later from the patient detail view.")
                    # Still reset the flow since patient was created successfully
                    reset_add_user_flow()
        else:
            incomplete = [title for key, _, title, _ in assessments if not status[key]]
            st.warning(f"⚠️ Please complete the following assessments: {', '.join(incomplete)}")

    # --- Step 3: Individual Forms ---
    def render_assessment_form(name, fields, api_key):
        st.subheader(f"Step 3: {name} Assessment")
        st.button("Back to Assessment Hub", on_click=lambda: st.session_state.update(add_user_step=2))
        
        with st.form(f"{api_key}_form"):
            form_data = {}
            for field, field_type, kwargs in fields:
                if field_type == "number":
                    # Use label from kwargs if available, otherwise use field name
                    label = kwargs.pop("label", field)
                    form_data[field] = st.number_input(label, **kwargs)
                elif field_type == "bool":
                    # Use label from kwargs if available, otherwise use field name
                    label = kwargs.pop("label", field)
                    form_data[field] = st.checkbox(label, **kwargs)
                elif field_type == "select":
                    # Use label from kwargs if available, otherwise use field name
                    label = kwargs.pop("label", field)
                    form_data[field] = st.selectbox(label, **kwargs)
            
            submitted = st.form_submit_button("Save Assessment")
            
            if submitted:
                with st.spinner("Saving assessment..."):
                    result = api_client.add_assessment(st.session_state.new_patient_id, api_key, form_data)
                if result:
                    st.toast("✅ Assessment saved", icon="✅")
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
        st.subheader("Step 3: Liver Assessment")
        st.button("Back to Assessment Hub", on_click=lambda: st.session_state.update(add_user_step=2))
        
        with st.form("liver_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                total_bilirubin = st.number_input("Total Bilirubin (mg/dL)", min_value=0.0, step=0.1, format="%.1f")
                direct_bilirubin = st.number_input("Direct Bilirubin (mg/dL)", min_value=0.0, step=0.1, format="%.1f")
                alkaline_phosphatase = st.number_input("Alkaline Phosphatase (IU/L)", min_value=0.0, step=1.0, format="%.1f")
                sgpt_alamine_aminotransferase = st.number_input("SGPT (U/L)", min_value=0.0, step=1.0, format="%.1f")
            
            with col2:
                sgot_aspartate_aminotransferase = st.number_input("SGOT (U/L)", min_value=0.0, step=1.0, format="%.1f")
                total_protein = st.number_input("Total Protein (g/dL)", min_value=0.0, step=0.1, format="%.1f")
                albumin = st.number_input("Albumin (g/dL)", min_value=0.0, step=0.1, format="%.1f")
            
            # Calculate and display A/G ratio
            if total_protein > 0 and albumin > 0 and total_protein > albumin:
                globulin = total_protein - albumin
                if globulin > 0:
                    ag_ratio = albumin / globulin
                    st.info(f"📊 **Calculated A/G Ratio**: {ag_ratio:.2f}")
                else:
                    st.warning("⚠️ Cannot calculate A/G ratio: Globulin value is zero or negative")
            elif total_protein > 0 and albumin > 0:
                st.warning("⚠️ Cannot calculate A/G ratio: Total protein must be greater than albumin")
            
            submitted = st.form_submit_button("Save Assessment")
            
            if submitted:
                form_data = {
                    "total_bilirubin": total_bilirubin,
                    "direct_bilirubin": direct_bilirubin,
                    "alkaline_phosphatase": alkaline_phosphatase,
                    "sgpt_alamine_aminotransferase": sgpt_alamine_aminotransferase,
                    "sgot_aspartate_aminotransferase": sgot_aspartate_aminotransferase,
                    "total_protein": total_protein,
                    "albumin": albumin
                }
                with st.spinner("Saving assessment..."):
                    result = api_client.add_assessment(st.session_state.new_patient_id, "liver", form_data)
                if result:
                    st.toast("✅ Assessment saved", icon="✅")
                    st.session_state.assessment_status["liver"] = True
                    st.session_state.add_user_step = 2
                    st.rerun()

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
    # Navigation Bar
    col1, col2 = st.columns([1, 4])
    with col1:
        st.button("🏠 Home", on_click=set_view, args=("main",), use_container_width=True)
    
    st.title("👥 Patient Management")
    
    # Initialize session state for filters
    if "patient_category" not in st.session_state:
        st.session_state.patient_category = "All Users"
    if "patient_sort" not in st.session_state:
        st.session_state.patient_sort = "Recently Added"
    
    # Unified Filter and Sort Panel
    st.markdown("### 🔍 Filter & Sort Options")
    
    # Create a clean filter panel
    filter_col1, filter_col2 = st.columns([2, 2])
    
    with filter_col1:
        category = st.selectbox(
            "Disease Category:",
            ["All Users", "Diabetes", "Liver", "Heart", "Mental Health"],
            key="category_selector",
            index=["All Users", "Diabetes", "Liver", "Heart", "Mental Health"].index(st.session_state.patient_category)
        )
        st.session_state.patient_category = category
    
    with filter_col2:
        sort_option = st.selectbox(
            "Sort by:",
            ["Recently Added", "High Risk", "Medium Risk", "Low Risk"],
            key="sort_selector",
            index=["Recently Added", "High Risk", "Medium Risk", "Low Risk"].index(st.session_state.patient_sort)
        )
        st.session_state.patient_sort = sort_option
    
    # Refresh button removed per requirement
    
    # Removed logout from filter bar per requirement
    
    st.divider()
    
    # Get patients data based on current filters
    patients = api_client.get_patients(category=st.session_state.patient_category, sort=st.session_state.patient_sort)
    
    # Display results
    if not patients:
        st.info(f"📭 No patients found for {st.session_state.patient_category} category.")
    else:
        # Results header
        st.markdown(f"### 📋 {st.session_state.patient_category} Patients ({len(patients)} found)")
        
        # Display patients as single, unified cards with actions
        for p in patients:
            with st.container():
                # Card wrapper open
                st.markdown(
                    """
                    <div style="background: var(--color-bg-white); padding: 1.25rem; border-radius: 12px; border-left: 4px solid var(--color-primary); margin: 0.75rem 0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                    """,
                    unsafe_allow_html=True,
                )

                # Header row: Name + actions
                header_left, header_mid, header_right = st.columns([6, 2, 2])
                with header_left:
                    st.markdown(
                        f"<h4 style=\"margin: 0 0 0.25rem 0; color: var(--color-primary); font-size: 1.1rem; font-weight: 600;\">👤 {str(p.get('name') or '').strip().title()}</h4>",
                        unsafe_allow_html=True,
                    )
                    gender_display = str(p.get('gender', 'N/A') or '').strip().rstrip('.')
                    st.markdown(
                        f"<span style=\"color: var(--color-text-secondary);\"><strong>ABHA ID:</strong> {p.get('abha_id')} &nbsp;|&nbsp; <strong>Age:</strong> {p.get('age', 'N/A')} &nbsp;|&nbsp; <strong>Gender:</strong> {gender_display}</span>",
                        unsafe_allow_html=True,
                    )
                with header_mid:
                    st.button(
                        "✏️ Edit Details",
                        key=f"edit_{p['patient_id']}",
                        on_click=go_to_edit_patient,
                        args=(p['patient_id'],),
                        use_container_width=True,
                    )
                with header_right:
                    st.button(
                        "👁️ View",
                        key=f"view_{p['patient_id']}",
                        on_click=go_to_patient_detail,
                        args=(p['patient_id'],),
                        use_container_width=True,
                        type="primary",
                    )

                # Disease-specific risk pill (if filtered)
                if st.session_state.patient_category != "All Users":
                    # Map display category to backend prediction key
                    category_key_map = {
                        "diabetes": "diabetes_risk_level",
                        "liver": "liver_risk_level",
                        "heart": "heart_risk_level",
                        "mental health": "mental_health_risk_level",
                    }
                    cat_lower = st.session_state.patient_category.lower()
                    risk_key = category_key_map.get(cat_lower, f"{cat_lower}_risk_level")
                    level = p.get('latest_prediction', {}).get(risk_key, 'N/A')
                    color = utils.risk_color(level)
                    st.markdown(f"""
                    <div style=\"background: {color}20; padding: 0.5rem 1rem; border-radius: 20px; border: 1px solid {color}; display: inline-block; margin-top: 0.5rem;\">
                        <strong style=\"color: {color}; font-size: 0.9rem;\">{level} Risk</strong>
                    </div>
                    """, unsafe_allow_html=True)

                # Close the card container
                st.markdown("</div>", unsafe_allow_html=True)

                st.divider()

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
        
    st.title(f"Patient Profile: {str(patient_data.get('name') or '').strip().title()}")
    gender_caption = str(patient_data.get('gender', 'N/A') or '').strip().rstrip('.')
    st.caption(f"ABHA ID: {patient_data.get('abha_id')} | Age: {patient_data.get('age')} | Gender: {gender_caption}")
    
    st.divider()
    
    utils.display_risk_table(risk_data)
    
    # Retry Prediction Section
    st.subheader("🔄 Prediction Management")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Retry Prediction", use_container_width=True, type="secondary"):
            with st.spinner("🔄 Retrying ML prediction..."):
                result = api_client.retry_prediction(patient_id)
                if result:
                    st.success("✅ Prediction retry successful!")
                    st.rerun()
                else:
                    st.error("❌ Prediction retry failed. Check if all assessments are complete.")
    
    with col2:
        if st.button("📊 View Latest Prediction", use_container_width=True):
            latest_prediction = api_client.get_latest_prediction(patient_id)
            if latest_prediction:
                st.json(latest_prediction)
            else:
                st.warning("No prediction data available.")
    
    st.divider()

    # --- Added Patient Info & History as per SRD ---
    st.subheader("Patient Information")
    p = patient_data
    st.text(f"Name: {str(p.get('name') or '').strip().title()}")
    st.text(f"ABHA ID: {p.get('abha_id')}")
    st.text(f"Age: {p.get('age')}")
    st.text(f"Gender: {str(p.get('gender') or '').strip().rstrip('.')}")
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

    
    # Consultation Actions Section
    st.subheader("🩺 Consultation Actions")
    
    if not risk_data:
        st.warning("⚠️ No risk assessment found. Cannot book consultation.")
    else:
        st.markdown("Based on the patient's risk levels, the following consultation options are available:")
        
        consultations_booked = []
        
        def book_and_track(disease, level):
            with st.spinner(f"📅 Booking consultation for {disease}..."):
                res = api_client.book_consultation(patient_id, disease, level)
                if res:
                    st.session_state.appointment_success = {
                        'disease': disease,
                        'type': 'In-Person Consultation' if level == 'High' else 'Teleconsultation',
                    }
                    st.session_state.show_appointment_modal = True
                    consultations_booked.append(disease)
                else:
                    st.error(f"❌ Failed to book consultation for {disease}.")

        # Display consultation options based on risk levels
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🚨 High Risk Consultations")
            high_risk_diseases = []
            
        with col2:
            st.markdown("### ⚠️ Medium Risk Consultations")
            medium_risk_diseases = []
        
        # Categorize diseases by risk level
        for risk_key, disease_name in [
            ("diabetes_risk_level", "Diabetes"),
            ("liver_risk_level", "Liver"),
            ("heart_risk_level", "Heart"),
            ("mental_health_risk_level", "Mental Health")
        ]:
            level = risk_data.get(risk_key)
            if level == "High":
                high_risk_diseases.append(disease_name)
            elif level == "Medium":
                medium_risk_diseases.append(disease_name)
        
        # Display high risk consultations
        with col1:
            if high_risk_diseases:
                for disease in high_risk_diseases:
                    st.markdown(f"""
                    <div style="background: var(--color-bg-white); padding: 1rem; border-radius: 8px; border-left: 4px solid var(--color-danger); margin: 0.5rem 0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                        <strong style="color: var(--color-danger); font-size: 1rem;">🚨 {disease} - URGENT CARE REQUIRED</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(
                        f"🏥 Book In-Person Consultation ({disease})", 
                        key=f"high_{disease}", 
                        use_container_width=True,
                        type="primary"
                    ):
                        book_and_track(disease, "High")
                        st.rerun()
            else:
                st.info("No high-risk conditions requiring urgent consultation.")
        
        # Display medium risk consultations
        with col2:
            if medium_risk_diseases:
                for disease in medium_risk_diseases:
                    st.markdown(f"""
                    <div style="background: var(--color-bg-white); padding: 1rem; border-radius: 8px; border-left: 4px solid var(--color-warning); margin: 0.5rem 0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                        <strong style="color: var(--color-warning); font-size: 1rem;">⚠️ {disease} - Monitoring Recommended</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(
                        f"💻 Book Teleconsultation ({disease})", 
                        key=f"medium_{disease}", 
                        use_container_width=True
                    ):
                        book_and_track(disease, "Medium")
                        st.rerun()
            else:
                st.info("No medium-risk conditions requiring consultation.")

    st.divider()
    
    # Appointment Success Card (centered, non-blocking)
    if st.session_state.get('show_appointment_modal'):
        success_data = st.session_state.get('appointment_success', {})
        left, center, right = st.columns([1, 2, 1])
        with center:
            st.markdown(
                f"""
                <div style="background: var(--color-bg-white); border: 1px solid var(--color-border); border-radius: 12px; padding: 1.25rem; box-shadow: 0 4px 16px rgba(0,0,0,0.08); text-align: center;">
                    <div style="font-size: 2.25rem; margin-bottom: 0.5rem;">✅</div>
                    <h3 style="margin: 0 0 0.5rem 0; color: var(--color-success);">Appointment Booked Successfully!</h3>
                    <p style="margin: 0; color: var(--color-text-secondary);"><strong>📋 Disease:</strong> {success_data.get('disease','')}</p>
                    <p style="margin: 0.25rem 0 1rem 0; color: var(--color-text-secondary);"><strong>📋 Type:</strong> {success_data.get('type','')}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("Close", key="close_modal_btn", use_container_width=True, type="primary"):
                    st.session_state.show_appointment_modal = False
                    st.rerun()
            with btn_col2:
                if st.button("Dismiss", key="dismiss_modal_btn", use_container_width=True):
                    st.session_state.show_appointment_modal = False
                    st.rerun()
    
    st.divider()
    st.subheader("📝 Notes for Doctor")
    st.markdown("Add any symptoms, observations, or additional notes that should be shared with the treating doctor:")
    
    with st.form("notes_form"):
        notes = st.text_area(
            "Symptoms (if any) or other notes:", 
            height=150, 
            placeholder="Enter any symptoms, observations, or additional notes for the doctor...",
            help="This information will be visible to the patient and shared with the treating doctor."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            save_notes = st.form_submit_button("💾 Save Notes", use_container_width=True, type="primary")
        with col2:
            clear_notes = st.form_submit_button("🗑️ Clear", use_container_width=True)
        
        if save_notes and notes.strip():
            with st.spinner("💾 Saving notes..."):
                success = api_client.add_consultation_notes(patient_id, notes)
                if success:
                    st.success("✅ Notes saved successfully!")
                    st.toast("✅ Notes saved", icon="✅")
                    st.info("📋 These notes will be visible to the patient and shared with the treating doctor.")
                else:
                    st.error("❌ Failed to save notes.")
        elif save_notes and not notes.strip():
            st.warning("⚠️ Please enter some notes before saving.")
        
        if clear_notes:
            st.rerun()
    
    # Display existing notes
    st.markdown("### 📋 Previous Notes")
    existing_notes = patient_data.get('consultation_notes', [])
    if existing_notes:
        for i, note in enumerate(existing_notes):
            st.markdown(f"""
            <div style="background: var(--color-bg-white); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--color-primary); margin: 0.75rem 0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
                <p style="margin: 0; color: var(--color-text-primary); line-height: 1.5;"><strong>Note #{i+1}:</strong> {note.get('notes', 'No content')}</p>
                <small style="color: var(--color-text-secondary); font-size: 0.85rem;">Added: {note.get('created_at', 'Unknown date')}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("📭 No previous notes found for this patient.")