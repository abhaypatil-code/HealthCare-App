# HealthCare App/medml-backend/app/db_seeder.py
from app.models import db, LifestyleRecommendation
from flask import current_app

def seed_static_recommendations():
    """
    Populates the LifestyleRecommendation table with static MVP data
    if it is currently empty.
    """
    try:
        if LifestyleRecommendation.query.first() is not None:
            # Data already exists, do nothing
            return

        recommendations = [
            # Diabetes
            LifestyleRecommendation(disease_type='diabetes', risk_level='Low', recommendation_text='Monitor blood sugar regularly. Maintain a balanced diet rich in fiber and whole grains. Engage in at least 30 minutes of moderate exercise daily.'),
            LifestyleRecommendation(disease_type='diabetes', risk_level='Medium', recommendation_text='Consult a dietician to create a specific meal plan. Increase physical activity and monitor blood glucose levels closely, especially after meals.'),
            LifestyleRecommendation(disease_type='diabetes', risk_level='High', recommendation_text='Urgent consultation with a doctor or endocrinologist is required. Follow a strict diet, monitor glucose multiple times a day, and discuss medication options with your doctor.'),
            
            # Liver
            LifestyleRecommendation(disease_type='liver', risk_level='Low', recommendation_text='Avoid alcohol and processed foods. Maintain a healthy weight and drink plenty of water. Eat a balanced diet with plenty of fruits and vegetables.'),
            LifestyleRecommendation(disease_type='liver', risk_level='Medium', recommendation_text='Limit fat, sugar, and salt intake. Avoid alcohol completely. Consult a doctor for liver function tests and possible dietary supplements.'),
            LifestyleRecommendation(disease_type='liver', risk_level='High', recommendation_text='Seek immediate medical attention from a hepatologist. Strict dietary restrictions are necessary. Avoid all alcohol, over-the-counter drugs (unless approved), and fatty foods.'),
            
            # Heart
            LifestyleRecommendation(disease_type='heart', risk_level='Low', recommendation_text='Maintain a heart-healthy diet (low in sodium and saturated fats). Engage in regular aerobic exercise (e.g., brisk walking, cycling). Manage stress levels.'),
            LifestyleRecommendation(disease_type='heart', risk_level='Medium', recommendation_text='Monitor blood pressure and cholesterol levels. Consult a doctor to discuss risk factors. Implement significant lifestyle changes, including diet and at least 150 minutes of exercise per week.'),
            LifestyleRecommendation(disease_type='heart', risk_level='High', recommendation_text='Urgent consultation with a cardiologist. Your doctor may recommend medication to manage blood pressure or cholesterol. A strict, low-sodium, low-fat diet and a supervised exercise plan are critical.'),
            
            # Mental Health
            LifestyleRecommendation(disease_type='mental_health', risk_level='Low', recommendation_text='Practice mindfulness or meditation for 10-15 minutes daily. Ensure 7-9 hours of quality sleep. Stay connected with friends and family.'),
            LifestyleRecommendation(disease_type='mental_health', risk_level='Medium', recommendation_text='Consider speaking to a counselor or therapist. Establish a consistent daily routine. Engage in hobbies and activities you enjoy to reduce stress.'),
            LifestyleRecommendation(disease_type='mental_health', risk_level='High', recommendation_text='Please see a mental health professional (psychologist or psychiatrist) immediately. Do not hesitate to reach out to a support hotline if you are in distress. Follow the treatment plan prescribed by your doctor.')
        ]
        
        db.session.bulk_save_objects(recommendations)
        db.session.commit()
        current_app.logger.info("Successfully seeded static LifestyleRecommendations.")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error seeding database: {e}")