// HealthCare App/src/types/index.ts
// --- EXPANDED to include all types for the application ---

/**
 * Represents the Admin User (Healthcare Worker)
 */
export interface AdminUser {
  id: number;
  name: string;
  email: string;
  role: 'admin';
  designation: string | null;
  contact_number: string | null;
}

/**
 * Represents the Patient User
 */
export interface PatientUser {
  id: number;
  full_name: string;
  age: number;
  gender: string;
  abha_id: string; // 14-digit string
  height_cm: number;
  weight_kg: number;
  bmi: number;
  state_name: string | null;
  created_by_user_id: number;
  created_at: string; // ISO date string
  
  // Linked data
  assessments: PatientAssessments;
  risk_prediction: RiskPrediction | null;
  consultations?: Consultation[]; // Added
}

/**
 * A container for all 4 assessment types
 */
export interface PatientAssessments {
  diabetes: DiabetesAssessment | null;
  liver: LiverAssessment | null;
  heart: HeartAssessment | null;
  mental_health: MentalHealthAssessment | null;
}

// --- Assessment Data Types ---

export interface DiabetesAssessment {
  pregnancies: number;
  glucose: number;
  blood_pressure: number;
  skin_thickness: number;
  insulin: number;
  diabetes_pedigree_function: number;
  assessed_at: string; // ISO date string
}

export interface LiverAssessment {
  total_bilirubin: number;
  direct_bilirubin: number;
  alkaline_phosphotase: number;
  alamine_aminotransferase: number;
  aspartate_aminotransferase: number;
  total_proteins: number;
  albumin: number;
  globulin: number;
  ag_ratio: number | null;
  assessed_at: string; // ISO date string
}

export interface HeartAssessment {
  chest_pain_type: number;
  resting_blood_pressure: number;
  cholesterol: number;
  fasting_blood_sugar: number;
  resting_ecg: number;
  max_heart_rate: number;
  exercise_angina: number;
  st_depression: number;
  st_slope: number;
  assessed_at: string; // ISO date string
}

export interface MentalHealthAssessment {
  phq_score: number;
  gad_score: number;
  sleep_quality: number;
  mood_factors: string | null;
  assessed_at: string; // ISO date string
}

/**
 * Represents the ML Risk Prediction results
 */
export interface RiskPrediction {
  patient_id: number;
  diabetes_score: number | null;
  diabetes_level: 'Low' | 'Medium' | 'High' | null;
  liver_score: number | null;
  liver_level: 'Low' | 'Medium' | 'High' | null;
  heart_score: number | null;
  heart_level: 'Low' | 'Medium' | 'High' | null;
  mental_health_score: number | null;
  mental_health_level: 'Low' | 'Medium' | 'High' | null;
  model_version: string | null;
  predicted_at: string; // ISO date string
}

/**
 * Represents a (dummy) consultation
 */
export interface Consultation {
  id: number;
  patient_id: number;
  admin_id: number;
  consultation_type: 'Teleconsultation' | 'In-Person';
  consultation_datetime: string; // ISO date string
  notes: string | null;
  status: 'Booked' | 'Completed';
  created_at: string; // ISO date string
}

/**
 * Represents a lifestyle recommendation
 */
export interface LifestyleRecommendation {
  id: number;
  disease_type: 'diabetes' | 'liver' | 'heart' | 'mental_health' | 'general';
  risk_level: 'Low' | 'Medium' | 'High';
  category: 'Diet' | 'Exercise' | 'Sleep' | 'Lifestyle' | 'general';
  recommendation_text: string;
}


// --- API Login Payloads ---

export interface AdminLoginPayload {
  email: string;
  password: string;
}

export interface PatientLoginPayload {
  abha_id: string; // 14-digit string
  password: string;
}