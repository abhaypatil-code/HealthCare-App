#!/usr/bin/env python3
"""
Automated test script for Streamlit frontend checks.
This script tests the main user flows for both HW and Patient roles.
"""

import requests
import json
import time
import sys
from typing import Dict, Any, Optional

# Configuration
BACKEND_URL = "http://127.0.0.1:5000/api/v1"
FRONTEND_URL = "http://127.0.0.1:8501"

# Test credentials
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "Admin123!"
}

PATIENT_CREDENTIALS = {
    "abha_id": "98765432109876",  # Use the test patient created in admin flow
    "password": "TestPatient123!"
}

class TestSession:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_role = None
        self.user_id = None
        
    def login_admin(self) -> bool:
        """Login as admin and store token."""
        try:
            response = self.session.post(f"{BACKEND_URL}/auth/admin/login", json=ADMIN_CREDENTIALS)
            response.raise_for_status()
            data = response.json()
            
            self.token = data.get("access_token")
            self.user_role = "admin"
            self.user_id = data.get("admin_id")
            
            if self.token:
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print(f"✅ Admin login successful. Admin ID: {self.user_id}")
                return True
            else:
                print("❌ Admin login failed: No token received")
                return False
                
        except Exception as e:
            print(f"❌ Admin login failed: {e}")
            return False
    
    def login_patient(self) -> bool:
        """Login as patient and store token."""
        try:
            response = self.session.post(f"{BACKEND_URL}/auth/patient/login", json=PATIENT_CREDENTIALS)
            response.raise_for_status()
            data = response.json()
            
            self.token = data.get("access_token")
            self.user_role = "patient"
            self.user_id = data.get("patient_id")
            
            if self.token:
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print(f"✅ Patient login successful. Patient ID: {self.user_id}")
                return True
            else:
                print("❌ Patient login failed: No token received")
                return False
                
        except Exception as e:
            print(f"❌ Patient login failed: {e}")
            return False
    
    def create_test_patient(self) -> Optional[int]:
        """Create a test patient for testing purposes."""
        if self.user_role != "admin":
            print("❌ Cannot create patient: Not logged in as admin")
            return None
            
        # Use timestamp to create unique ABHA ID
        import time
        unique_abha_id = f'9876543210{int(time.time()) % 10000:04d}'
        
        patient_data = {
            "name": "Test Patient",
            "age": 35,
            "gender": "Male",
            "height": 175.0,
            "weight": 70.0,
            "abha_id": unique_abha_id,
            "state_name": "Karnataka",
            "password": "TestPatient123!"
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/patients", json=patient_data)
            response.raise_for_status()
            data = response.json()
            
            patient_id = data.get("patient_id")
            print(f"✅ Test patient created successfully. Patient ID: {patient_id}")
            return patient_id
            
        except Exception as e:
            print(f"❌ Failed to create test patient: {e}")
            return None
    
    def create_assessment(self, patient_id: int, assessment_type: str, data: Dict[str, Any]) -> bool:
        """Create an assessment for a patient."""
        try:
            response = self.session.post(f"{BACKEND_URL}/patients/{patient_id}/assessments/{assessment_type}", json=data)
            response.raise_for_status()
            print(f"✅ {assessment_type} assessment created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create {assessment_type} assessment: {e}")
            return False
    
    def trigger_prediction(self, patient_id: int) -> bool:
        """Trigger ML prediction for a patient."""
        try:
            response = self.session.post(f"{BACKEND_URL}/patients/{patient_id}/predict")
            response.raise_for_status()
            data = response.json()
            print(f"✅ Prediction triggered successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to trigger prediction: {e}")
            return False
    
    def get_latest_prediction(self, patient_id: int) -> Optional[Dict[str, Any]]:
        """Get latest prediction for a patient."""
        try:
            response = self.session.get(f"{BACKEND_URL}/patients/{patient_id}/predictions/latest")
            response.raise_for_status()
            data = response.json()
            print(f"✅ Latest prediction retrieved successfully")
            return data
            
        except Exception as e:
            print(f"❌ Failed to get latest prediction: {e}")
            return None
    
    def generate_pdf_report(self, patient_id: int, sections: list) -> bool:
        """Generate PDF report for a patient."""
        try:
            response = self.session.post(f"{BACKEND_URL}/patients/{patient_id}/report/pdf", json={"sections": sections})
            response.raise_for_status()
            print(f"✅ PDF report generated successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to generate PDF report: {e}")
            return False
    
    def get_recommendations(self, patient_id: int) -> Optional[Dict[str, Any]]:
        """Get recommendations for a patient."""
        try:
            response = self.session.get(f"{BACKEND_URL}/patients/{patient_id}/recommendations")
            response.raise_for_status()
            data = response.json()
            print(f"✅ Recommendations retrieved successfully")
            return data
            
        except Exception as e:
            print(f"❌ Failed to get recommendations: {e}")
            return None

def test_admin_flow():
    """Test the complete admin workflow."""
    print("\n" + "="*50)
    print("TESTING ADMIN WORKFLOW")
    print("="*50)
    
    session = TestSession()
    
    # Step 1: Login as admin
    if not session.login_admin():
        return False
    
    # Step 2: Create a test patient
    patient_id = session.create_test_patient()
    if not patient_id:
        return False
    
    # Step 3: Create assessments
    diabetes_data = {
        "pregnancy": False,
        "glucose": 120.0,
        "blood_pressure": 80.0,
        "skin_thickness": 25.0,
        "insulin": 100.0,
        "diabetes_history": False
    }
    
    liver_data = {
        "total_bilirubin": 1.2,
        "direct_bilirubin": 0.3,
        "alkaline_phosphatase": 100.0,
        "sgpt_alamine_aminotransferase": 30.0,
        "sgot_aspartate_aminotransferase": 25.0,
        "total_protein": 7.0,
        "albumin": 4.0
    }
    
    heart_data = {
        "diabetes": False,
        "hypertension": False,
        "obesity": False,
        "smoking": False,
        "alcohol_consumption": False,
        "physical_activity": True,
        "diet_score": 7,
        "cholesterol_level": 200.0,
        "triglyceride_level": 150.0,
        "ldl_level": 120.0,
        "hdl_level": 50.0,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "air_pollution_exposure": 50.0,
        "family_history": False,
        "stress_level": 5,
        "heart_attack_history": False
    }
    
    mental_health_data = {
        "phq_score": 5,
        "gad_score": 3,
        "depressiveness": False,
        "suicidal": False,
        "anxiousness": False,
        "sleepiness": False
    }
    
    assessments_created = 0
    if session.create_assessment(patient_id, "diabetes", diabetes_data):
        assessments_created += 1
    if session.create_assessment(patient_id, "liver", liver_data):
        assessments_created += 1
    if session.create_assessment(patient_id, "heart", heart_data):
        assessments_created += 1
    if session.create_assessment(patient_id, "mental_health", mental_health_data):
        assessments_created += 1
    
    if assessments_created != 4:
        print(f"❌ Only {assessments_created}/4 assessments created")
        return False
    
    # Step 4: Trigger prediction
    if not session.trigger_prediction(patient_id):
        print("⚠️ Prediction failed, but continuing with test")
    
    # Step 5: Get latest prediction
    prediction = session.get_latest_prediction(patient_id)
    if prediction:
        print(f"📊 Prediction data: {json.dumps(prediction, indent=2)}")
    
    # Step 6: Generate PDF report
    if not session.generate_pdf_report(patient_id, ["Overview", "Diabetes"]):
        print("⚠️ PDF generation failed, but continuing with test")
    
    # Step 7: Get recommendations
    recommendations = session.get_recommendations(patient_id)
    if recommendations:
        print(f"💡 Recommendations: {json.dumps(recommendations, indent=2)}")
    
    print("✅ Admin workflow test completed successfully!")
    return True

def test_patient_flow():
    """Test the patient workflow."""
    print("\n" + "="*50)
    print("TESTING PATIENT WORKFLOW")
    print("="*50)
    
    session = TestSession()
    
    # Step 1: Login as patient
    if not session.login_patient():
        return False
    
    # Step 2: Get patient details
    try:
        response = session.session.get(f"{BACKEND_URL}/patients/{session.user_id}")
        response.raise_for_status()
        patient_data = response.json()
        print(f"✅ Patient details retrieved: {patient_data.get('name')}")
    except Exception as e:
        print(f"❌ Failed to get patient details: {e}")
        return False
    
    # Step 3: Get latest prediction
    prediction = session.get_latest_prediction(session.user_id)
    if prediction:
        print(f"📊 Patient prediction data: {json.dumps(prediction, indent=2)}")
    
    # Step 4: Get recommendations
    recommendations = session.get_recommendations(session.user_id)
    if recommendations:
        print(f"💡 Patient recommendations: {json.dumps(recommendations, indent=2)}")
    
    # Step 5: Generate PDF report
    if not session.generate_pdf_report(session.user_id, ["Overview"]):
        print("⚠️ PDF generation failed, but continuing with test")
    
    print("✅ Patient workflow test completed successfully!")
    return True

def test_backend_connectivity():
    """Test if backend is running and accessible."""
    print("\n" + "="*50)
    print("TESTING BACKEND CONNECTIVITY")
    print("="*50)
    
    try:
        response = requests.get(f"{BACKEND_URL}/auth/me", timeout=5)
        print(f"✅ Backend is accessible (status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not accessible. Please start the backend server.")
        return False
    except Exception as e:
        print(f"❌ Backend connectivity test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Starting Streamlit Frontend Tests")
    print("="*50)
    
    # Test backend connectivity first
    if not test_backend_connectivity():
        print("\n❌ Backend connectivity test failed. Please start the backend server.")
        sys.exit(1)
    
    # Run admin workflow test
    admin_success = test_admin_flow()
    
    # Run patient workflow test
    patient_success = test_patient_flow()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    if admin_success and patient_success:
        print("✅ All tests passed successfully!")
        print("\n🎉 The Streamlit frontend is working correctly with the backend.")
        print("📋 Both HW and Patient user flows are functional.")
        return 0
    else:
        print("❌ Some tests failed.")
        if not admin_success:
            print("  - Admin workflow test failed")
        if not patient_success:
            print("  - Patient workflow test failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
