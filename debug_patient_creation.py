#!/usr/bin/env python3
"""
Quick test script to debug patient creation issues.
Run this to test the backend API directly.
"""

import requests
import json

# Configuration
BACKEND_URL = "http://127.0.0.1:5000/api/v1"

def test_admin_login():
    """Test admin login to get token."""
    try:
        response = requests.post(f"{BACKEND_URL}/auth/admin/login", json={
            "username": "admin",
            "password": "Admin123!"
        })
        response.raise_for_status()
        data = response.json()
        print(f"✅ Admin login successful: {data.get('name')}")
        return data.get("access_token")
    except Exception as e:
        print(f"❌ Admin login failed: {e}")
        return None

def test_patient_creation(token):
    """Test patient creation with various data."""
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test data
    test_patient = {
        "name": "Test Patient",
        "age": 35,
        "gender": "Male",
        "height": 175.0,
        "weight": 70.0,
        "abha_id": "11111111111111",
        "state_name": "Karnataka",
        "password": "11111111111111@Default123"
    }
    
    print(f"🔍 Testing patient creation with data:")
    print(json.dumps(test_patient, indent=2))
    
    try:
        response = requests.post(f"{BACKEND_URL}/patients", json=test_patient, headers=headers)
        print(f"📊 Response status: {response.status_code}")
        print(f"📊 Response headers: {dict(response.headers)}")
        
        if response.status_code == 201:
            data = response.json()
            print(f"✅ Patient created successfully!")
            print(f"Patient ID: {data.get('patient_id')}")
            print(f"Patient Name: {data.get('name')}")
            return True
        else:
            print(f"❌ Patient creation failed with status {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def test_backend_connectivity():
    """Test if backend is accessible."""
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
    print("🧪 Testing Patient Creation API")
    print("=" * 40)
    
    # Test backend connectivity
    if not test_backend_connectivity():
        return
    
    # Test admin login
    token = test_admin_login()
    if not token:
        return
    
    # Test patient creation
    print("\n" + "=" * 40)
    print("Testing Patient Creation")
    print("=" * 40)
    
    success = test_patient_creation(token)
    
    if success:
        print("\n✅ All tests passed! Patient creation is working.")
    else:
        print("\n❌ Patient creation failed. Check the error details above.")
        print("\nCommon issues:")
        print("1. Password doesn't meet complexity requirements")
        print("2. ABHA ID already exists")
        print("3. Validation errors in data")
        print("4. Backend database issues")

if __name__ == "__main__":
    main()
