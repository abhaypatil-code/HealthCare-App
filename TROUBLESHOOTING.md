# Troubleshooting Guide

This comprehensive guide helps you resolve common issues with the Healthcare Management System. Follow the solutions in order of complexity, starting with quick fixes.

## 🚨 Quick Fixes

### Most Common Solutions
```bash
# Clear rate limits (if getting 429 errors)
cd medml-backend
python clear_rate_limits.py

# Recreate database (if corrupted)
python create_admin.py

# Check system status
python test_system.py

# Restart both services
# Stop both backend and frontend, then restart
```

## 🚫 Rate Limiting Issues

### Problem: "429 TOO MANY REQUESTS" errors
**Symptoms:**
- "Error fetching patients: 429 Client Error: TOO MANY REQUESTS"
- API calls being blocked after a few requests
- Frontend unable to load data
- Login attempts blocked

**Solutions:**
```bash
# Clear rate limit cache
cd medml-backend
python clear_rate_limits.py

# Or restart the backend server
# The rate limits are configured to be more permissive in development
```

**Configuration:**
- Default limits: 1000 per day, 200 per hour, 50 per minute
- Patient listing: 100 per minute
- Dashboard stats: 100 per minute
- Login endpoints: 10 per minute (more restrictive for security)
- Registration: 5 requests per hour

## 🔧 Backend Server Issues

### Problem: Backend won't start
**Symptoms:**
- Error messages when running `python run.py`
- Port 5000 already in use
- Database connection errors
- Module import errors

**Solutions:**
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill process using port 5000 (Windows)
taskkill /PID <PID_NUMBER> /F

# Or use a different port
set FLASK_RUN_PORT=5001
python run.py

# Check Python installation
python --version

# Install missing dependencies
pip install -r requirements.txt
```

### Problem: Database errors
**Symptoms:**
- "Database is locked" errors
- "Table doesn't exist" errors
- Permission denied errors
- SQLite errors

**Solutions:**
```bash
# Recreate database
cd medml-backend
python create_admin.py

# Check database file permissions
ls -la app/medml.db

# Delete and recreate if corrupted
rm app/medml.db
python create_admin.py

# Check SQLite installation
python -c "import sqlite3; print('SQLite OK')"
```

#### Problem: ML models not loading
**Symptoms:**
- "Model not found" errors
- Prediction failures
- Missing model files
- Model loading errors

**Solutions:**
```bash
# Check models directory
ls -la medml-backend/models_store/

# Verify model files exist
# Required files:
# - diabetes_XGBoost.pkl
# - heart_best_model.pkl
# - liver_LightGBM SMOTE.pkl
# - mental_health_depressiveness.pkl

# Test model loading
cd medml-backend
python -c "from app.services import load_models; from app import create_app; app = create_app(); load_models(app)"

# Verify model compatibility
python -c "import joblib; model = joblib.load('models_store/diabetes_XGBoost.pkl'); print(model)"
```

### 2. Frontend Issues

#### Problem: Frontend won't load
**Symptoms:**
- "Cannot connect to backend" errors
- Blank page
- Streamlit errors
- Port 8501 issues

**Solutions:**
```bash
# Check if backend is running
curl http://127.0.0.1:5000/api/v1/auth/me

# Restart frontend
cd medml-frontend
streamlit run app.py

# Check Streamlit installation
pip install streamlit --upgrade

# Install frontend dependencies
pip install -r requirements.txt

# Check port availability
netstat -ano | findstr :8501
```

#### Problem: Login issues
**Symptoms:**
- "Invalid credentials" errors
- Authentication failures
- Token errors

**Solutions:**
```bash
# Check admin user exists
cd medml-backend
python -c "from app import create_app; from app.models import User; app = create_app(); app.app_context().push(); print(User.query.all())"

# Recreate admin user
python create_admin.py
```

### 3. Database Issues

#### Problem: Database corruption
**Symptoms:**
- "Database is locked" errors
- Inconsistent data
- Query failures

**Solutions:**
```bash
# Backup existing data
cp medml-backend/app/medml.db medml-backend/app/medml.db.backup

# Recreate database
rm medml-backend/app/medml.db
cd medml-backend
python create_admin.py
```

#### Problem: Migration issues
**Symptoms:**
- "Table already exists" errors
- Schema mismatch errors
- Migration failures

**Solutions:**
```bash
# Reset migrations
cd medml-backend
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 4. ML Model Issues

#### Problem: Model prediction errors
**Symptoms:**
- "Model not loaded" errors
- Prediction failures
- Feature mismatch errors

**Solutions:**
```bash
# Check model files
ls -la medml-backend/models_store/

# Test model loading
cd medml-backend
python -c "from app.services import load_models; from app import create_app; app = create_app(); load_models(app)"

# Verify model compatibility
python -c "import joblib; model = joblib.load('models_store/diabetes_XGBoost.pkl'); print(model)"
```

#### Problem: Feature mismatch
**Symptoms:**
- "Feature not found" errors
- Prediction errors
- Data type errors

**Solutions:**
```bash
# Check feature requirements in services.py
# Verify input data format matches model expectations
# Check data preprocessing steps
```

### 5. API Issues

#### Problem: CORS errors
**Symptoms:**
- "CORS policy" errors
- Cross-origin request blocked
- API call failures

**Solutions:**
```bash
# Check CORS configuration in app/__init__.py
# Add frontend URL to CORS_ORIGINS
export CORS_ORIGINS="http://localhost:8501,http://127.0.0.1:8501"
```

#### Problem: Rate limiting
**Symptoms:**
- "Rate limit exceeded" errors
- Too many requests errors
- API throttling

**Solutions:**
```bash
# Check rate limiting configuration
# Adjust limits in app/extensions.py
# Clear rate limit cache if needed
```

### 6. Authentication Issues

#### Problem: JWT token errors
**Symptoms:**
- "Invalid token" errors
- Token expiration errors
- Authentication failures

**Solutions:**
```bash
# Check JWT configuration
# Verify SECRET_KEY and JWT_SECRET_KEY
# Clear token blacklist if needed
```

#### Problem: Password issues
**Symptoms:**
- "Invalid password" errors
- Password hash errors
- Login failures

**Solutions:**
```bash
# Reset admin password
cd medml-backend
python -c "from app import create_app; from app.models import User; from flask_bcrypt import Bcrypt; app = create_app(); app.app_context().push(); user = User.query.filter_by(email='admin@healthcare.com').first(); bcrypt = Bcrypt(); user.password_hash = bcrypt.generate_password_hash('Admin123!').decode('utf-8'); from app.extensions import db; db.session.commit()"
```

## 🔧 System Diagnostics

### Run System Tests
```bash
python test_system.py
```

### Check System Status
```bash
# Backend status
curl http://127.0.0.1:5000/api/v1/auth/me

# Frontend status
curl http://localhost:8501

# Database status
cd medml-backend
python -c "from app import create_app; from app.models import db; app = create_app(); app.app_context().push(); db.session.execute('SELECT 1')"
```

### Check Logs
```bash
# Backend logs
tail -f medml-backend/logs/medml.log

# Frontend logs (check console output)
# Database logs (check SQLite logs)
```

## 🛠️ Advanced Troubleshooting

### Performance Issues

#### Problem: Slow response times
**Solutions:**
- Check database query performance
- Optimize ML model loading
- Increase server resources
- Check network latency

#### Problem: Memory issues
**Solutions:**
- Monitor memory usage
- Optimize ML model memory usage
- Check for memory leaks
- Increase system memory

### Deployment Issues

#### Problem: Production deployment
**Solutions:**
- Set production environment variables
- Configure production database
- Set up proper logging
- Configure reverse proxy

#### Problem: SSL/HTTPS issues
**Solutions:**
- Configure SSL certificates
- Update CORS settings
- Check certificate validity
- Configure secure cookies

## 📞 Getting Help

### Before Asking for Help
1. Run the system tests: `python test_system.py`
2. Check the logs for error messages
3. Verify all dependencies are installed
4. Check system requirements

### Information to Provide
- Operating system and version
- Python version
- Error messages and logs
- Steps to reproduce the issue
- System configuration

### Common Solutions
1. **Restart the system**: Stop both backend and frontend, then restart
2. **Clear cache**: Clear browser cache and restart
3. **Reinstall dependencies**: `pip install -r requirements.txt --force-reinstall`
4. **Recreate database**: Run `python create_admin.py`
5. **Check permissions**: Ensure proper file permissions

## 🔄 Recovery Procedures

### Complete System Reset
```bash
# Stop all services
# Delete database
rm medml-backend/app/medml.db

# Reinstall dependencies
cd medml-backend && pip install -r requirements.txt --force-reinstall
cd ../medml-frontend && pip install -r requirements.txt --force-reinstall

# Recreate database
cd ../medml-backend && python create_admin.py

# Test system
cd .. && python test_system.py
```

### Data Recovery
```bash
# Restore from backup
cp medml-backend/app/medml.db.backup medml-backend/app/medml.db

# Or restore specific tables
sqlite3 medml-backend/app/medml.db < backup.sql
```

---

**Remember**: Always backup your data before making changes!