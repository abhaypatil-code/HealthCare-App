#!/usr/bin/env python3
"""
Quick test to verify admin login and token generation.
"""

import requests
import json

BACKEND_URL = "http://127.0.0.1:5000/api/v1"

def test_admin_login():
    """Test admin login and token generation."""
    print("🔐 Testing admin login...")
    
    try:
        response = requests.post(f"{BACKEND_URL}/auth/admin/login", json={
            "username": "admin",
            "password": "Admin123!"
        })
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login successful!")
            print(f"Admin ID: {data.get('admin_id')}")
            print(f"Name: {data.get('name')}")
            print(f"Token length: {len(data.get('access_token', ''))}")
            return data.get('access_token')
        else:
            print(f"❌ Admin login failed")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server.")
        print("Please make sure the backend is running on http://127.0.0.1:5000")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_token_validation(token):
    """Test if the token is valid."""
    if not token:
        return False
        
    print("\n🔍 Testing token validation...")
    
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BACKEND_URL}/auth/me", headers=headers)
        
        print(f"📊 Token validation status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Token is valid!")
            print(f"User role: {data.get('role')}")
            print(f"User name: {data.get('name')}")
            return True
        else:
            print(f"❌ Token validation failed")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Token validation error: {e}")
        return False

def main():
    print("🧪 Admin Authentication Test")
    print("=" * 30)
    
    # Test login
    token = test_admin_login()
    
    if token:
        # Test token validation
        if test_token_validation(token):
            print("\n✅ All tests passed! Authentication is working.")
            print("You can now use the frontend to create patients.")
        else:
            print("\n❌ Token validation failed. Check backend logs.")
    else:
        print("\n❌ Admin login failed. Run 'python create_admin.py' first.")

if __name__ == "__main__":
    main()
