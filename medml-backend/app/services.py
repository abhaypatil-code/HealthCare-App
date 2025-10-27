# HealthCare App/medml-backend/app/services.py
import joblib
import pandas as pd
import numpy as np
import os
from typing import Dict, Any
from flask import current_app

# --- Model Loading ---
# FIX: Corrected path. __file__ is 'app/services.py', so we go 'app/../models_store'
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models_store')

# Global dictionary to hold models and preprocessors
models = {
    'diabetes': None,
    'heart': None,
    'liver': None,
    'mental_health': None
}
preprocessors = {
    'heart': None
}

def load_model(app: Any, key: str, filename: str):
    """Loads a .pkl model from the models_store directory into a global dict."""
    try:
        path = os.path.join(MODEL_DIR, filename)
        if not os.path.exists(path):
            app.logger.warning(f"Model file not found at {path}. Predictions for '{key}' will fail.")
            return None
        return joblib.load(path)
    except Exception as e:
        app.logger.error(f"Error loading model {filename}: {e}")
        return None

def load_models(app: Any):
    """Loads all models and preprocessors at application startup."""
    with app.app_context():
        app.logger.info(f"Loading models from: {MODEL_DIR}")
        
        models['diabetes'] = load_model(app, 'diabetes', 'diabetes_XGBoost.pkl')
        models['heart'] = load_model(app, 'heart', 'heart_best_model.pkl')
        models['liver'] = load_model(app, 'liver', 'liver_LightGBM SMOTE.pkl')
        # MVP specifies PHQ-9 (depression), so 'depressiveness' is the correct model
        models['mental_health'] = load_model(app, 'mental_health', 'mental_health_depressiveness.pkl')
        
        # Load the separate preprocessor for the heart model
        preprocessors['heart'] = load_model(app, 'heart_preprocessor', 'heart_preprocessor.pkl')
        
        app.logger.info("Model loading complete.")

# --- Preprocessing & Prediction Logic ---

def predict_diabetes(data: Dict[str, Any]) -> Dict[str, Any]:
    model = models.get('diabetes')
    if model is None:
        current_app.logger.error("Diabetes model is not loaded.")
        raise RuntimeError("Diabetes model is not loaded.")
        
    try:
        # The model .pkl is assumed to be a pipeline (scaler + model)
        # Create DataFrame in the correct order expected by the model
        # This order is based on the DiabetesAssessmentSchema
        feature_order = [
            'pregnancies', 'glucose', 'blood_pressure', 
            'skin_thickness', 'insulin', 'diabetes_pedigree_function'
        ]
        # We also need 'age' and 'bmi' which are on the Patient model
        # The *caller* (api/predict.py) must add these.
        
        # Re-check: The schema only has 6 features. But the model notebook
        # likely used Age and BMI. The DiabetesAssessment model only has 6.
        # This is a schema/model mismatch.
        # For now, we'll assume the model *only* uses the 6 features from the assessment.
        # This may need refinement if prediction accuracy is low.
        df = pd.DataFrame([data], columns=feature_order)
        
        prediction = model.predict(df)[0]
        probability = np.max(model.predict_proba(df))
        
        # Output: 1 = Yes, 0 = No
        return {"prediction": int(prediction), "probability": float(probability)}
    except Exception as e:
        current_app.logger.error(f"Diabetes prediction error: {e}")
        raise ValueError("Failed to preprocess diabetes data. Is model a pipeline? Are all features present?")

def predict_heart(data: Dict[str, Any]) -> Dict[str, Any]:
    model = models.get('heart')
    preprocessor = preprocessors.get('heart')
    
    if model is None or preprocessor is None:
        current_app.logger.error("Heart model or preprocessor is not loaded.")
        raise RuntimeError("Heart model or preprocessor is not loaded.")
        
    try:
        # Data dict comes from HeartAssessment.to_dict()
        # It needs patient 'age' and 'gender'
        # The *caller* (api/predict.py) must add these.
        
        # Define expected columns for the preprocessor
        # This must match the training notebook
        feature_columns = [
            'age', 'gender', 'chest_pain_type', 'resting_blood_pressure',
            'cholesterol', 'fasting_blood_sugar', 'resting_ecg',
            'max_heart_rate', 'exercise_angina', 'st_depression', 'st_slope'
        ]
        
        # Map 'gender' from 'Male'/'Female' to 0/1 as expected by preprocessor
        data['gender'] = 1 if data.get('gender') == 'Male' else 0

        df = pd.DataFrame([data], columns=feature_columns)
        
        # Apply the preprocessor first
        df_processed = preprocessor.transform(df) 
        
        # Predict on the processed data
        prediction = model.predict(df_processed)[0] 
        probability = np.max(model.predict_proba(df_processed))
            
        # Output: 1 = Yes, 0 = No
        return {"prediction": int(prediction), "probability": float(probability)}
    except Exception as e:
        current_app.logger.error(f"Heart prediction error: {e}")
        raise ValueError("Failed to preprocess heart data. Check model/preprocessor and features.")

def predict_liver(data: Dict[str, Any]) -> Dict[str, Any]:
    model = models.get('liver')
    if model is None:
        current_app.logger.error("Liver model is not loaded.")
        raise RuntimeError("Liver model is not loaded.")

    try:
        data_processed = data.copy()
        
        # Map 'gender' (must be added by caller)
        data_processed['Gender'] = 1 if data_processed.get('gender') == 'Male' else 0
        
        # --- FIX: Calculate A/G Ratio as required by model ---
        # The model expects 'Albumin_and_Globulin_Ratio'
        # We get albumin and globulin from the assessment data
        albumin = data_processed.get('albumin', 0)
        globulin = data_processed.get('globulin', 0)
        
        if globulin and globulin > 0:
            data_processed['Albumin_and_Globulin_Ratio'] = round(albumin / globulin, 2)
        else:
            # Handle division by zero, e.g., assign a default or median
            data_processed['Albumin_and_Globulin_Ratio'] = 0.9 # Placeholder
        # --- End Fix ---
        
        # FIX: Rename keys to match the model's expected feature names
        # (Based on common notebook practices)
        key_map = {
            'age': 'Age',
            'gender': 'Gender', # Already mapped
            'total_bilirubin': 'Total_Bilirubin',
            'direct_bilirubin': 'Direct_Bilirubin',
            'alkaline_phosphotase': 'Alkaline_Phosphotase',
            'alamine_aminotransferase': 'Alamine_Aminotransferase',
            'aspartate_aminotransferase': 'Aspartate_Aminotransferase',
            'total_proteins': 'Total_Protiens', # Keep typo if model was trained with it
            'albumin': 'Albumin',
            'globulin': 'Globulin', # Not a feature, used for ratio
            'Albumin_and_Globulin_Ratio': 'Albumin_and_Globulin_Ratio' # Calculated
        }
        
        model_input_data = {
            key_map.get(k, k): v for k, v in data_processed.items()
        }

        # Define feature order for the model
        # This must match the training notebook
        feature_columns = [
            'Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 
            'Alkaline_Phosphotase', 'Alamine_Aminotransferase', 
            'Aspartate_Aminotransferase', 'Total_Protiens', 'Albumin', 
            'Albumin_and_Globulin_Ratio'
        ]
        
        df = pd.DataFrame([model_input_data], columns=feature_columns)
        
        # The .pkl is assumed to be a pipeline (scaler + model)
        prediction = model.predict(df)[0]
        probability = np.max(model.predict_proba(df))
        
        # Model output 1=disease, 2=no disease. Map to 1 and 0
        prediction_mapped = 1 if prediction == 1 else 0
        
        return {"prediction": int(prediction_mapped), "probability": float(probability)}
    except Exception as e:
        current_app.logger.error(f"Liver prediction error: {e}")
        raise ValueError("Failed to preprocess liver data. Is model a pipeline? Check feature names.")


def predict_mental_health(data: Dict[str, Any]) -> Dict[str, Any]:
    model = models.get('mental_health')
    if model is None:
        current_app.logger.error("Mental Health model is not loaded.")
        raise RuntimeError("Mental Health model is not loaded.")
        
    try:
        # This model is based on PHQ-9, GAD-7, etc.
        # The schema provides: 'phq_score', 'gad_score', 'sleep_quality', 'mood_factors'
        # The model likely expects 'Age' as well (per MVP).
        # The *caller* (api/predict.py) must add 'age'.
        
        # The model .pkl is assumed to be a full pipeline that handles
        # all required preprocessing (e.g., encoding 'mood_factors' if used).
        
        # Define features based on schema + patient
        feature_columns = [
            'age', 'phq_score', 'gad_score', 'sleep_quality', 'mood_factors'
        ]
        
        df = pd.DataFrame([data], columns=feature_columns)
        
        prediction = model.predict(df)[0]
        probability = np.max(model.predict_proba(df))
        
        # Output: 1 = Yes (at risk), 0 = No
        return {"prediction": int(prediction), "probability": float(probability)}
            
    except Exception as e:
        current_app.logger.error(f"Mental Health prediction error: {e}")
        raise ValueError("Failed to preprocess mental health data. The .pkl must be a full pipeline.")


# --- Main Service Function ---

def run_prediction(assessment_type: str, input_data: dict) -> dict:
    """
    Routes prediction task to the correct function.
    """
    current_app.logger.info(f"Running prediction for {assessment_type}")
    
    if assessment_type == 'diabetes':
        return predict_diabetes(input_data)
    elif assessment_type == 'heart':
        return predict_heart(input_data)
    elif assessment_type == 'liver':
        return predict_liver(input_data)
    elif assessment_type == 'mental_health':
        return predict_mental_health(input_data)
    else:
        current_app.logger.error(f"Invalid assessment type: {assessment_type}")
        raise ValueError("Invalid assessment type")