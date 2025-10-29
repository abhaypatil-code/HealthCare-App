#!/usr/bin/env python3
"""
Script to create the default admin account.
Run this before using the application.
"""

import requests
import json

# Configuration
BACKEND_URL = "http://127.0.0.1:5000/api/v1"

def create_admin_account():
    """Create the default admin account."""
    admin_data = {
        "name": "System Administrator",
        "email": "admin@healthcare.com",
        "username": "admin",
        "password": "Admin123!",
        "designation": "System Administrator",
        "contact_number": "1234567890",
        "facility_name": "Healthcare Management System"
    }
    
    print("🔧 Creating admin account...")
    print(f"Data: {json.dumps(admin_data, indent=2)}")
    
    try:
        response = requests.post(f"{BACKEND_URL}/auth/admin/register", json=admin_data)
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Admin account created successfully!")
            print(f"Admin ID: {data.get('user', {}).get('admin_id')}")
            print(f"Name: {data.get('user', {}).get('name')}")
            return True
        elif response.status_code == 409:
            print("ℹ️ Admin account already exists (this is OK)")
            return True
        else:
            print(f"❌ Failed to create admin account (status: {response.status_code})")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server.")
        print("Please make sure the backend is running on http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_admin_login():
    """Test admin login after creation."""
    print("\n🔐 Testing admin login...")
    
    try:
        response = requests.post(f"{BACKEND_URL}/auth/admin/login", json={
            "username": "admin",
            "password": "Admin123!"
        })
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Admin login successful!")
            print(f"Admin ID: {data.get('admin_id')}")
            print(f"Name: {data.get('name')}")
            print(f"Token received: {'Yes' if data.get('access_token') else 'No'}")
            return True
        else:
            print(f"❌ Admin login failed (status: {response.status_code})")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Login test failed: {e}")
        return False

def main():
    print("🏥 Healthcare System - Admin Setup")
    print("=" * 40)
    
    # Create admin account
    if create_admin_account():
        # Test login
        if test_admin_login():
            print("\n✅ Setup complete! You can now use the application.")
            print("\nNext steps:")
            print("1. Start the frontend: streamlit run app.py")
            print("2. Login with: admin / Admin123!")
            print("3. Create patients and run assessments")
        else:
            print("\n❌ Admin login test failed. Check the error above.")
    else:
        print("\n❌ Admin account creation failed. Check the error above.")

if __name__ == "__main__":
    main()
