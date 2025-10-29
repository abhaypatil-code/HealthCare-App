PreventVance AI — Leading the Future of Early Health Defense
A comprehensive healthcare management system designed for rural healthcare workers to manage patient diagnostics and care delivery. The system enables early detection and preventive care by identifying individuals at risk of diseases before they become symptomatic.

🎯 Why This Project Matters
Addressing Healthcare Disparities: This project, PreventVance AI, tackles the critical healthcare gap in rural and underserved areas where access to specialized medical care is limited. By leveraging machine learning and AI technologies, we enable healthcare workers to identify patients at risk of developing serious conditions like diabetes, heart disease, liver disorders, and mental health issues before they become symptomatic. This proactive approach not only saves lives but also reduces healthcare costs by preventing complications that require expensive treatments. The system democratizes access to advanced diagnostic capabilities, ensuring that quality healthcare is not just a privilege of urban areas but reaches every corner of our communities, ultimately creating a more equitable healthcare system for all.

🎯 System Overview
Project Goal: Address critical gaps in diagnosis and treatment accessibility by enabling early detection and preventive care, particularly in underserved rural areas.

Target Users:

Primary: Rural healthcare workers who manage patient diagnostics and care delivery

Secondary: Corporate wellness programs seeking employee health monitoring solutions

Value Proposition: Bridge the healthcare delivery gap in rural areas by proactively identifying at-risk individuals before conditions become symptomatic. Transform raw health data into actionable insights, enabling preventive interventions and reducing long-term health complications.

🚀 Quick Start
Windows Users (Recommended)
Double-click start_system.bat in the project root

Wait for both backend and frontend to start

Open browser to: http://localhost:8501

Login with admin credentials: admin / Admin123!

Manual Setup
Bash

# Start Backend
cd medml-backend
python run.py

# Start Frontend (new terminal)
cd medml-frontend
streamlit run app.py
🚀 Features
For Healthcare Workers (Admin)
Patient Registration: Complete patient management with ABHA ID integration

Health Assessments: Comprehensive assessments for Diabetes, Liver, Heart, and Mental Health

AI-Powered Risk Analysis: ML models predict disease risk levels (Low/Medium/High)

Consultation Management: Book teleconsultations and in-person consultations based on risk levels

Analytics Dashboard: Real-time metrics and risk summaries

Notes Management: Add symptoms and observations for doctors

For Patients
Health Dashboard: Comprehensive health overview with BMI, risk assessments, and recommendations

Disease-Specific Tabs: Detailed risk analysis for each disease category

Lifestyle Recommendations: Personalized guidance based on risk levels

Appointment Tracking: View upcoming consultations

PDF Reports: Download comprehensive health reports

Data Sharing: Share selected health information

Technical Features
ML Integration: Integrates the best-performing pre-trained models (e.g., XGBoost, LightGBM) selected from a rigorous data science pipeline for high-accuracy predictions.

AI Recommendations: Gemini API-powered personalized lifestyle guidance

Secure Authentication: JWT-based authentication with role-based access control

PDF Generation: Dynamic report generation with selective sections

Responsive Design: Works on multiple device types

Real-time Analytics: Live dashboard metrics

🏗️ System Architecture
Backend (Flask)
RESTful API: JSON-based communication

Database: SQLite with SQLAlchemy ORM

Authentication: JWT tokens with refresh mechanism

ML Models: Pre-trained, production-ready models. These models are the champions from a comprehensive ML pipeline that trained and evaluated numerous classifiers (XGBoost, LightGBM, RF, etc.) on real-world datasets to ensure the highest accuracy for each specific disease.

AI Integration: Google Gemini API for recommendations

Frontend (Streamlit)
Admin Dashboard: Patient management and analytics

Patient Portal: Health monitoring and recommendations

Responsive UI: Modern, intuitive interface

Real-time Updates: Live data synchronization

Database Schema
Users: Healthcare workers (admins)

Patients: Patient demographic and health data

Assessments: Disease-specific health parameters

Risk Predictions: ML model outputs with risk levels

Recommendations: AI-generated lifestyle guidance

Consultations: Appointment management

Notes: Doctor communication

📋 Prerequisites
Python 3.8 or higher

pip (Python package manager)

Git (for cloning the repository)

🛠️ Installation & Setup
Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8 or higher (Download Python)

pip (usually comes with Python)

Git (Download Git)

Windows 10/11 (for batch files) or any OS for manual setup

Step 1: Clone the Repository
Bash

git clone https://github.com/yourusername/HealthCare-App.git
cd HealthCare-App
Step 2: Install Dependencies
Backend Dependencies
Bash

cd medml-backend
pip install -r requirements.txt
Frontend Dependencies
Bash

cd ../medml-frontend
pip install -r requirements.txt
Step 3: Initialize Database
Bash

cd ../medml-backend
python create_admin.py
This creates the database and sets up the default admin account.

Step 4: Start the Application
Option A: Quick Start (Windows)
Bash

cd ..
start_system.bat
Option B: Manual Startup
Terminal 1 - Backend:

Bash

cd medml-backend
python run.py
Wait for: Running on http://127.0.0.1:5000

Terminal 2 - Frontend:

Bash

cd medml-frontend
streamlit run app.py
Wait for: You can now view your Streamlit app in your browser.

Step 5: Access the Application
Open your browser and navigate to: http://localhost:8501

Step 6: Login
Use the default credentials:

Admin Username: admin

Admin Password: Admin123!

⚠️ Troubleshooting Setup Issues
Common Setup Problems
Backend won't start:

Bash

# Check if port 5000 is available
netstat -ano | findstr :5000

# Kill process using port 5000 (Windows)
taskkill /PID <PID_NUMBER> /F

# Reinstall dependencies
cd medml-backend
pip install -r requirements.txt --force-reinstall
Frontend won't load:

Bash

# Install Streamlit
pip install streamlit

# Install frontend dependencies
cd medml-frontend
pip install -r requirements.txt
Database errors:

Bash

# Recreate database
cd medml-backend
python create_admin.py
Rate limiting errors (429):

Bash

# Clear rate limits
cd medml-backend
python clear_rate_limits.py
For detailed troubleshooting, see TROUBLESHOOTING.md

🔑 Default Credentials
Admin Login
Username: admin

Email: admin@healthcare.com

Password: Admin123!

Test Patient Login
ABHA ID: 12345678901234

Password: 12345678901234@Default123

Generate Test Data
For comprehensive testing with 50+ patients:

Bash

cd medml-backend
python comprehensive_test_data_generator.py
📊 ML Models
The intelligence of this system comes from a rigorous and data-centric ML pipeline. The models used are not just off-the-shelf; they are the "champion" models selected after exhaustive testing.

Real-World, Relevant Data: The models were trained on real-world datasets, including those specific to Indian demographics, to ensure the highest possible accuracy and relevance for the target population.

Rigorous Model Selection: For each of the four disease categories, a wide array of machine learning algorithms (such as Logistic Regression, Random Forest, SVM, KNN, XGBoost, and LightGBM) were trained, tuned, and evaluated.

Best-in-Class Performance: The system automatically selects and integrates only the best-performing model (based on F1-score and other metrics) for each specific disease. This ensures that the risk prediction for diabetes, for example, uses the most accurate classifier for that unique dataset, which may be different from the best model for heart disease.

This process ensures that PreventVance AI operates with the highest-fidelity predictions possible, moving beyond a one-size-fits-all approach.

Risk Levels
Low Risk: Preventive care and lifestyle maintenance

Medium Risk: Enhanced monitoring and teleconsultation

High Risk: Urgent care and in-person consultation

🔧 Configuration
Environment Variables (Optional)
Bash

# Database
DATABASE_URL=sqlite:///path/to/database.db

# Security
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key

# AI Integration
GEMINI_API_KEY=your-gemini-api-key

# CORS
CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
Risk Thresholds
The system uses configurable risk thresholds:

Low: 0.0 - 0.34

Medium: 0.35 - 0.69

High: 0.70 - 1.0

🧪 Testing
Automated Testing
Bash

# System-wide tests
python test_system.py

# Frontend-specific tests
cd tests
python streamlit_frontend_checks.py
Manual Testing
Follow comprehensive test cases in run_manual_checks.md:

Admin login and dashboard access

Patient registration and assessment flow

ML prediction triggering

Patient dashboard and reports

Error handling scenarios

Test Data Generation
Generate 50+ test patients for intensive testing:

Bash

cd medml-backend
python comprehensive_test_data_generator.py
python verify_test_data.py
📱 Usage
For Healthcare Workers
Login with admin credentials

Add New User to register patients

Complete Health Assessments for all 4 disease categories

Run Risk Analysis to get ML predictions

Book Consultations based on risk levels

Add Notes for doctors

View Analytics on the dashboard

For Patients
Login with ABHA ID and password

View Health Overview with risk assessments

Check Disease-Specific Tabs for detailed analysis

Review Lifestyle Recommendations

Download PDF Reports

Share Health Information

🔒 Security Features
JWT Authentication: Secure token-based authentication

Password Hashing: Bcrypt encryption for passwords

Role-Based Access: Admin and patient role separation

Rate Limiting: API rate limiting to prevent abuse

CORS Protection: Cross-origin resource sharing controls

Token Revocation: JWT token blacklisting for logout

📈 Analytics & Reporting
Admin Dashboard Metrics
Today's registrations

Users at risk by disease category

Risk level distributions

Patient management statistics

Patient Reports
Comprehensive health summaries

Risk assessment details

Lifestyle recommendations

Medical history

Consultation records

🚨 Troubleshooting
Quick Fixes
Bash

# Clear rate limits
cd medml-backend
python clear_rate_limits.py

# Recreate database
python create_admin.py

# Check system status
python test_system.py
Common Issues
Rate Limiting: Run python clear_rate_limits.py

Backend Won't Start: Check port 5000 availability

Frontend Won't Load: Ensure backend is running

ML Models Missing: Check models_store/ directory

Database Errors: Recreate with python create_admin.py

Detailed Troubleshooting
See TROUBLESHOOTING.md for comprehensive solutions to:

Authentication issues

ML prediction failures

Database problems

API connectivity issues

Performance optimization

🤝 Contributing
Fork the repository

Create a feature branch

Make your changes

Run tests

Submit a pull request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Support
For support and questions:

Check the troubleshooting section

Run the test suite to identify issues

Review the logs for error details

📚 Documentation
Setup Guide: HOW_TO_RUN.md - Complete installation and startup instructions

Troubleshooting: TROUBLESHOOTING.md - Comprehensive problem-solving guide

Backend API: BACKEND_DISCOVERY.md - Complete API documentation

Frontend Setup: setup_frontend.md - Streamlit frontend configuration

Test Cases: run_manual_checks.md - Manual testing procedures

Test Data: medml-backend/TEST_DATA_GENERATOR_README.md - Test data generation

Changelog: CHANGELOG_STREAMLIT.md - Recent changes and improvements

🔮 Future Enhancements
Mobile app development

Integration with hospital systems

Advanced analytics and reporting

Multi-language support

Cloud deployment options

Real-time notifications

Integration with wearable devices

Enhanced ML model accuracy

Telemedicine integration

Patient portal mobile app

📞 Support
For technical support:

Check TROUBLESHOOTING.md for common issues

Run python test_system.py for system diagnostics

Review logs for detailed error information

Follow manual test cases in run_manual_checks.md

PreventVance AI - Empowering rural healthcare through technology
