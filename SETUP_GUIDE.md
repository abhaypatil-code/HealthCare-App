# Healthcare Diagnostic Dashboard MVP - Setup Guide

## Overview
This is a comprehensive MVP for a healthcare diagnostic dashboard targeting rural healthcare workers and corporate wellness programs. The system provides early disease detection and preventive care with machine learning integration.

## Features Implemented

### ✅ User Authentication & Access Control
- Patient login using 14-digit ABHA ID and password
- Admin login for healthcare workers with role-based access
- Secure JWT token management with refresh tokens
- Password hashing and validation

### ✅ Patient Dashboard
- Left sidebar navigation: Overview, Diabetes, Liver, Heart, Mental Health
- Overview tab with BMI, height, weight, disease risk table (color-coded)
- Healthcare worker info, static appointments, lifestyle recommendations
- Profile & Reports access
- PDF download and share functionality

### ✅ Disease-Specific Tabs
- Risk score display and contributing factors
- Next recommended actions for each disease
- Guidance for low, medium, and high risk levels

### ✅ Admin Dashboard
- Welcome header with 'Add New User' and 'View Registered Patients' buttons
- Analytics dashboard: Today's registrations and risk assessment metrics
- Add New User workflow with health assessment forms
- View Registered Patients with filtering and patient management
- Patient detail view with assessment forms

### ✅ Backend API
- RESTful API for frontend-backend communication
- Authentication endpoints (patient and admin)
- Patient management endpoints (create, update, retrieve, list)
- Health assessment endpoints for all 4 diseases
- Machine learning integration for risk prediction
- Lifestyle recommendation endpoints
- Analytics and PDF generation endpoints

### ✅ Database Models
- Patient, Admin, Assessment tables for all 4 diseases
- RiskPrediction and LifestyleRecommendation tables
- One-to-many relationships properly implemented
- Audit logging and token blocklist

### ✅ Security Features
- JWT tokens with refresh token rotation
- Password hashing with bcrypt
- Role-based access control
- Rate limiting on sensitive endpoints
- CORS configuration
- Input validation with Pydantic

## Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Git

## Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd medml-backend