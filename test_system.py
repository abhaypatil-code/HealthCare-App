#!/usr/bin/env python3
"""
Comprehensive test script for the Healthcare Management System.
This script tests the entire system end-to-end.
"""

import os
import sys
import requests
import json
import time
import subprocess
import threading
from datetime import datetime

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'medml-backend'))

def test_backend_startup():
    """Test if the backend can start successfully."""
    print("Testing backend startup...")
    
    try:
        from app import create_app
        from app.models import db, User, Patient
        
        app = create_app('development')
        with app.app_context():
            # Test database connection
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            print("✅ Backend startup test passed!")
            return True
            
    except Exception as e:
        print(f"❌ Backend startup test failed: {e}")
        return False

def test_database_tables():
    """Test if all required database tables exist."""
    print("Testing database tables...")
    
    try:
        from app import create_app
        from app.models import db, User, Patient, DiabetesAssessment, LiverAssessment, HeartAssessment, MentalHealthAssessment, RiskPrediction, LifestyleRecommendation, Consultation, ConsultationNote, TokenBlocklist
        
        app = create_app('development')
        with app.app_context():
            # Test if all tables exist by querying them
            tables_to_test = [
                User, Patient, DiabetesAssessment, LiverAssessment, 
                HeartAssessment, MentalHealthAssessment, RiskPrediction, 
                LifestyleRecommendation, Consultation, ConsultationNote, TokenBlocklist
            ]
            
            for table in tables_to_test:
                try:
                    db.session.query(table).first()
                    print(f"✅ Table {table.__tablename__} exists")
                except Exception as e:
                    print(f"❌ Table {table.__tablename__} missing: {e}")
                    return False
            
            print("✅ All database tables exist!")
            return True
            
    except Exception as e:
        print(f"❌ Database tables test failed: {e}")
        return False

def test_ml_models():
    """Test if ML models can be loaded."""
    print("Testing ML models...")
    
    try:
        from app import create_app
        from app.services import models, load_models
        
        app = create_app('development')
        with app.app_context():
            load_models(app)
            
            model_names = ['diabetes', 'heart', 'liver', 'mental_health']
            for model_name in model_names:
                if models[model_name] is not None:
                    print(f"✅ {model_name} model loaded successfully")
                else:
                    print(f"❌ {model_name} model failed to load")
                    return False
            
            print("✅ All ML models loaded successfully!")
            return True
            
    except Exception as e:
        print(f"❌ ML models test failed: {e}")
        return False

def test_api_endpoints():
    """Test if API endpoints are accessible."""
    print("Testing API endpoints...")
    
    base_url = "http://127.0.0.1:5000/api/v1"
    
    # Test endpoints that don't require authentication
    test_endpoints = [
        "/auth/admin/login",
        "/auth/patient/login",
    ]
    
    for endpoint in test_endpoints:
        try:
            response = requests.post(f"{base_url}{endpoint}", 
                                   json={"test": "data"}, 
                                   timeout=5)
            # We expect 422 (validation error) or 401 (auth error), not 500 (server error)
            if response.status_code in [422, 401]:
                print(f"✅ Endpoint {endpoint} is accessible")
            else:
                print(f"⚠️ Endpoint {endpoint} returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Endpoint {endpoint} - Backend server not running")
            return False
        except Exception as e:
            print(f"❌ Endpoint {endpoint} failed: {e}")
            return False
    
    print("✅ API endpoints are accessible!")
    return True

def test_admin_creation():
    """Test if admin user can be created."""
    print("Testing admin user creation...")
    
    try:
        from app import create_app
        from app.models import db, User
        from flask_bcrypt import Bcrypt
        
        app = create_app('development')
        with app.app_context():
            # Check if admin already exists
            existing_admin = User.query.filter_by(email='admin@healthcare.com').first()
            if existing_admin:
                print("✅ Admin user already exists")
                return True
            
            # Create admin user
            bcrypt = Bcrypt()
            password_hash = bcrypt.generate_password_hash('Admin123!').decode('utf-8')
            
            admin = User(
                name='System Administrator',
                email='admin@healthcare.com',
                username='admin',
                password_hash=password_hash,
                designation='System Administrator',
                contact_number='+91-9876543210',
                facility_name='Healthcare Management System',
                role='admin'
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("✅ Admin user created successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Admin user creation failed: {e}")
        return False

def test_patient_creation():
    """Test if a patient can be created."""
    print("Testing patient creation...")
    
    try:
        from app import create_app
        from app.models import db, User, Patient
        from flask_bcrypt import Bcrypt
        
        app = create_app('development')
        with app.app_context():
            # Get admin user
            admin = User.query.filter_by(email='admin@healthcare.com').first()
            if not admin:
                print("❌ Admin user not found")
                return False
            
            # Create test patient
            bcrypt = Bcrypt()
            password_hash = bcrypt.generate_password_hash('Patient123!').decode('utf-8')
            
            # Use a unique ABHA ID with timestamp to avoid conflicts
            import time
            unique_abha_id = f'1234567890{int(time.time()) % 10000:04d}'
            
            patient = Patient(
                name='Test Patient',
                age=30,
                gender='Male',
                height=175.0,
                weight=70.0,
                abha_id=unique_abha_id,
                password_hash=password_hash,
                state_name='Karnataka',
                created_by_admin_id=admin.id
            )
            
            db.session.add(patient)
            db.session.commit()
            
            print("✅ Patient created successfully!")
            return True
            
    except Exception as e:
        print(f"❌ Patient creation failed: {e}")
        return False

def test_ml_prediction():
    """Test if ML prediction works."""
    print("Testing ML prediction...")
    
    try:
        from app import create_app
        from app.models import db, Patient, DiabetesAssessment, LiverAssessment, HeartAssessment, MentalHealthAssessment, RiskPrediction
        from app.services import run_prediction
        
        app = create_app('development')
        with app.app_context():
            # Get the most recently created test patient
            patient = Patient.query.filter(Patient.abha_id.like('1234567890%')).order_by(Patient.created_at.desc()).first()
            if not patient:
                print("❌ Test patient not found")
                return False
            
            # Create test assessments
            diabetes_assessment = DiabetesAssessment(
                patient_id=patient.id,
                pregnancy=False,
                glucose=120.0,
                blood_pressure=80.0,
                skin_thickness=25.0,
                insulin=100.0,
                diabetes_history=False
            )
            
            liver_assessment = LiverAssessment(
                patient_id=patient.id,
                total_bilirubin=1.2,
                direct_bilirubin=0.3,
                alkaline_phosphatase=100.0,
                sgpt_alamine_aminotransferase=25.0,
                sgot_aspartate_aminotransferase=30.0,
                total_protein=7.0,
                albumin=4.0
            )
            
            heart_assessment = HeartAssessment(
                patient_id=patient.id,
                diabetes=False,
                hypertension=False,
                obesity=False,
                smoking=False,
                alcohol_consumption=False,
                physical_activity=True,
                diet_score=7,
                cholesterol_level=200.0,
                triglyceride_level=150.0,
                ldl_level=120.0,
                hdl_level=50.0,
                systolic_bp=120,
                diastolic_bp=80,
                air_pollution_exposure=2.0,
                family_history=False,
                stress_level=3,
                heart_attack_history=False
            )
            
            mental_health_assessment = MentalHealthAssessment(
                patient_id=patient.id,
                phq_score=5,
                gad_score=3,
                depressiveness=False,
                suicidal=False,
                anxiousness=False,
                sleepiness=False
            )
            
            db.session.add(diabetes_assessment)
            db.session.add(liver_assessment)
            db.session.add(heart_assessment)
            db.session.add(mental_health_assessment)
            db.session.commit()
            
            # Test predictions
            diabetes_score = run_prediction('diabetes', patient.get_latest_diabetes_features())
            liver_score = run_prediction('liver', patient.get_latest_liver_features())
            heart_score = run_prediction('heart', patient.get_latest_heart_features())
            mental_health_score = run_prediction('mental_health', patient.get_latest_mental_health_features())
            
            print(f"✅ Diabetes prediction: {diabetes_score:.3f}")
            print(f"✅ Liver prediction: {liver_score:.3f}")
            print(f"✅ Heart prediction: {heart_score:.3f}")
            print(f"✅ Mental health prediction: {mental_health_score:.3f}")
            
            return True
            
    except Exception as e:
        print(f"❌ ML prediction test failed: {e}")
        return False

def run_backend_server():
    """Run the backend server in a separate thread."""
    try:
        from app import create_app
        app = create_app('development')
        app.run(debug=False, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"Backend server error: {e}")

def main():
    """Run all tests."""
    print("Healthcare Management System - Comprehensive Test")
    print("=" * 60)
    
    tests = [
        ("Backend Startup", test_backend_startup),
        ("Database Tables", test_database_tables),
        ("ML Models", test_ml_models),
        ("Admin Creation", test_admin_creation),
        ("Patient Creation", test_patient_creation),
        ("ML Prediction", test_ml_prediction),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name:20} : {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The system is ready to use.")
        print("\nNext steps:")
        print("1. Start the backend server: python run.py")
        print("2. Start the frontend: streamlit run app.py")
        print("3. Use admin credentials: admin@healthcare.com / Admin123!")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please fix the issues before proceeding.")
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)