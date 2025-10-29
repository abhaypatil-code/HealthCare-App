import streamlit as st
import api_client
from utils import logout
from theme import apply_light_theme, create_navbar
import requests

st.set_page_config(
    page_title="HealthCare System", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    page_icon="🩺"
)

# Apply enhanced global theme with compact spacing and sticky header
apply_light_theme()

def check_backend_status():
    """Check if the backend server is running."""
    try:
        response = requests.get("http://127.0.0.1:5000/api/v1/auth/me", timeout=3)
        return True
    except:
        return False

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

# --- Main Content Area ---
if st.session_state.logged_in:
    # Create top navigation bar
    create_navbar(st.session_state.user_name, st.session_state.user_role)
    
    # Welcome section with better visual hierarchy
    st.markdown("---")
    
    # Welcome message in a container for better spacing
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.success(f"Welcome back, {st.session_state.user_name}!")
        with col2:
            st.info(f"Role: **{st.session_state.user_role.title()}**")
        with col3:
            if st.button("Logout", use_container_width=True, type="primary"):
                logout()
    
    st.markdown("---")
    
    # Dashboard redirect section
    with st.container():
        st.info(f"Redirecting to your **{st.session_state.user_role.title()} Dashboard**...")
        
        if st.session_state.user_role == "admin":
            st.switch_page("pages/2_Admin_Dashboard.py")
        else:
            st.switch_page("pages/1_Patient_Dashboard.py")

else:
    # Main login interface - clean and professional layout
    st.markdown("---")
    
    # Header section
    with st.container():
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: var(--color-primary); margin-bottom: 0.5rem; font-size: 2.5rem;">🩺 HealthCare System</h1>
            <p style="color: var(--color-text-secondary); font-size: 1.1rem; margin-bottom: 0.25rem;">Welcome to the Healthcare Management System</p>
            <p style="color: var(--color-text-secondary); font-size: 0.95rem;">Early Disease Detection & Prevention for Rural Healthcare</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Backend status check
    backend_status = check_backend_status()
    if not backend_status:
        st.error("⚠️ **Backend server is not running.** Please start the backend server before logging in.")
        with st.expander("How to start the backend server", expanded=True):
            st.markdown("""
            **To start the backend server:**
            1. Open a new terminal/command prompt
            2. Navigate to the project directory
            3. Run: `cd medml-backend && python run.py`
            4. Wait for the server to start (you'll see "Running on http://127.0.0.1:5000")
            5. Refresh this page
            """)
        st.stop()
    else:
        st.success("🟢 Backend server is running")
    
    st.markdown("---")
    
    # Initialize login type in session state
    if "login_type" not in st.session_state:
        st.session_state.login_type = "admin"
    
    # Login type selector
    with st.container():
        st.markdown("### Select Login Type")
        login_type = st.radio(
            "Choose your role:",
            ["admin", "patient"],
            format_func=lambda x: "👨‍⚕️ Healthcare Worker" if x == "admin" else "👤 Patient",
            horizontal=True,
            key="login_type_selector"
        )
        st.session_state.login_type = login_type
    
    st.markdown("---")
    
    # Login form section with better visual organization
    if st.session_state.login_type == "admin":
        # Admin Login Section
        with st.container():
            st.markdown("### 👨‍⚕️ Healthcare Worker Login")
            st.markdown("Access the admin dashboard to manage patients and assessments")
            
            # Login form in a well-defined container
            with st.container():
                with st.form("admin_login_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        username = st.text_input("Username or Email", placeholder="Enter your username or email", key="admin_username")
                    with col2:
                        password = st.text_input("Password", type="password", placeholder="Enter your password", key="admin_password")
                    
                    submitted = st.form_submit_button("Login as Admin", use_container_width=True, type="primary")
                    
                    if submitted:
                        if not username or not password:
                            st.error("Username/Email and Password are required.")
                        else:
                            with st.spinner("Logging in..."):
                                handle_admin_login(username, password)
        
        # Admin credentials info in a separate container
        with st.container():
            with st.expander("🔑 Admin Credentials", expanded=False):
                st.code("Username: admin\nPassword: admin123", language="text")
    
    else:
        # Patient Login Section
        with st.container():
            st.markdown("### 👤 Patient Login")
            st.markdown("Access your personal health dashboard and reports")
            
            # Login form in a well-defined container
            with st.container():
                with st.form("patient_login_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        abha_id = st.text_input("ABHA ID", placeholder="Enter 14-digit ABHA ID", max_chars=14, key="patient_abha")
                    with col2:
                        password = st.text_input("Password", type="password", placeholder="Enter your password", key="patient_password")
                    
                    submitted = st.form_submit_button("Login as Patient", use_container_width=True, type="primary")
                    
                    if submitted:
                        if len(abha_id) != 14 or not abha_id.isdigit():
                            st.error("ABHA ID must be 14 digits.")
                        elif not password:
                            st.error("Password is required.")
                        else:
                            with st.spinner("Logging in..."):
                                handle_patient_login(abha_id, password)
        
        # Patient information in a separate container
        with st.container():
            with st.expander("ℹ️ Patient Information", expanded=False):
                st.info("""
                Patients need to be registered by a healthcare worker first.
                Contact your healthcare provider if you don't have an account.
                """)
    
    st.markdown("---")
    
    # Footer
    with st.container():
        st.markdown("""
        <div style='text-align: center; color: var(--color-text-secondary); margin-top: 2rem;'>
            <p style="font-size: 0.9rem;">Healthcare Management System | Early Disease Detection & Prevention</p>
            <p style="font-size: 0.8rem;">For rural healthcare workers and patients</p>
        </div>
        """, unsafe_allow_html=True)