# 🩺 PreventVance AI — Leading the Future of Early Health Defense

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Kaggle](https://img.shields.io/badge/Datasets-Kaggle-blue?logo=kaggle)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

> **PreventVance AI** is a comprehensive healthcare management system designed for **rural healthcare workers** to manage patient diagnostics and care delivery.  
> The system enables **early detection and preventive care** by identifying individuals at risk of diseases before they become symptomatic.

---

## 🎯 Why This Project Matters

**PreventVance AI** tackles healthcare disparities by bringing AI-driven diagnostics to **rural and underserved areas**.  
Through machine learning and data-driven insights, healthcare workers can proactively identify patients at risk of diseases such as:

- 🩸 **Diabetes**
- ❤️ **Heart Disease**
- 🧠 **Mental Health Disorders**
- 🫀 **Liver Conditions**

This project aims to **democratize access** to advanced medical intelligence, ensuring equitable healthcare access for all — not just those in urban centers.

---

## 🧭 System Overview

**Project Goal:**  
Address critical gaps in diagnosis and treatment accessibility by enabling early detection and preventive care, particularly in underserved rural areas.

**Target Users:**
- **Primary:** Rural healthcare workers managing patient diagnostics and care delivery  
- **Secondary:** Corporate wellness programs seeking employee health monitoring solutions  

**Value Proposition:**  
Transform raw health data into actionable insights, enabling **preventive interventions** and **reducing long-term health complications**.

---

## 🚀 Quick Start

### 💻 Windows Users (Recommended)

1. Double-click **`start_system.bat`** in the project root  
2. Wait for both backend and frontend to start  
3. Open browser at: [http://localhost:8501](http://localhost:8501)  
4. Login with admin credentials:  
   **Username:** `admin` | **Password:** `Admin123!`

### ⚙️ Manual Setup


# Start Backend
cd medml-backend
python run.py

# Start Frontend (new terminal)
cd medml-frontend
streamlit run app.py
✨ Features
🩺 For Healthcare Workers (Admin)
Patient registration with ABHA ID integration

Comprehensive health assessments

AI-powered risk analysis using ML models

Manage teleconsultations and in-person appointments

Analytics Dashboard for real-time metrics

Add clinical notes and observations

👩‍⚕️ For Patients
Personalized health dashboard

Disease-specific risk analysis

AI-driven lifestyle recommendations

Appointment tracking

Downloadable PDF reports

Selective data sharing

🧠 Technical Highlights
ML Integration: Champion models (XGBoost, LightGBM, RF)

AI Recommendations: Google Gemini API-powered insights

Secure Authentication: JWT-based, role-based access

Responsive Design: Optimized Streamlit frontend

Real-time Analytics: Live dashboard metrics

🏗️ System Architecture
🧩 Backend (Flask)
RESTful JSON APIs

SQLite + SQLAlchemy ORM

JWT Authentication

AI Integration via Gemini API

Pre-trained ML models for each disease category

💡 Frontend (Streamlit)
Admin & Patient dashboards

Intuitive, responsive UI

Real-time synchronization

🗄️ Database Schema Overview
Table	Description
Users	Healthcare workers and admins
Patients	Demographics and health data
Assessments	Disease-specific parameters
Risk Predictions	ML risk outputs
Recommendations	AI lifestyle suggestions
Consultations	Appointment details
Notes	Doctor-patient communication

📋 Prerequisites
Python 3.8+

pip

Git

Windows 10/11 or compatible OS

🛠️ Installation & Setup
Step 1: Clone Repository
bash
Copy code
git clone https://github.com/yourusername/HealthCare-App.git
cd HealthCare-App
Step 2: Install Dependencies
bash
Copy code
# Backend
cd medml-backend
pip install -r requirements.txt

# Frontend
cd ../medml-frontend
pip install -r requirements.txt
Step 3: Initialize Database
bash
Copy code
cd ../medml-backend
python create_admin.py
Step 4: Start the Application
Option A (Windows Quick Start):

bash
Copy code
cd ..
start_system.bat
Option B (Manual):

bash
Copy code
cd medml-backend
python run.py
Then:

bash
Copy code
cd ../medml-frontend
streamlit run app.py
🔑 Default Credentials
Admin Login

Username: admin

Email: admin@healthcare.com

Password: Admin123!

Test Patient

ABHA ID: 12345678901234

Password: 12345678901234@Default123

📊 Machine Learning Models
Each disease module uses a champion ML model chosen after extensive evaluation of algorithms (XGBoost, LightGBM, RF, SVM, etc.) on real-world datasets.

Disease	Model	Metric
Diabetes	XGBoost	High F1-score
Heart Disease	LightGBM	Best ROC-AUC
Liver Disease	Random Forest	Balanced Accuracy
Mental Health	XGBoost	Robust Cross-Validation

Risk Levels:

🟢 Low: 0.0 – 0.34

🟡 Medium: 0.35 – 0.69

🔴 High: 0.70 – 1.0

🔧 Configuration
Environment Variables
bash
Copy code
DATABASE_URL=sqlite:///path/to/database.db
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
GEMINI_API_KEY=your-gemini-api-key
CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
🧪 Testing
Automated Tests
bash
Copy code
python test_system.py
cd tests
python streamlit_frontend_checks.py
Manual Testing
Refer to run_manual_checks.md for:

Login flows

Risk analysis

Consultation management

Error handling

Generate 50+ test patients:

bash
Copy code
cd medml-backend
python comprehensive_test_data_generator.py
🔒 Security Features
JWT Authentication

Bcrypt Password Hashing

Role-Based Access Control

Rate Limiting

CORS Protection

Token Revocation

📈 Analytics & Reports
Admin Dashboard:

Daily patient registrations

Risk distribution metrics

Disease-wise analytics

Patient Reports:

Risk summaries

Lifestyle guidance

Medical history

Consultation records

🚨 Troubleshooting
Common fixes:

bash
Copy code
cd medml-backend
python clear_rate_limits.py
python create_admin.py
python test_system.py
If backend port 5000 is busy:

bash
Copy code
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F
For full details, see TROUBLESHOOTING.md.

🤝 Contributing
Fork the repo

Create your branch

Make your changes

Run tests

Submit a PR

📄 License
This project is licensed under the MIT License.

swift
Copy code
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy...
📚 Documentation
🧭 HOW_TO_RUN.md — Setup guide

🧩 BACKEND_DISCOVERY.md — API documentation

💡 setup_frontend.md — Streamlit configuration

🧪 run_manual_checks.md — Manual tests

🧮 TEST_DATA_GENERATOR_README.md — Test data generation

🔮 Future Enhancements
Mobile app integration 📱

Multi-language support 🌐

Real-time notifications 🔔

Cloud deployment ☁️

Wearable device integration ⌚

Advanced analytics & visualization 📊

📞 Support
For technical assistance:

Review TROUBLESHOOTING.md

Run python test_system.py

Check system logs

Email support or open a GitHub issue
