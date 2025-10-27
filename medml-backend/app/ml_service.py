# HealthCare App/medml-backend/app/ml_service.py
import os
import joblib
import pandas as pd
from flask import current_app
from app.models import db, Patient, RiskPrediction

# Global dictionary to hold the loaded models
models = {}

def load_models(app):
    """
    Load all ML models from 'models_store' into memory.
    This is called once on application startup.
    """
    global models
    model_path = os.path.join(app.config['BASE_DIR'], 'models_store')
    
    try:
        models['diabetes'] = joblib.load(os.path.join(model_path, 'diabetes_XGBoost.pkl'))
        models['liver'] = joblib.load(os.path.join(model_path, 'liver_LightGBM SMOTE.pkl'))
        
        # Heart model has a separate preprocessor and model
        models['heart_preprocessor'] = joblib.load(os.path.join(model_path, 'heart_preprocessor.pkl'))
        models['heart_model'] = joblib.load(os.path.join(model_path, 'heart_best_model.pkl'))
        
        # Mental Health models
        models['mental_health_depressiveness'] = joblib.load(os.path.join(model_path, 'mental_health_depressiveness.pkl'))
        models['mental_health_anxiousness'] = joblib.load(os.path.join(model_path, 'mental_health_anxiousness.pkl'))
        models['mental_health_sleepiness'] = joblib.load(os.path.join(model_path, 'mental_health_sleepiness.pkl'))
        
        app.logger.info("All ML models loaded successfully.")
        
    except FileNotFoundError as e:
        app.logger.error(f"Model file not found: {e}. Predictions will fail.")
    except Exception as e:
        app.logger.error(f"Error loading models: {e}")

def _categorize_risk(score):
    """
    Categorizes a risk score (0-1) into Low, Medium, High
    as per the MVP's example thresholds.
    """
    if score <= 0.33:
        return 'Low'
    elif score <= 0.66:
        return 'Medium'
    else:
        return 'High'

def _predict_diabetes(assessment, patient):
    """
    Prepares data and predicts diabetes risk.
    MVP: Uses glucose, BP, insulin, age, BMI.
    """
    try:
        # These column names are based on standard PIMA dataset training
        features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                    'Insulin', 'DiabetesPedigreeFunction', 'Age', 'BMI']
        
        data = {
            'Pregnancies': [assessment.pregnancies],
            'Glucose': [assessment.glucose],
            'BloodPressure': [assessment.blood_pressure],
            'SkinThickness': [assessment.skin_thickness],
            'Insulin': [assessment.insulin],
            'DiabetesPedigreeFunction': [assessment.diabetes_pedigree_function],
            'Age': [patient.age],
            'BMI': [patient.bmi]
        }
        
        df = pd.DataFrame(data, columns=features)
        score = models['diabetes'].predict_proba(df)[0][1] # Probability of class 1
        return score, _categorize_risk(score)
    
    except Exception as e:
        current_app.logger.error(f"Diabetes prediction failed: {e}")
        return None, None

def _predict_liver(assessment, patient):
    """
    Prepares data and predicts liver risk.
    MVP: Bilirubin, enzymes, proteins, BMI, age, gender.
    """
    try:
        # These column names are based on standard Indian Liver Patient Dataset
        features = ['Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 
                    'Alkaline_Phosphotase', 'Alamine_Aminotransferase', 
                    'Aspartate_Aminotransferase', 'Total_Protiens', 'Albumin', 
                    'Albumin_and_Globulin_Ratio']
        
        gender_numeric = 1 if patient.gender.lower() == 'male' else 0
        
        data = {
            'Age': [patient.age],
            'Gender': [gender_numeric],
            'Total_Bilirubin': [assessment.total_bilirubin],
            'Direct_Bilirubin': [assessment.direct_bilirubin],
            'Alkaline_Phosphotase': [assessment.alkaline_phosphotase],
            'Alamine_Aminotransferase': [assessment.alamine_aminotransferase],
            'Aspartate_Aminotransferase': [assessment.aspartate_aminotransferase],
            'Total_Protiens': [assessment.total_proteins],
            'Albumin': [assessment.albumin],
            'Albumin_and_Globulin_Ratio': [assessment.ag_ratio]
        }
        
        df = pd.DataFrame(data, columns=features)
        score = models['liver'].predict_proba(df)[0][1]
        return score, _categorize_risk(score)
        
    except Exception as e:
        current_app.logger.error(f"Liver prediction failed: {e}")
        return None, None

def _predict_heart(assessment, patient):
    """
    Prepares data and predicts heart risk using preprocessor.
    MVP: Lifestyle + lipid + blood pressure + demographic data.
    """
    try:
        # Features based on the heart_preprocessor.pkl (UCI Heart dataset)
        # Note: 'sex', 'cp', 'fbs', 'restecg', 'exang', 'slope' are categorical
        raw_features = {
            'age': [patient.age],
            'sex': [1 if patient.gender.lower() == 'male' else 0],
            'cp': [assessment.chest_pain_type],
            'trestbps': [assessment.resting_blood_pressure],
            'chol': [assessment.cholesterol],
            'fbs': [assessment.fasting_blood_sugar],
            'restecg': [assessment.resting_ecg],
            'thalach': [assessment.max_heart_rate],
            'exang': [assessment.exercise_angina],
            'oldpeak': [assessment.st_depression],
            'slope': [assessment.st_slope],
            'bmi': [patient.bmi]
        }
        
        df = pd.DataFrame(raw_features)
        
        # Apply the preprocessor
        processed_df = models['heart_preprocessor'].transform(df)
        
        # Predict with the main model
        score = models['heart_model'].predict_proba(processed_df)[0][1]
        return score, _categorize_risk(score)

    except Exception as e:
        current_app.logger.error(f"Heart prediction failed: {e}")
        return None, None

def _predict_mental_health(assessment):
    """
    Prepares data and predicts mental health risk.
    MVP: Averages scores from PHQ-9, GAD-7, and sleep models.
    """
    try:
        # 1. Depressiveness
        dep_df = pd.DataFrame({'PHQ-9': [assessment.phq_score]})
        dep_score = models['mental_health_depressiveness'].predict_proba(dep_df)[0][1]
        
        # 2. Anxiousness
        anx_df = pd.DataFrame({'GAD-7': [assessment.gad_score]})
        anx_score = models['mental_health_anxiousness'].predict_proba(anx_df)[0][1]
        
        # 3. Sleepiness
        slp_df = pd.DataFrame({'Sleep Quality': [assessment.sleep_quality]})
        slp_score = models['mental_health_sleepiness'].predict_proba(slp_df)[0][1]
        
        # Combine scores (using average as a simple metric)
        avg_score = (dep_score + anx_score + slp_score) / 3.0
        return avg_score, _categorize_risk(avg_score)

    except Exception as e:
        current_app.logger.error(f"Mental Health prediction failed: {e}")
        return None, None


def trigger_all_predictions(patient_id, model_version="v1.0-mvp"):
    """
    Main service function called by the API.
    Triggers all 4 predictions and saves them to the database.
    Fulfills MVP: "Admin completes all assessments -> 'Finish Survey' triggers ML prediction"
    """
    patient = Patient.query.get(patient_id)
    if not patient:
        return None, "Patient not found"

    # MVP Check: Ensure all 4 assessments are completed
    assessments = [
        patient.diabetes_assessment,
        patient.liver_assessment,
        patient.heart_assessment,
        patient.mental_health_assessment
    ]
    if not all(assessments):
        return None, "All 4 assessments must be completed before running predictions."
    
    # Run all predictions
    d_score, d_level = _predict_diabetes(patient.diabetes_assessment, patient)
    l_score, l_level = _predict_liver(patient.liver_assessment, patient)
    h_score, h_level = _predict_heart(patient.heart_assessment, patient)
    mh_score, mh_level = _predict_mental_health(patient.mental_health_assessment)

    # Save results to the database
    prediction = RiskPrediction.query.filter_by(patient_id=patient_id).first()
    if not prediction:
        prediction = RiskPrediction(patient_id=patient_id)
        db.session.add(prediction)
    
    prediction.diabetes_score = d_score
    prediction.diabetes_level = d_level
    prediction.liver_score = l_score
    prediction.liver_level = l_level
    prediction.heart_score = h_score
    prediction.heart_level = h_level
    prediction.mental_health_score = mh_score
    prediction.mental_health_level = mh_level
    prediction.model_version = model_version

    try:
        db.session.commit()
        current_app.logger.info(f"Predictions successfully generated for patient {patient_id}")
        return prediction, None
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error saving predictions for patient {patient_id}: {e}")
        return None, "Database error while saving predictions."