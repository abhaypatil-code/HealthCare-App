# HealthCare App/medml-backend/app/services.py
import joblib
import pandas as pd
import numpy as np
import os
import json
import google.generativeai as genai
from typing import Dict, Any, List
from flask import current_app

# Path to models_store directory
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models_store')

# Global dictionary to hold models and preprocessors
models = {
    'diabetes': None,
    'heart': None,
    'liver': None,
    'mental_health': None
}
# --- FIX: Removed preprocessor dict ---
# preprocessors = {
#     'heart': None
# }

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
        models['mental_health'] = load_model(app, 'mental_health', 'mental_health_depressiveness.pkl')
        
        # --- FIX: Removed loading of the problematic preprocessor ---
        # preprocessors['heart'] = load_model(app, 'heart_preprocessor', 'heart_preprocessor.pkl')
        
        app.logger.info("Model loading complete.")
        
        # --- Configure Gemini ---
        try:
            api_key = app.config.get('GEMINI_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                app.logger.info("Gemini API configured successfully.")
            else:
                app.logger.warning("GEMINI_API_KEY is not set. Recommendation service will be disabled.")
        except Exception as e:
            app.logger.error(f"Error configuring Gemini API: {e}")

# --- Preprocessing & Prediction Logic (UPDATED) ---

def predict_diabetes(data: Dict[str, Any]) -> float:
    model = models.get('diabetes')
    if model is None:
        current_app.logger.error("Diabetes model is not loaded.")
        raise RuntimeError("Diabetes model is not loaded.")
        
    try:
        # --- UPDATED FEATURES per SRD ---
        feature_order = [
            'pregnancy', 'glucose', 'blood_pressure', 'skin_thickness', 
            'insulin', 'diabetes_history', 'age', 'bmi'
        ]
        
        # Convert bools to int
        data['pregnancy'] = 1 if data.get('pregnancy') else 0
        data['diabetes_history'] = 1 if data.get('diabetes_history') else 0

        df = pd.DataFrame([data], columns=feature_order)
        
        # Predict probability of class 1 (disease)
        probability = model.predict_proba(df)[0][1] 
        
        return float(probability)
    except Exception as e:
        current_app.logger.error(f"Diabetes prediction error: {e}")
        raise ValueError("Failed to preprocess diabetes data.")

def predict_heart(data: Dict[str, Any]) -> float:
    model = models.get('heart')
    # --- FIX: Removed preprocessor ---
    # preprocessor = preprocessors.get('heart')
    
    # --- FIX: Removed preprocessor check ---
    if model is None:
        current_app.logger.error("Heart model is not loaded.")
        raise RuntimeError("Heart model is not loaded.")
        
    try:
        # --- UPDATED FEATURES per SRD ---
        feature_columns = [
            'diabetes', 'hypertension', 'obesity', 'smoking', 'alcohol_consumption', 
            'physical_activity', 'diet_score', 'cholesterol_level', 
            'triglyceride_level', 'ldl_level', 'hdl_level', 'systolic_bp', 
            'diastolic_bp', 'air_pollution_exposure', 'family_history', 
            'stress_level', 'heart_attack_history', 'age', 'gender', 'bmi'
        ]
        
        # Map 'gender' from 'Male'/'Female' to 0/1
        data['gender'] = 1 if data.get('gender') == 'Male' else 0
        
        # Convert bools to int
        bool_cols = ['diabetes', 'hypertension', 'obesity', 'smoking', 'alcohol_consumption', 
                     'physical_activity', 'family_history', 'heart_attack_history']
        for col in bool_cols:
            data[col] = 1 if data.get(col) else 0

        df = pd.DataFrame([data], columns=feature_columns)
        
        # --- FIX: Removed preprocessor step ---
        # df_processed = preprocessor.transform(df) 
        
        # --- FIX: Predict on the raw df, assuming model is a pipeline ---
        probability = model.predict_proba(df)[0][1]
            
        return float(probability)
    except Exception as e:
        current_app.logger.error(f"Heart prediction error: {e}")
        raise ValueError("Failed to preprocess heart data.")

def predict_liver(data: Dict[str, Any]) -> float:
    model = models.get('liver')
    if model is None:
        current_app.logger.error("Liver model is not loaded.")
        raise RuntimeError("Liver model is not loaded.")

    try:
        data_processed = data.copy()
        
        # Map 'gender'
        data_processed['Gender'] = 1 if data_processed.get('gender') == 'Male' else 0
        
        # --- UPDATED: Calculate A/G Ratio per SRD/model ---
        albumin = data_processed.get('albumin', 0)
        total_protein = data_processed.get('total_protein', 0)
        
        if total_protein and albumin and total_protein > albumin:
            globulin = total_protein - albumin
            data_processed['Albumin_and_Globulin_Ratio'] = round(albumin / globulin, 2)
        else:
            data_processed['Albumin_and_Globulin_Ratio'] = 0.9 # Placeholder median
        # --- End Update ---
        
        # Map keys to match the model's expected feature names
        key_map = {
            'age': 'Age',
            'gender': 'Gender',
            'total_bilirubin': 'Total_Bilirubin',
            'direct_bilirubin': 'Direct_Bilirubin',
            'alkaline_phosphatase': 'Alkaline_Phosphotase',
            'sgpt_alamine_aminotransferase': 'Alamine_Aminotransferase', # Model might have this name
            'sgot_aspartate_aminotransferase': 'Aspartate_Aminotransferase', # Model might have this name
            'total_protein': 'Total_Protiens', # Keep typo if model was trained with it
            'albumin': 'Albumin',
            'ag_ratio': 'Albumin_and_Globulin_Ratio' # Calculated
        }
        
        model_input_data = {
            key_map.get(k, k): v for k, v in data_processed.items()
        }

        # Define feature order for the model
        feature_columns = [
            'Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 
            'Alkaline_Phosphotase', 'Alamine_Aminotransferase', 
            'Aspartate_Aminotransferase', 'Total_Protiens', 'Albumin', 
            'Albumin_and_Globulin_Ratio'
        ]
        
        df = pd.DataFrame([model_input_data], columns=feature_columns)
        
        # Predict probability of class 1 (disease)
        probability = model.predict_proba(df)[0][1]
        
        return float(probability)
    except Exception as e:
        current_app.logger.error(f"Liver prediction error: {e}")
        raise ValueError("Failed to preprocess liver data.")


def predict_mental_health(data: Dict[str, Any]) -> float:
    model = models.get('mental_health')
    if model is None:
        current_app.logger.error("Mental Health model is not loaded.")
        raise RuntimeError("Mental Health model is not loaded.")
        
    try:
        # --- UPDATED FEATURES per SRD ---
        feature_columns = [
            'phq_score', 'gad_score', 'depressiveness', 'suicidal', 
            'anxiousness', 'sleepiness', 'age', 'gender'
        ]
        
        # Map 'gender' from 'Male'/'Female' to 0/1
        data['gender'] = 1 if data.get('gender') == 'Male' else 0
        
        # Convert bools to int
        bool_cols = ['depressiveness', 'suicidal', 'anxiousness', 'sleepiness']
        for col in bool_cols:
            data[col] = 1 if data.get(col) else 0

        df = pd.DataFrame([data], columns=feature_columns)
        
        # Predict probability of class 1 (disease)
        probability = model.predict_proba(df)[0][1]
            
        return float(probability)
    except Exception as e:
        current_app.logger.error(f"Mental Health prediction error: {e}")
        raise ValueError("Failed to preprocess mental health data.")


# --- Main Service Function ---

def run_prediction(assessment_type: str, input_data: dict) -> float:
    """
    Routes prediction task to the correct function.
    Returns the raw risk score (probability).
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

# --- Gemini Recommendation Service ---

def get_gemini_recommendations(risk_map: dict) -> List[Dict[str, Any]]:
    """
    Generates lifestyle recommendations using the Gemini API based on the
    patient's risk profile.
    """
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key:
        current_app.logger.warning("GEMINI_API_KEY not set. Returning empty recommendations.")
        return []

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        # Build a prompt focusing on Medium/High risks
        risk_summary = []
        has_high_risk = False
        for disease, level in risk_map.items():
            if level in ['Medium', 'High']:
                disease_name = disease.replace("_risk_level", "").capitalize()
                risk_summary.append(f"- {disease_name}: {level} risk")
                if level == 'High':
                    has_high_risk = True

        if not risk_summary:
            prompt_intro = "The patient has Low risk for all assessed conditions (diabetes, liver, heart, mental health)."
            prompt_request = "Provide 2-3 general preventative lifestyle recommendations."
        else:
            prompt_intro = "A patient has the following health risk profile:\n" + "\n".join(risk_summary)
            if has_high_risk:
                prompt_request = "Provide a mix of actionable lifestyle recommendations (diet, exercise, sleep, habits) for these conditions, prioritizing the 'High' risk items. Provide 2-3 recommendations per HIGH risk condition and 1-2 per MEDIUM risk condition."
            else:
                prompt_request = "Provide actionable lifestyle recommendations (diet, exercise, sleep, habits) for these 'Medium' risk conditions. Provide 2-3 recommendations per condition."

        # JSON format instruction
        prompt = f"""
        You are a helpful, empathetic health assistant. {prompt_intro}

        {prompt_request}

        Format your response *only* as a valid JSON list of objects.
        Each object in the list must have the following keys:
        - "disease_type": (string) The disease this applies to (e.g., "Diabetes", "Heart", "General"). Use the capitalized name.
        - "risk_level": (string) The risk level this applies to (e.g., "High", "Medium", "Low").
        - "category": (string) The category of advice (e.g., "Diet", "Exercise", "Sleep", "Lifestyle").
        - "recommendation_text": (string) The specific recommendation.

        Example:
        [
          {{
            "disease_type": "Diabetes",
            "risk_level": "High",
            "category": "Diet",
            "recommendation_text": "Monitor blood sugar as advised by your doctor. Strictly limit sugary drinks and processed carbohydrates."
          }}
        ]

        Provide *only* the JSON list.
        """
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        response = model.generate_content(prompt, safety_settings=safety_settings)
        
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        recommendations = json.loads(cleaned_text)
        
        # Group recommendations by category for frontend
        grouped_recs = {"diet": [], "exercise": [], "sleep": [], "lifestyle": []}
        for rec in recommendations:
            cat = rec.get("category", "Lifestyle").lower()
            if cat in grouped_recs:
                grouped_recs[cat].append(rec)
            else:
                grouped_recs["lifestyle"].append(rec)
            
        current_app.logger.info(f"Successfully fetched {len(recommendations)} recommendations from Gemini.")
        return grouped_recs

    except Exception as e:
        current_app.logger.error(f"Error calling Gemini API: {e}. Response text: {response.text if 'response' in locals() else 'N/A'}")
        return {"diet": [], "exercise": [], "sleep": [], "lifestyle": []}