# HealthCare App/medml-backend/app/models.py
# HealthCare App/medml-backend/app/models.py
from app.extensions import db, bcrypt
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime # <-- ADDED

class User(db.Model):
    """
    Represents an Admin user (Healthcare Worker) as per MVP.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    
    # Fields from MVP 'Admin' table
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) # Used for login
    password_hash = db.Column(db.String(256), nullable=False)
    designation = db.Column(db.String(100), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    
    # Role-based access
    role = db.Column(db.String(20), nullable=False, default='admin')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # 1:N relationship (Admin -> Patients)
    patients = db.relationship('Patient', back_populates='created_by')
    
    # 1:N relationship (Admin -> Consultations)
    booked_consultations = db.relationship('Consultation', back_populates='booked_by_admin')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "designation": self.designation,
            "contact_number": self.contact_number
        }

class Patient(db.Model):
    """
    Represents a Patient as per MVP.
    """
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    
    # MVP Fields
    full_name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    height_cm = db.Column(db.Float, nullable=False)
    weight_kg = db.Column(db.Float, nullable=False)
    abha_id = db.Column(db.String(14), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False) # For patient login
    state_name = db.Column(db.String(100), nullable=True)
    
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_by = db.relationship('User', back_populates='patients')
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # 1:1 Relationships with Assessments and Predictions
    diabetes_assessment = db.relationship('DiabetesAssessment', back_populates='patient', uselist=False, cascade="all, delete-orphan")
    liver_assessment = db.relationship('LiverAssessment', back_populates='patient', uselist=False, cascade="all, delete-orphan")
    heart_assessment = db.relationship('HeartAssessment', back_populates='patient', uselist=False, cascade="all, delete-orphan")
    mental_health_assessment = db.relationship('MentalHealthAssessment', back_populates='patient', uselist=False, cascade="all, delete-orphan")
    risk_prediction = db.relationship('RiskPrediction', back_populates='patient', uselist=False, cascade="all, delete-orphan")
    
    # 1:N relationship (Patient -> Consultations)
    consultations = db.relationship('Consultation', back_populates='patient')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @hybrid_property
    def bmi(self):
        """ Auto-calculates BMI as required by MVP """
        if self.height_cm and self.weight_kg and self.height_cm > 0:
            height_m = self.height_cm / 100.0
            return round(self.weight_kg / (height_m ** 2), 2)
        return None

    def to_dict(self, include_assessments=False, include_predictions=False, include_consultations=False):
        data = {
            "id": self.id,
            "full_name": self.full_name,
            "age": self.age,
            "gender": self.gender,
            "abha_id": self.abha_id,
            "height_cm": self.height_cm,
            "weight_kg": self.weight_kg,
            "bmi": self.bmi,
            "state_name": self.state_name,
            "created_by_user_id": self.created_by_user_id,
            "created_at": self.created_at.isoformat(),
        }
        if include_assessments:
            data['assessments'] = {
                "diabetes": self.diabetes_assessment.to_dict() if self.diabetes_assessment else None,
                "liver": self.liver_assessment.to_dict() if self.liver_assessment else None,
                "heart": self.heart_assessment.to_dict() if self.heart_assessment else None,
                "mental_health": self.mental_health_assessment.to_dict() if self.mental_health_assessment else None,
            }
        if include_predictions:
            data['risk_prediction'] = self.risk_prediction.to_dict() if self.risk_prediction else None
        if include_consultations:
            data['consultations'] = [c.to_dict() for c in self.consultations]
        return data

# --- Assessment Tables (as per MVP) ---

class BaseAssessment(db.Model):
    """ Abstract base for common assessment fields """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, unique=True) # 1:1
    assessed_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class DiabetesAssessment(BaseAssessment):
    __tablename__ = 'diabetes_assessments'
    patient = db.relationship('Patient', back_populates='diabetes_assessment')
    
    pregnancies = db.Column(db.Integer, nullable=False)
    glucose = db.Column(db.Float, nullable=False)
    blood_pressure = db.Column(db.Float, nullable=False)
    skin_thickness = db.Column(db.Float, nullable=False)
    insulin = db.Column(db.Float, nullable=False)
    diabetes_pedigree_function = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        # Exclude 'id' and 'patient_id' from the dict sent to the model
        return {
            "pregnancies": self.pregnancies,
            "glucose": self.glucose,
            "blood_pressure": self.blood_pressure,
            "skin_thickness": self.skin_thickness,
            "insulin": self.insulin,
            "diabetes_pedigree_function": self.diabetes_pedigree_function,
            "assessed_at": self.assessed_at.isoformat()
        }

class LiverAssessment(BaseAssessment):
    __tablename__ = 'liver_assessments'
    patient = db.relationship('Patient', back_populates='liver_assessment')
    
    total_bilirubin = db.Column(db.Float, nullable=False)
    direct_bilirubin = db.Column(db.Float, nullable=False)
    alkaline_phosphotase = db.Column(db.Float, nullable=False)
    alamine_aminotransferase = db.Column(db.Float, nullable=False)
    aspartate_aminotransferase = db.Column(db.Float, nullable=False)
    total_proteins = db.Column(db.Float, nullable=False)
    albumin = db.Column(db.Float, nullable=False)
    globulin = db.Column(db.Float, nullable=False)
    
    @hybrid_property
    def ag_ratio(self):
        """ Auto-calculates A/G Ratio as required """
        if self.albumin and self.globulin and self.globulin > 0:
            return round(self.albumin / self.globulin, 2)
        return None

    def to_dict(self):
        # Exclude 'id' and 'patient_id'
        data = {
            "total_bilirubin": self.total_bilirubin,
            "direct_bilirubin": self.direct_bilirubin,
            "alkaline_phosphotase": self.alkaline_phosphotase,
            "alamine_aminotransferase": self.alamine_aminotransferase,
            "aspartate_aminotransferase": self.aspartate_aminotransferase,
            "total_proteins": self.total_proteins,
            "albumin": self.albumin,
            "globulin": self.globulin,
            "ag_ratio": self.ag_ratio, # Add the computed ratio
            "assessed_at": self.assessed_at.isoformat()
        }
        return data

class HeartAssessment(BaseAssessment):
    __tablename__ = 'heart_assessments'
    patient = db.relationship('Patient', back_populates='heart_assessment')
    
    chest_pain_type = db.Column(db.Integer, nullable=False)
    resting_blood_pressure = db.Column(db.Float, nullable=False)
    cholesterol = db.Column(db.Float, nullable=False)
    fasting_blood_sugar = db.Column(db.Integer, nullable=False)
    resting_ecg = db.Column(db.Integer, nullable=False)
    max_heart_rate = db.Column(db.Float, nullable=False)
    exercise_angina = db.Column(db.Integer, nullable=False)
    st_depression = db.Column(db.Float, nullable=False)
    st_slope = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        # Exclude 'id' and 'patient_id'
        return {
            "chest_pain_type": self.chest_pain_type,
            "resting_blood_pressure": self.resting_blood_pressure,
            "cholesterol": self.cholesterol,
            "fasting_blood_sugar": self.fasting_blood_sugar,
            "resting_ecg": self.resting_ecg,
            "max_heart_rate": self.max_heart_rate,
            "exercise_angina": self.exercise_angina,
            "st_depression": self.st_depression,
            "st_slope": self.st_slope,
            "assessed_at": self.assessed_at.isoformat()
        }

class MentalHealthAssessment(BaseAssessment):
    __tablename__ = 'mental_health_assessments'
    patient = db.relationship('Patient', back_populates='mental_health_assessment')
    
    phq_score = db.Column(db.Integer, nullable=False)
    gad_score = db.Column(db.Integer, nullable=False)
    sleep_quality = db.Column(db.Integer, nullable=False)
    mood_factors = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        # Exclude 'id' and 'patient_id'
        return {
            "phq_score": self.phq_score,
            "gad_score": self.gad_score,
            "sleep_quality": self.sleep_quality,
            "mood_factors": self.mood_factors,
            "assessed_at": self.assessed_at.isoformat()
        }

# --- Prediction and Recommendation Tables (as per MVP) ---

class RiskPrediction(db.Model):
    __tablename__ = 'risk_predictions'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, unique=True) # 1:1
    patient = db.relationship('Patient', back_populates='risk_prediction')
    
    diabetes_score = db.Column(db.Float, nullable=True)
    diabetes_level = db.Column(db.String(20), nullable=True)
    liver_score = db.Column(db.Float, nullable=True)
    liver_level = db.Column(db.String(20), nullable=True)
    heart_score = db.Column(db.Float, nullable=True)
    heart_level = db.Column(db.String(20), nullable=True)
    mental_health_score = db.Column(db.Float, nullable=True)
    mental_health_level = db.Column(db.String(20), nullable=True)
    
    model_version = db.Column(db.String(50), nullable=True, default='1.0')
    predicted_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "diabetes_score": self.diabetes_score,
            "diabetes_level": self.diabetes_level,
            "liver_score": self.liver_score,
            "liver_level": self.liver_level,
            "heart_score": self.heart_score,
            "heart_level": self.heart_level,
            "mental_health_score": self.mental_health_score,
            "mental_health_level": self.mental_health_level,
            "model_version": self.model_version,
            "predicted_at": self.predicted_at.isoformat()
        }

class LifestyleRecommendation(db.Model):
    """ Stores static recommendation templates """
    __tablename__ = 'lifestyle_recommendations'
    id = db.Column(db.Integer, primary_key=True)
    disease_type = db.Column(db.String(50), nullable=False) # 'diabetes', 'liver', 'heart', 'mental_health', 'general'
    risk_level = db.Column(db.String(20), nullable=False) # 'Low', 'Medium', 'High'
    category = db.Column(db.String(50), nullable=False, default='general') # 'Diet', 'Exercise', 'Sleep', 'Lifestyle'
    recommendation_text = db.Column(db.Text, nullable=False)
    
    __table_args__ = (db.UniqueConstraint('disease_type', 'risk_level', 'category', 'recommendation_text'),)

# --- NEW: Consultation Table ---
class Consultation(db.Model):
    """
    Represents a (dummy) consultation booking as per MVP.
    """
    __tablename__ = 'consultations'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    consultation_type = db.Column(db.String(50), nullable=False) # 'Teleconsultation', 'In-Person'
    consultation_datetime = db.Column(db.DateTime, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='Booked') # e.g., 'Booked', 'Completed'
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    patient = db.relationship('Patient', back_populates='consultations')
    booked_by_admin = db.relationship('User', back_populates='booked_consultations')

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "admin_id": self.admin_id,
            "consultation_type": self.consultation_type,
            "consultation_datetime": self.consultation_datetime.isoformat(),
            "notes": self.notes,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }