import streamlit as st
from theme import create_risk_badge, create_metric_card

def risk_color(level):
    """Returns a color based on risk level."""
    if level == "High":
        return "#ef4444"  # Red-500
    if level == "Medium":
        return "#f59e0b"  # Amber-500
    if level == "Low":
        return "#10b981"  # Emerald-500
    return "#64748b"  # Slate-500

def styled_metric(label, value, help_text=None):
    """Creates a styled metric card."""
    st.markdown(f"""
    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
        <h3 style="margin: 0; padding: 0; color: #555;">{label}</h3>
        <p style="font-size: 24px; font-weight: bold; margin: 0; padding: 0;">{value}</p>
        {f'<p style="font-size: 14px; color: #888; margin: 0; padding: 0;">{help_text}</p>' if help_text else ""}
    </div>
    """, unsafe_allow_html=True)

def display_risk_table(risk_data):
    """Displays the main risk assessment table."""
    if not risk_data:
        st.warning("No risk assessment has been performed yet.")
        return

    data = [
        {"Disease": "Diabetes", "Risk Level": risk_data.get('diabetes_risk_level', 'N/A')},
        {"Disease": "Liver Disease", "Risk Level": risk_data.get('liver_risk_level', 'N/A')},
        {"Disease": "Heart Disease", "Risk Level": risk_data.get('heart_risk_level', 'N/A')},
        {"Disease": "Mental Health", "Risk Level": risk_data.get('mental_health_risk_level', 'N/A')}
    ]
    
    st.subheader("Disease Risk Assessment")
    
    for item in data:
        level = item['Risk Level']
        badge_html = create_risk_badge(level)
        st.markdown(f"""
        <div class="card" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.1em; font-weight: 500; color: var(--text-primary);">{item['Disease']}</span>
            {badge_html}
        </div>
        """, unsafe_allow_html=True)

def logout():
    """Clears session state and returns to login."""
    keys_to_clear = [
        "logged_in", "user_role", "user_id", "user_name", "token", 
        "admin_view", "add_user_step", "new_patient_id", "new_patient_name",
        "assessment_status", "view_patient_id", "edit_patient_data"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def check_login(role=None):
    """Checks if user is logged in and has the correct role."""
    if not st.session_state.get("logged_in", False):
        st.error("Access Denied. Please log in first.")
        st.switch_page("app.py")
    
    if role and st.session_state.get("user_role") != role:
        st.error(f"Access Denied. You must be a {role}.")
        st.switch_page("app.py")


INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", 
    "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", 
    "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", 
    "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", 
    "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", 
    "West Bengal", "Andaman and Nicobar Islands", "Chandigarh", 
    "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", 
    "Ladakh", "Lakshadweep", "Puducherry"
]