# Quick Start Guide - Rural Healthcare System

## 🚀 5-Minute Setup & Demo

### 1️⃣ Setup Gemini API (Required for Recommendations)
When you first open the app, you'll be prompted to enter your Gemini API key:
- Get a free API key from: https://makersuite.google.com/app/apikey
- Paste it when prompted
- This enables AI-powered personalized health recommendations

### 2️⃣ Login as Healthcare Worker
```
Username: admin
Password: admin123
```

### 3️⃣ Create Your First Patient

Click **"Add New User"** and fill in:

**Basic Information:**
- Name: `Ramesh Kumar`
- ABHA ID: `12345678901234` (any 14 digits)
- Age: `45`
- Gender: `Male`
- Height: `170` cm
- Weight: `75` kg
- State: `Karnataka`

Click **Submit** → You'll see the Assessment Dashboard

### 4️⃣ Complete Health Assessments

**Diabetes Assessment:**
- Pregnancies: `0`
- Blood Glucose: `140` mg/dL
- Blood Pressure: `135` mm Hg
- Skin Thickness: `25` mm
- Insulin: `80` μU/mL
- ✓ Has diabetes diagnosis

**Liver Assessment:**
- Total Bilirubin: `1.2` mg/dL
- Direct Bilirubin: `0.4` mg/dL
- Alkaline Phosphatase: `120` IU/L
- SGPT: `45` U/L
- SGOT: `40` U/L
- Total Protein: `7.0` g/dL
- Albumin: `4.2` g/dL

**Heart Assessment:**
- ✓ Diabetes
- ✓ Hypertension
- ✓ Smoking
- Diet Score: `5`
- Cholesterol: `220` mg/dL
- Triglycerides: `180` mg/dL
- LDL: `130` mg/dL
- HDL: `40` mg/dL
- Systolic BP: `140` mm Hg
- Diastolic BP: `90` mm Hg
- Air Pollution: `5`
- ✓ Family History
- Stress Level: `7`

**Mental Health Assessment:**
- PHQ-9 Score: `8`
- GAD-7 Score: `6`
- Depressiveness: `0.3`
- Anxiousness: `0.4`
- Sleep Disturbance: `0.5`

After all 4 assessments, click **"Finish Survey & Calculate Risk Predictions"**

### 5️⃣ View Analytics Dashboard

You'll see:
- Today's registrations: `1`
- Risk summaries for each disease
- Total at-risk patients

### 6️⃣ View Patient Details

Click **"View Registered Patients"** → **"View"** on Ramesh Kumar

You'll see:
- Complete patient information
- Risk assessments with color-coded levels
- Consultation booking options (based on risk level)
- Add symptoms/notes section
- All assessment data

### 7️⃣ Book Consultations

Based on risk levels:
- **High Risk** → "Book In-Person" consultation with specialist
- **Medium Risk** → "Book Tele" consultation (e-Sanjeevani)
- **Low Risk** → No booking needed, follow preventive care

### 8️⃣ Patient Login

Logout and switch to **"Patient"** tab:
```
ABHA ID: 12345678901234
Password: 123456 (default)
```

As a patient, you can:
- View health dashboard with BMI
- See risk assessment for all diseases
- View upcoming appointments
- Read personalized recommendations
- Check medication schedule
- Download/Share health reports

## 📊 Sample Test Cases

### High Risk Diabetes Patient
```
Glucose: 200 mg/dL
Blood Pressure: 145 mm Hg
BMI: 32 (calc from 85kg, 170cm)
Diabetes History: ✓
```

### High Risk Heart Patient
```
Cholesterol: 250 mg/dL
Systolic BP: 160 mm Hg
Smoking: ✓
Family History: ✓
Heart Attack History: ✓
```

### High Risk Mental Health Patient
```
PHQ-9 Score: 20
GAD-7 Score: 18
Depressiveness: 0.8
Suicidal Ideation: ✓
```

## 🎯 Key Features to Test

### Patient Dashboard
1. ✅ BMI calculation (automatic)
2. ✅ Color-coded risk table (green/yellow/red)
3. ✅ Appointment list (based on risk level)
4. ✅ Lifestyle recommendations (AI-generated)
5. ✅ Medication schedule with timing dots
6. ✅ Download/Share functionality

### Admin Dashboard
1. ✅ Multi-step patient registration
2. ✅ 4 comprehensive health assessment forms
3. ✅ Real-time analytics
4. ✅ Patient filtering (All/Diabetes/Liver/Heart/Mental)
5. ✅ Sorting (High Risk/Medium Risk/Recent)
6. ✅ Consultation booking with confirmation
7. ✅ Healthcare worker notes

### Disease-Specific Tabs
1. ✅ Risk score display
2. ✅ Contributing factors list
3. ✅ Next action steps
4. ✅ Risk-level specific guidance
5. ✅ Personalized recommendations by category

## 🔍 Testing Filters & Sorting

**View Patients by Category:**
- All Users → Shows everyone
- Diabetes → Only patients with Medium/High diabetes risk
- Liver → Only patients with Medium/High liver risk
- Heart → Only patients with Medium/High heart risk
- Mental Health → Only patients with Medium/High mental health risk

**Sort Options:**
- Recently Added → Newest patients first
- High Risk → Only high-risk patients for selected category
- Medium Risk → Only medium-risk patients for selected category

## ⚠️ Important Notes

1. **ABHA ID must be exactly 14 digits** (validation enabled)
2. **All 4 assessments must be completed** before finishing survey
3. **Default patient password is `123456`** (can be changed in backend)
4. **Gemini API key is required** for AI recommendations to work
5. **Risk calculation happens automatically** after completing all assessments

## 🐛 Troubleshooting

**"No predictions found" error:**
- Make sure all 4 assessments are completed
- Click "Finish Survey" button after assessments
- Wait a few seconds for calculations

**No recommendations showing:**
- Verify Gemini API key is entered correctly
- Check browser console for API errors
- Default recommendations will show if API fails

**Patient login not working:**
- Verify ABHA ID is exactly 14 digits
- Default password is `123456`
- Check if patient was created successfully

## 💡 Tips

- Create multiple patients with different risk profiles to see dashboard variations
- Test both High and Medium risk levels to see different consultation options
- Try filtering and sorting in the View Patients section
- Explore each disease-specific tab as a patient to see personalized content
- Add notes in the admin view and see them reflected in patient view

---

**Ready to explore? Start with Step 1 above! 🎉**
