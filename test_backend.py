#!/usr/bin/env python3
"""
Quick test script to verify backend functionality.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_backend():
    """Test basic backend functionality."""
    print("Testing backend connectivity...")
    
    # Test 1: Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/auth/me", timeout=5)
        print(f"✅ Backend is running (status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("❌ Backend server is not running!")
        print("Please start the backend with: cd medml-backend && python run.py")
        return False
    except Exception as e:
        print(f"❌ Backend error: {e}")
        return False
    
    # Test 2: Try admin login
    print("\nTesting admin login...")
    try:
        login_data = {
            "username": "admin@healthcare.com",
            "password": "Admin123!"
        }
        response = requests.post(f"{BASE_URL}/auth/admin/login", json=login_data)
        print(f"Login response status: {response.status_code}")
        print(f"Login response: {response.text}")
        
        if response.status_code == 200:
            login_result = response.json()
            token = login_result.get("access_token")
            print(f"✅ Admin login successful! Token: {token[:20]}...")
            
            # Test 3: Try creating a patient
            print("\nTesting patient creation...")
            headers = {"Authorization": f"Bearer {token}"}
            
            patient_data = {
                "name": "Test Patient",
                "age": 30,
                "gender": "Male",
                "height": 175.0,
                "weight": 70.0,
                "abha_id": "12345678901234",
                "password": "12345678901234@Default123",
                "state_name": "Karnataka"
            }
            
            print(f"Sending patient data: {patient_data}")
            response = requests.post(f"{BASE_URL}/patients", json=patient_data, headers=headers)
            print(f"Patient creation response status: {response.status_code}")
            print(f"Patient creation response: {response.text}")
            
            if response.status_code == 201:
                print("✅ Patient creation successful!")
            else:
                print("❌ Patient creation failed!")
                
        else:
            print("❌ Admin login failed!")
            
    except Exception as e:
        print(f"❌ Login test error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Backend Test Script")
    print("=" * 30)
    test_backend()
