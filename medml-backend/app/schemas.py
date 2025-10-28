# HealthCare App/medml-backend/app/schemas.py
from pydantic import BaseModel, EmailStr, constr, conint, confloat
from typing import List

# --- FIX: Define Strong Password Regex ---
# Min 8 chars, 1 uppercase, 1 lowercase, 1 number, 1 special char
PASSWORD_REGEX = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,}$"
PASSWORD_ERROR_MSG = "Password must be at least 8 characters long and contain one uppercase letter, one lowercase letter, one number, and one special character."

# --- Auth Schemas ---

class UserRegisterSchema(BaseModel):
    """ Validates admin registration data """
    name: constr(min_length=2, max_length=150)
    email: EmailStr
    password: constr(pattern=PASSWORD_REGEX, min_length=8)
    designation: constr(max_length=100) | None = None
    contact_number: constr(max_length=20) | None = None
    role: str = 'admin'

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "name": "Dr. Jane Doe",
                    "email": "jane.doe@med.com",
                    "password": "Password123!",
                    "designation": "Cardiologist",
                    "contact_number": "555-1234"
                }
            ]
        }


class UserLoginSchema(BaseModel):
    """ Validates admin login """
    email: EmailStr
    password: str

class PatientLoginSchema(BaseModel):
    """ Validates patient login as per MVP """
    abha_id: constr(pattern=r'^\d{14}$') # Strict 14-digit ABHA ID
    password: str

# --- Patient Schema ---

class PatientCreateSchema(BaseModel):
    """ Validates data for creating a new patient """
    full_name: constr(min_length=2, max_length=150)
    age: conint(gt=0, lt=120)
    gender: constr(min_length=1, max_length=20)
    height_cm: confloat(gt=0)
    weight_kg: confloat(gt=0)
    abha_id: constr(pattern=r'^\d{14}$') # Strict 14-digit validation
    state_name: constr(max_length=100) | None = None
    password: constr(pattern=PASSWORD_REGEX, min_length=8) # Admin sets initial patient password

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "full_name": "John Patient",
                    "age": 45,
                    "gender": "Male",
                    "height_cm": 175,
                    "weight_kg": 80,
                    "abha_id": "12345678901234",
                    "state_name": "Karnataka",
                    "password": "Password123!"
                }
            ]
        }

# --- Assessment Schemas (as per MVP) ---
# These schemas validate the *input* for the 4 assessment types.

class DiabetesAssessmentSchema(BaseModel):
    pregnancies: int
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    diabetes_pedigree_function: float

class LiverAssessmentSchema(BaseModel):
    total_bilirubin: float
    direct_bilirubin: float
    alkaline_phosphotase: float
    alamine_aminotransferase: float
    aspartate_aminotransferase: float
    total_proteins: float
    albumin: float
    globulin: float # MVP states A/G ratio is computed, so globulin is needed

class HeartAssessmentSchema(BaseModel):
    chest_pain_type: int
    resting_blood_pressure: float
    cholesterol: float
    fasting_blood_sugar: int # 1 or 0
    resting_ecg: int
    max_heart_rate: float
    exercise_angina: int # 1 or 0
    st_depression: float
    st_slope: int

class MentalHealthAssessmentSchema(BaseModel):
    # As per MVP, using PHQ-9 and GAD-7 factors
    phq_score: conint(ge=0, le=27) # PHQ-9 total score
    gad_score: conint(ge=0, le=21) # GAD-7 total score
    sleep_quality: conint(ge=1, le=5) # Example: 1-5 scale
    mood_factors: constr(max_length=255) | None = None