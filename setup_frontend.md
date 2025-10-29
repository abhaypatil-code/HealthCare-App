# Streamlit Frontend Setup Guide

## Prerequisites

### System Requirements
- Python 3.8 or higher
- pip package manager
- Git (for cloning repository)

### Backend Requirements
- Backend server running on `http://127.0.0.1:5000`
- Database properly initialized
- ML model files present in `models_store/` directory
- Environment variables configured

## Installation Steps

### 1. Clone Repository
```bash
git clone <repository-url>
cd HealthCare-App
```

### 2. Install Python Dependencies
```bash
cd medml-frontend
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the `medml-frontend` directory:
```env
# Backend Configuration
BACKEND_URL=http://127.0.0.1:5000/api/v1

# Optional: Custom configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### 4. Verify Backend Connectivity
Ensure the backend server is running:
```bash
cd ../medml-backend
python run.py
```

The backend should start on `http://127.0.0.1:5000`

### 5. Start Streamlit Frontend
```bash
cd ../medml-frontend
streamlit run app.py
```

The frontend will start on `http://127.0.0.1:8501`

## Configuration Details

### Backend URL Configuration
The frontend is configured to connect to the backend at:
- **Base URL**: `http://127.0.0.1:5000/api/v1`
- **Authentication**: JWT token-based
- **API Version**: v1

### Default Credentials

#### Admin Account
- **Username**: `admin`
- **Email**: `admin@healthcare.com`
- **Password**: `Admin123!`

#### Test Patient Account
- **ABHA ID**: `12345678901234`
- **Password**: `12345678901234@Default123`

## Running Tests

### Automated Tests
```bash
cd tests
python streamlit_frontend_checks.py
```

### Manual Tests
Follow the test cases in `run_manual_checks.md` for comprehensive manual testing.

## Troubleshooting

### Common Issues

#### 1. Backend Connection Failed
**Error**: "Cannot connect to backend server"
**Solution**: 
- Ensure backend server is running on port 5000
- Check if backend URL is correct
- Verify firewall settings

#### 2. Authentication Failed
**Error**: "Login Failed: Invalid credentials"
**Solution**:
- Verify admin credentials are correct
- Check if admin account exists in database
- Ensure JWT configuration is proper

#### 3. ML Prediction Failed
**Error**: "Failed to trigger prediction"
**Solution**:
- Check if ML model files exist in `models_store/`
- Verify all assessments are completed
- Check backend logs for model loading errors

#### 4. PDF Generation Failed
**Error**: "Error generating PDF"
**Solution**:
- Ensure FPDF is installed in backend
- Check if patient has prediction data
- Verify PDF generation endpoint is working

#### 5. Recommendations Not Loading
**Error**: "No recommendations available"
**Solution**:
- Check if GEMINI_API_KEY is configured
- Verify Gemini API is accessible
- Check backend logs for API errors

### Debug Mode

#### Enable Debug Logging
Add to `.env` file:
```env
STREAMLIT_LOGGER_LEVEL=debug
```

#### Backend Debug Mode
Start backend with debug mode:
```bash
cd medml-backend
export FLASK_ENV=development
python run.py
```

## Development Setup

### Code Structure
```
medml-frontend/
├── app.py                 # Main Streamlit application
├── api_client.py         # Backend API client
├── utils.py              # Utility functions
├── pages/
│   ├── 1_Patient_Dashboard.py
│   └── 2_Admin_Dashboard.py
├── requirements.txt       # Python dependencies
└── .env                  # Environment configuration
```

### Key Components

#### 1. `app.py`
- Main application entry point
- Login interface for both admin and patient
- Session state management
- Backend connectivity checks

#### 2. `api_client.py`
- Backend API communication
- Authentication handling
- Error handling and user feedback
- Request/response processing

#### 3. `utils.py`
- UI utility functions
- Risk level color coding
- Session management
- Form validation helpers

#### 4. `pages/`
- Role-specific dashboard pages
- Patient dashboard with assessment history
- Admin dashboard with patient management

## Production Deployment

### 1. Environment Variables
Set production environment variables:
```env
FLASK_ENV=production
SECRET_KEY=<strong-secret-key>
JWT_SECRET_KEY=<jwt-secret-key>
GEMINI_API_KEY=<gemini-api-key>
DATABASE_URL=<production-database-url>
```

### 2. Security Configuration
- Use strong secret keys
- Enable HTTPS in production
- Configure proper CORS settings
- Set up rate limiting

### 3. Performance Optimization
- Enable Streamlit caching
- Optimize database queries
- Use CDN for static assets
- Configure proper logging

### 4. Monitoring
- Set up application monitoring
- Configure error tracking
- Monitor API response times
- Track user activity

## API Integration Details

### Authentication Flow
1. User submits login credentials
2. Frontend sends request to `/auth/{role}/login`
3. Backend returns JWT tokens
4. Frontend stores tokens in session state
5. All subsequent requests include `Authorization: Bearer <token>`

### Data Flow
1. **Patient Creation**: Admin creates patient → Backend stores in database
2. **Assessment**: Admin completes assessments → Backend stores assessment data
3. **Prediction**: Admin triggers prediction → Backend runs ML models → Results stored
4. **Display**: Frontend fetches data → Displays in user-friendly format

### Error Handling
- Network errors: Show connectivity messages
- Authentication errors: Redirect to login
- Validation errors: Show field-specific messages
- Server errors: Show generic error with retry options

## Support and Maintenance

### Log Files
- Streamlit logs: Check terminal output
- Backend logs: Check backend console
- Browser console: Check for JavaScript errors

### Updates
- Keep dependencies updated
- Monitor for security patches
- Test after any backend changes
- Verify ML model compatibility

### Backup
- Regular database backups
- Configuration file backups
- ML model file backups
- User data backups

## Contact Information

For technical support or questions:
- Check the troubleshooting section above
- Review the manual test cases
- Run automated tests for validation
- Check backend logs for detailed errors

## Version Information

- **Frontend Version**: 1.0.0
- **Backend API Version**: v1
- **Streamlit Version**: Latest stable
- **Python Version**: 3.8+
