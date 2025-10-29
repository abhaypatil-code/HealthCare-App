#!/usr/bin/env python3
"""
Direct backend API test to debug the JWT issue.
"""

import requests
import json

def test_backend_directly():
    """Test backend API directly."""
    base_url = "http://127.0.0.1:5000/api/v1"
    
    print("🧪 Testing Backend API Directly")
    print("=" * 40)
    
    # Test 1: Check if backend is running
    print("1. Testing backend connectivity...")
    try:
        response = requests.get(f"{base_url}/auth/me", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Backend is running (401 = no auth, expected)")
        else:
            print(f"   ⚠️ Unexpected status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Backend is not running!")
        print("   Please start backend: cd medml-backend && python run.py")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Try admin login
    print("\n2. Testing admin login...")
    try:
        login_data = {
            "username": "admin",
            "password": "Admin123!"
        }
        response = requests.post(f"{base_url}/auth/admin/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"   ✅ Login successful!")
            print(f"   Token length: {len(token) if token else 0}")
            
            # Test 3: Test token validation
            print("\n3. Testing token validation...")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{base_url}/auth/me", headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"   ✅ Token valid!")
                print(f"   User: {user_data.get('name')}")
                print(f"   Role: {user_data.get('role')}")
                
                # Test 4: Try patient creation
                print("\n4. Testing patient creation...")
                patient_data = {
                    "name": "Test Patient",
                    "abha_id": "11111111111111",
                    "password": "11111111111111@Default123",
                    "age": 25,
                    "gender": "Male",
                    "height": 175.0,
                    "weight": 70.0,
                    "state_name": "Karnataka"
                }
                
                response = requests.post(f"{base_url}/patients", json=patient_data, headers=headers)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 201:
                    print("   ✅ Patient creation successful!")
                    return True
                else:
                    print(f"   ❌ Patient creation failed!")
                    try:
                        error_data = response.json()
                        print(f"   Error: {json.dumps(error_data, indent=2)}")
                    except:
                        print(f"   Raw response: {response.text}")
                    return False
            else:
                print(f"   ❌ Token validation failed!")
                try:
                    error_data = response.json()
                    print(f"   Error: {json.dumps(error_data, indent=2)}")
                except:
                    print(f"   Raw response: {response.text}")
                return False
        else:
            print(f"   ❌ Login failed!")
            try:
                error_data = response.json()
                print(f"   Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_backend_directly()
    
    if success:
        print("\n✅ All tests passed! Backend is working correctly.")
        print("The issue might be in the frontend authentication flow.")
    else:
        print("\n❌ Backend tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Run: cd medml-backend && python create_admin.py")
        print("2. Restart backend: cd medml-backend && python run.py")
        print("3. Check database connection")
        print("4. Verify JWT_SECRET_KEY is set")
