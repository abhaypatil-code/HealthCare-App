import streamlit as st
import requests
import json

# --- FIX: Updated BASE_URL to include /v1 ---
BASE_URL = "http://127.0.0.1:5000/api/v1"

def get_token():
    """Retrieves the auth token from session state."""
    return st.session_state.get("token")

def get_auth_headers():
    """Returns authorization headers."""
    token = get_token()
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

# --- Authentication ---

def patient_login(abha_id, password):
    """Logs in a patient."""
    try:
        response = requests.post(f"{BASE_URL}/auth/patient/login", json={
            "abha_id": abha_id,
            "password": password
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Login Failed: {e.response.json().get('message', 'Unknown error')}")
        return None

def admin_login(username, password):
    """Logs in an admin."""
    try:
        response = requests.post(f"{BASE_URL}/auth/admin/login", json={
            "username": username,
            "password": password
        })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Login Failed: {e.response.json().get('message', 'Unknown error')}")
        return None

# --- Admin: Dashboard & Patient Management ---

def get_dashboard_stats():
    """Fetches admin dashboard analytics."""
    try:
        response = requests.get(f"{BASE_URL}/dashboard/stats", headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching stats: {e}")
        return None

def add_patient(data):
    """Adds a new patient (Step 1)."""
    try:
        response = requests.post(f"{BASE_URL}/patients", json=data, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error adding patient: {e.response.json().get('message', 'Check fields')}")
        return None

def update_patient(patient_id, data):
    """Updates an existing patient's basic info."""
    try:
        response = requests.put(f"{BASE_URL}/patients/{patient_id}", json=data, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating patient: {e.response.json().get('message', 'Check fields')}")
        return None

def get_patients(category=None, sort=None):
    """Gets a list of registered patients with filters."""
    params = {}
    if category and category != "All Users":
        params['disease'] = category.lower()
    if sort:
        params['sort'] = sort.lower().replace(" ", "_")
        
    try:
        response = requests.get(f"{BASE_URL}/patients", headers=get_auth_headers(), params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching patients: {e}")
        return []

# --- Admin: Assessments ---

def add_assessment(patient_id, assessment_type, data):
    """Adds a new assessment for a patient."""
    try:
        url = f"{BASE_URL}/patients/{patient_id}/assessments/{assessment_type}"
        response = requests.post(url, json=data, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error saving {assessment_type} data: {e.response.json().get('message', 'Check fields')}")
        return None

def trigger_prediction(patient_id):
    """Triggers the ML prediction pipeline for a patient."""
    try:
        url = f"{BASE_URL}/patients/{patient_id}/predict"
        response = requests.post(url, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error triggering prediction: {e}")
        return None

# --- Admin: Consultations ---

def book_consultation(patient_id, disease, risk_level):
    """Books a consultation."""
    data = {
        "patient_id": patient_id,
        "disease": disease,
        "consultation_type": "teleconsultation" if risk_level == "Medium" else "in_person"
    }
    try:
        url = f"{BASE_URL}/consultations"
        response = requests.post(url, json=data, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error booking consultation: {e}")
        return None

def add_consultation_notes(patient_id, notes):
    """Adds admin notes for the doctor."""
    try:
        url = f"{BASE_URL}/consultations/notes"
        response = requests.post(url, json={"patient_id": patient_id, "notes": notes}, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error saving notes: {e}")
        return None

# --- Patient & Shared ---

def get_patient_details(patient_id):
    """Fetches all details for a single patient."""
    try:
        url = f"{BASE_URL}/patients/{patient_id}"
        response = requests.get(url, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching patient details: {e}")
        return None

def get_latest_prediction(patient_id):
    """Fetches the latest risk prediction for a patient."""
    try:
        url = f"{BASE_URL}/patients/{patient_id}/predictions/latest"
        response = requests.get(url, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # It's ok if no prediction exists yet
        if e.response.status_code == 404:
            return None
        st.error(f"Error fetching predictions: {e}")
        return None

def get_recommendations(patient_id):
    """Fetches lifestyle recommendations for a patient."""
    try:
        url = f"{BASE_URL}/patients/{patient_id}/recommendations"
        response = requests.get(url, headers=get_auth_headers())
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching recommendations: {e}")
        return {"diet": [], "exercise": [], "sleep": [], "lifestyle": []}

def get_pdf_report(patient_id, sections):
    """Downloads the patient report as a PDF."""
    try:
        url = f"{BASE_URL}/patients/{patient_id}/report/pdf"
        response = requests.post(url, json={"sections": sections}, headers=get_auth_headers())
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        st.error(f"Error generating PDF: {e}")
        return None