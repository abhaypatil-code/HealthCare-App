# Backend Discovery Summary

## Overview
This document summarizes the discovery of API endpoints, authentication patterns, ML prediction flows, and database models in the HealthCare App backend. The system provides a comprehensive RESTful API for healthcare management with ML-powered disease prediction capabilities.

## System Architecture

### Technology Stack
- **Backend Framework**: Flask with Flask-RESTful
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens) with Flask-JWT-Extended
- **ML Models**: XGBoost, LightGBM with scikit-learn
- **AI Integration**: Google Gemini API for recommendations
- **PDF Generation**: FPDF library
- **Rate Limiting**: Flask-Limiter

## Authentication System
- **Method**: JWT (JSON Web Tokens)
- **Implementation**: Flask-JWT-Extended
- **Token Storage**: Access token + Refresh token
- **Token Header**: `Authorization: Bearer <token>`
- **Token Expiry**: Access tokens (15 min), Refresh tokens (30 days)
- **Logout**: Token blocklisting system
- **Rate Limiting**: Applied to login endpoints (10/min for login, 5/hour for registration)
- **Password Security**: Bcrypt hashing with salt
- **Role-Based Access**: Admin and Patient roles with different permissions

## API Endpoints Summary

### Authentication Endpoints
1. **POST /auth/admin/register** - Register new healthcare worker
2. **POST /auth/admin/login** - Admin login (username/email + password)
3. **POST /auth/patient/login** - Patient login (ABHA ID + password)
4. **POST /auth/refresh** - Refresh access token
5. **POST /auth/logout** - Logout and blocklist token
6. **GET /auth/me** - Get current user profile

### Patient Management Endpoints
7. **POST /patients** - Create new patient (admin only)
8. **GET /patients** - List patients with filtering (admin only)
9. **GET /patients/{id}** - Get patient details (admin/patient - patient can only access own)
10. **PUT /patients/{id}** - Update patient info (admin only)

### Assessment Endpoints
11. **POST /patients/{id}/assessments/diabetes** - Create diabetes assessment
12. **POST /patients/{id}/assessments/liver** - Create liver assessment
13. **POST /patients/{id}/assessments/heart** - Create heart assessment
14. **POST /patients/{id}/assessments/mental_health** - Create mental health assessment
15. **GET /patients/{id}/assessments** - Get all assessments for patient

### ML Prediction Endpoints
16. **POST /patients/{id}/predict** - Trigger ML prediction for all diseases
17. **GET /patients/{id}/predictions/latest** - Get latest risk prediction

### Dashboard & Analytics
18. **GET /dashboard/stats** - Get dashboard analytics (admin only)

### Reports & Recommendations
19. **POST /patients/{id}/report/pdf** - Generate PDF report with section selection
20. **GET /patients/{id}/recommendations** - Get AI-generated lifestyle recommendations

### Consultation Management
21. **POST /consultations** - Book consultation (admin only)
22. **GET /consultations/patient/{id}** - Get patient consultations
23. **POST /consultations/notes** - Add consultation notes

### System Management
24. **GET /health** - Health check endpoint
25. **POST /auth/refresh** - Refresh JWT tokens
26. **POST /auth/logout** - Logout and invalidate tokens

## ML Prediction System

### Model Files
- **Diabetes**: `diabetes_XGBoost.pkl` (XGBoost classifier)
- **Heart**: `heart_best_model.pkl` (XGBoost classifier)
- **Liver**: `liver_LightGBM SMOTE.pkl` (LightGBM with SMOTE)
- **Mental Health**: `mental_health_depressiveness.pkl` (Multiple models for different aspects)

### Prediction Flow
1. Patient completes all 4 assessments (diabetes, liver, heart, mental health)
2. Admin triggers prediction via `POST /patients/{id}/predict`
3. Backend calls `run_prediction()` function for each disease type
4. Each model processes features and returns probability score (0-1)
5. Risk levels are calculated: Low (<0.35), Medium (0.35-0.69), High (≥0.70)
6. New RiskPrediction record is created with all scores and levels
7. Results stored in database for future reference

### Feature Processing
- **Diabetes**: pregnancy, glucose, blood_pressure, skin_thickness, insulin, diabetes_history, age, bmi
- **Heart**: diabetes, hypertension, obesity, smoking, alcohol_consumption, physical_activity, diet_score, cholesterol_level, triglyceride_level, ldl_level, hdl_level, systolic_bp, diastolic_bp, air_pollution_exposure, family_history, stress_level, heart_attack_history, age, gender, bmi
- **Liver**: age, gender, total_bilirubin, direct_bilirubin, alkaline_phosphatase, sgpt_alamine_aminotransferase, sgot_aspartate_aminotransferase, total_protein, albumin, ag_ratio
- **Mental Health**: phq_score, gad_score, depressiveness, suicidal, anxiousness, sleepiness, age, gender

## Database Models

### Core Models
- **User**: Healthcare workers/admins with authentication details
- **Patient**: Patient records with ABHA ID, demographics, and health metrics
- **Assessment Models**: 
  - `DiabetesAssessment`: Glucose, blood pressure, insulin levels
  - `LiverAssessment`: Bilirubin, enzyme markers, protein levels
  - `HeartAssessment`: Cholesterol, lifestyle factors, family history
  - `MentalHealthAssessment`: PHQ-9, GAD-7 scores, mental health indicators
- **RiskPrediction**: ML prediction results with risk levels
- **Consultation**: Appointment booking and scheduling
- **ConsultationNote**: Doctor notes and observations
- **LifestyleRecommendation**: AI-generated lifestyle guidance
- **TokenBlocklist**: JWT token revocation for security

### Computed Fields
- **BMI**: `weight_kg / (height_m)^2` (Patient model)
- **A/G Ratio**: `albumin / (total_protein - albumin)` (LiverAssessment model)
- **Risk Levels**: Calculated from ML model probabilities

### Relationships
- **1:N**: User → Patients (one healthcare worker manages multiple patients)
- **1:N**: Patient → Assessments (one patient has multiple assessments per disease)
- **1:N**: Patient → RiskPredictions (one patient has multiple prediction records)
- **1:N**: Patient → Consultations (one patient can have multiple consultations)
- **1:N**: User → Consultations (one healthcare worker can manage multiple consultations)
- **1:N**: Consultation → ConsultationNotes (one consultation can have multiple notes)

## Ambiguities and Notes

### Multiple Endpoints for Same Function
- **Patient Login**: Only one endpoint exists (`/auth/patient/login`) - no ambiguity
- **Admin Login**: Only one endpoint exists (`/auth/admin/login`) - no ambiguity
- **Patient Details**: Single endpoint `/patients/{id}` serves both admin and patient views with role-based access control

### ML Prediction Patterns
- **Single Prediction Endpoint**: `/patients/{id}/predict` triggers all 4 disease predictions
- **No Individual Disease Prediction**: Cannot predict single disease in isolation
- **Prediction Dependencies**: Requires all 4 assessments to be completed before prediction

### Assessment Creation
- **Separate Endpoints**: Each disease has its own assessment creation endpoint
- **No Bulk Assessment**: Cannot create multiple assessments in single request
- **Assessment History**: 1:N relationship allows multiple assessments per patient per disease

### PDF Generation
- **Single Endpoint**: `/patients/{id}/report/pdf` with sections parameter
- **No Template Selection**: Fixed PDF template, only section selection available
- **No Customization**: Cannot customize PDF layout or styling

### Recommendations
- **AI-Generated**: Uses Gemini API for dynamic recommendations
- **No Manual Recommendations**: Cannot manually add/edit recommendations
- **Category-Based**: Recommendations grouped by diet, exercise, sleep, lifestyle

## Security Considerations

### Role-Based Access Control
- **Admin-Only Endpoints**: Patient creation, assessment creation, prediction triggering, dashboard stats, consultation management
- **Patient-Accessible Endpoints**: Own patient details, own predictions, own recommendations, own PDF reports
- **Shared Endpoints**: Authentication, logout, token refresh, health check

### Data Validation
- **Pydantic Schemas**: All endpoints use Pydantic for request validation
- **Password Complexity**: Enforced for both admin and patient accounts (minimum 8 characters, special characters)
- **ABHA ID Validation**: Strict 14-digit numeric validation
- **Rate Limiting**: Applied to authentication endpoints (10/min login, 5/hour registration)
- **Input Sanitization**: All user inputs are validated and sanitized

### Token Management
- **JWT Blocklisting**: Tokens are revoked on logout and stored in TokenBlocklist
- **Refresh Token Rotation**: New refresh token issued on each refresh
- **Token Expiry**: Short-lived access tokens (15 min) for security
- **Secure Headers**: Authorization header required for protected endpoints

## External Dependencies

### ML Models
- **Scikit-learn/Pandas**: For model loading and prediction
- **Joblib**: For model serialization and loading
- **NumPy**: For numerical operations and array handling
- **XGBoost**: For diabetes and heart disease prediction
- **LightGBM**: For liver disease prediction with SMOTE

### AI Services
- **Google Gemini API**: For lifestyle recommendations generation
- **API Key Required**: GEMINI_API_KEY environment variable
- **Rate Limiting**: Handled by Gemini API service

### PDF Generation
- **FPDF**: For PDF report generation
- **No External Services**: Self-contained PDF generation
- **Section-Based**: Dynamic PDF generation with selectable sections

### Database
- **SQLite**: Default database for development
- **SQLAlchemy**: ORM for database operations
- **Alembic**: Database migrations
- **Production Ready**: Supports PostgreSQL, MySQL for production

## Error Handling Patterns

### Standard Error Responses
- **Validation Errors**: 422 with detailed field errors and validation messages
- **Authentication Errors**: 401 with clear authentication failure messages
- **Authorization Errors**: 403 with role requirements and access denied messages
- **Not Found Errors**: 404 for missing resources with helpful error messages
- **Conflict Errors**: 409 for duplicate data (e.g., ABHA ID already exists)
- **Rate Limit Errors**: 429 with retry-after headers
- **Server Errors**: 500 with generic error messages (detailed logs server-side)

### ML Prediction Errors
- **Missing Assessment**: 400 with specific error message indicating which assessments are missing
- **Model Loading Failure**: Runtime error logged, prediction fails gracefully
- **Feature Processing Error**: ValueError with preprocessing details and expected format
- **Model Compatibility**: Version mismatch errors with model requirements

### Database Errors
- **Connection Errors**: Database connectivity issues with retry mechanisms
- **Constraint Violations**: Foreign key and unique constraint violations
- **Transaction Errors**: Rollback on failed operations
- **Migration Errors**: Schema version mismatches

## Rate Limiting
- **Login Endpoints**: 10 requests per minute (security-focused)
- **Registration**: 5 requests per hour (prevent spam)
- **Patient Listing**: 100 requests per minute
- **Dashboard Stats**: 100 requests per minute
- **Other Endpoints**: No rate limiting applied
- **Implementation**: Flask-Limiter with Redis/SQLite backend
- **Clear Rate Limits**: `python clear_rate_limits.py` utility available

## Database Configuration
- **SQLite**: Default database (development)
- **Environment Support**: DATABASE_URL for production (PostgreSQL, MySQL)
- **Migrations**: Alembic for schema changes and version control
- **Connection Pooling**: Not configured for SQLite (production databases support pooling)
- **Backup Strategy**: Regular database backups recommended
- **Performance**: Indexed on frequently queried fields (ABHA ID, user_id, patient_id)
