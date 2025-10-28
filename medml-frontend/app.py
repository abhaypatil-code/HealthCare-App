import streamlit as st
import api_client
from utils import logout

st.set_page_config(page_title="HealthApp Login", layout="centered")

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "token" not in st.session_state:
    st.session_state.token = None

def handle_patient_login(abha_id, password):
    """Callback for patient login."""
    data = api_client.patient_login(abha_id, password)
    if data:
        st.session_state.logged_in = True
        st.session_state.user_role = "patient"
        st.session_state.token = data.get("access_token")
        st.session_state.user_id = data.get("patient_id")
        st.session_state.user_name = data.get("name")
        st.rerun()

def handle_admin_login(username, password):
    """Callback for admin login."""
    data = api_client.admin_login(username, password)
    if data:
        st.session_state.logged_in = True
        st.session_state.user_role = "admin"
        st.session_state.token = data.get("access_token")
        st.session_state.user_id = data.get("admin_id")
        st.session_state.user_name = data.get("name")
        st.rerun()

# --- Page Logic ---

if st.session_state.logged_in:
    # If already logged in, show welcome and redirect
    st.sidebar.success(f"Welcome, {st.session_state.user_name}!")
    st.sidebar.button("Logout", on_click=logout, use_container_width=True, type="primary")
    
    if st.session_state.user_role == "admin":
        st.write("Redirecting to Admin Dashboard...")
        st.switch_page("pages/2_Admin_Dashboard.py")
    else:
        st.write("Redirecting to Patient Dashboard...")
        st.switch_page("pages/1_Patient_Dashboard.py")

else:
    # If not logged in, show login UI
    st.title("🩺 HealthCare System Login")
    
    patient_tab, admin_tab = st.tabs(["Patient Login", "Admin Login"])

    with patient_tab:
        st.subheader("Patient Login")
        with st.form("patient_login_form"):
            abha_id = st.text_input("ABHA ID (14 digits)", max_chars=14)
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                if len(abha_id) != 14:
                    st.error("ABHA ID must be 14 digits.")
                elif not password:
                    st.error("Password is required.")
                else:
                    handle_patient_login(abha_id, password)

    with admin_tab:
        st.subheader("Admin (Healthcare Worker) Login")
        with st.form("admin_login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            
            if submitted:
                if not username or not password:
                    st.error("Username and Password are required.")
                else:
                    handle_admin_login(username, password)