import requests
import json
import os

BACKEND_URL = "http://127.0.0.1:5000/api/v1"

def verify_pdf():
    print("🧪 Verifying PDF Generation...")
    
    # 1. Login as Admin
    try:
        login_resp = requests.post(f"{BACKEND_URL}/auth/admin/login", json={
            "username": "admin",
            "password": "Admin123!"
        })
        if login_resp.status_code != 200:
            print(f"❌ Admin login failed: {login_resp.text}")
            return
        
        token = login_resp.json().get('access_token')
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Admin logged in.")
        
        # 2. Get a Patient
        patients_resp = requests.get(f"{BACKEND_URL}/patients", headers=headers)
        if patients_resp.status_code != 200:
            print(f"❌ Failed to fetch patients: {patients_resp.text}")
            return
            
        patients = patients_resp.json().get('data', [])
        if not patients:
            print("⚠️ No patients found. Cannot verify PDF generation without a patient.")
            return
            
        patient_id = patients[0]['patient_id']
        print(f"✅ Found patient ID: {patient_id}")
        
        # 3. Request PDF
        print(f"📄 Requesting PDF for patient {patient_id}...")
        pdf_payload = {
            "sections": ["Overview", "Diabetes", "Heart", "Liver", "Mental Health"]
        }
        
        pdf_resp = requests.post(
            f"{BACKEND_URL}/patients/{patient_id}/report/pdf", 
            json=pdf_payload,
            headers=headers
        )
        
        if pdf_resp.status_code == 200:
            content_type = pdf_resp.headers.get('Content-Type')
            content_length = len(pdf_resp.content)
            
            print(f"✅ PDF Response Received!")
            print(f"   Status: {pdf_resp.status_code}")
            print(f"   Content-Type: {content_type}")
            print(f"   Size: {content_length} bytes")
            
            if 'application/pdf' in content_type and content_length > 0:
                # Save to file to manually check if needed
                filename = f"test_report_{patient_id}.pdf"
                with open(filename, 'wb') as f:
                    f.write(pdf_resp.content)
                print(f"✅ PDF saved to {filename}")
                return True
            else:
                print("❌ Invalid PDF response content.")
        else:
            print(f"❌ PDF generation failed: {pdf_resp.status_code} - {pdf_resp.text}")
            
    except Exception as e:
        print(f"❌ Error during verification: {e}")

if __name__ == "__main__":
    verify_pdf()
