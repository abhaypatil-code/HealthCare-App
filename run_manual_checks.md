# Manual Test Cases for Streamlit Frontend

## Prerequisites
1. Backend server running on `http://127.0.0.1:5000`
2. Streamlit frontend running on `http://127.0.0.1:8501`
3. Admin account: `admin` / `Admin123!`
4. Test patient account: `12345678901234` / `12345678901234@Default123`

## Test Case 1: Admin Login and Dashboard Access

### Steps:
1. Open browser and navigate to `http://127.0.0.1:8501`
2. In the "Healthcare Worker Login" section, enter:
   - Username: `admin`
   - Password: `Admin123!`
3. Click "Login as Admin"

### Expected Results:
- ✅ Login successful
- ✅ Redirected to Admin Dashboard
- ✅ Welcome message displayed: "Welcome, Admin!"
- ✅ Dashboard shows analytics (Today's Registrations, Risk counts)
- ✅ "Add New User" and "View Registered Patients" buttons visible

---

## Test Case 2: Patient Registration Flow

### Steps:
1. From Admin Dashboard, click "Add New User"
2. Fill in patient basic information:
   - Full Name: `John Doe`
   - ABHA ID: `11111111111111`
   - Age: `45`
   - Gender: `Male`
   - Height: `175` cm
   - Weight: `80` kg
   - State: `Karnataka`
3. Click "Save and Proceed to Health Assessment"
4. Complete all 4 assessments:
   - **Diabetes Assessment:**
     - Pregnancy: `No`
     - Glucose: `120`
     - Blood Pressure: `85`
     - Skin Thickness: `25`
     - Insulin: `100`
     - Diabetes History: `No`
   - **Liver Assessment:**
     - Total Bilirubin: `1.2`
     - Direct Bilirubin: `0.3`
     - Alkaline Phosphatase: `100`
     - SGPT: `30`
     - SGOT: `25`
     - Total Protein: `7.0`
     - Albumin: `4.0`
   - **Heart Assessment:**
     - Diabetes: `No`
     - Hypertension: `No`
     - Obesity: `No`
     - Smoking: `No`
     - Alcohol Consumption: `No`
     - Physical Activity: `Yes`
     - Diet Score: `7`
     - Cholesterol Level: `200`
     - Triglyceride Level: `150`
     - LDL Level: `120`
     - HDL Level: `50`
     - Systolic BP: `120`
     - Diastolic BP: `80`
     - Air Pollution Exposure: `50`
     - Family History: `No`
     - Stress Level: `5`
     - Heart Attack History: `No`
   - **Mental Health Assessment:**
     - PHQ Score: `5`
     - GAD Score: `3`
     - Depressiveness: `No`
     - Suicidal: `No`
     - Anxiousness: `No`
     - Sleepiness: `No`
5. Click "Finish Survey & Run Risk Analysis"

### Expected Results:
- ✅ Patient created successfully
- ✅ All assessments completed
- ✅ Risk analysis triggered
- ✅ Success message displayed
- ✅ Redirected to main dashboard
- ✅ New patient appears in patient list

---

## Test Case 3: Patient List and Details View

### Steps:
1. From Admin Dashboard, click "View Registered Patients"
2. Select "All Users" tab
3. Click "View Details" on any patient
4. Verify patient information is displayed
5. Check assessment history tabs
6. Test "Retry Prediction" button
7. Test "View Latest Prediction" button

### Expected Results:
- ✅ Patient list loads correctly
- ✅ Patient details page displays all information
- ✅ Assessment history shows in tabs
- ✅ Risk assessment table displays
- ✅ Prediction management buttons work
- ✅ BMI and A/G ratio calculated correctly

---

## Test Case 4: Consultation Booking

### Steps:
1. From patient detail view, scroll to "Consultation Actions"
2. If patient has Medium/High risk conditions, click consultation buttons
3. Verify consultation booking success message
4. Check "Notes for Doctor" section
5. Add a test note and save

### Expected Results:
- ✅ Consultation buttons appear for Medium/High risk conditions
- ✅ Consultation booking successful
- ✅ Success message displayed
- ✅ Notes can be added and saved
- ✅ Previous notes displayed

---

## Test Case 5: Patient Login and Dashboard

### Steps:
1. Logout from admin account
2. In "Patient Login" section, enter:
   - ABHA ID: `12345678901234`
   - Password: `12345678901234@Default123`
3. Click "Login as Patient"

### Expected Results:
- ✅ Patient login successful
- ✅ Redirected to Patient Dashboard
- ✅ Welcome message: "Welcome, [Patient Name]!"
- ✅ Health metrics displayed (BMI, Height, Weight)
- ✅ Risk assessment table shows
- ✅ Assessment history tabs available
- ✅ Healthcare worker information displayed
- ✅ Lifestyle recommendations shown

---

## Test Case 6: Patient PDF Report Generation

### Steps:
1. In Patient Dashboard, click "Download PDF" button
2. Select sections: "Overview", "Diabetes", "Heart"
3. Click "Download PDF"
4. Verify PDF downloads successfully

### Expected Results:
- ✅ PDF download modal opens
- ✅ Section selection works
- ✅ PDF generates successfully
- ✅ File downloads with correct name
- ✅ PDF contains selected sections

---

## Test Case 7: Patient Assessment History

### Steps:
1. In Patient Dashboard, navigate to "Assessment History" section
2. Click on different assessment tabs (Diabetes, Liver, Heart, Mental Health)
3. Verify assessment data is displayed correctly

### Expected Results:
- ✅ Assessment history section visible
- ✅ All assessment tabs work
- ✅ Assessment data displayed in tables
- ✅ Empty tabs show appropriate messages

---

## Test Case 8: Error Handling and Edge Cases

### Steps:
1. Try logging in with wrong credentials
2. Try accessing patient details without login
3. Try creating patient with invalid ABHA ID
4. Try triggering prediction without completing assessments
5. Test with backend server stopped

### Expected Results:
- ✅ Wrong credentials show error message
- ✅ Unauthorized access blocked
- ✅ Invalid ABHA ID validation works
- ✅ Prediction failure handled gracefully
- ✅ Backend connectivity issues handled

---

## Test Case 9: Computed Fields Validation

### Steps:
1. Create patient with specific height/weight values
2. Verify BMI calculation matches backend
3. Create liver assessment with specific protein/albumin values
4. Verify A/G ratio calculation matches backend

### Expected Results:
- ✅ BMI calculated correctly in frontend
- ✅ A/G ratio calculated correctly in frontend
- ✅ Values match backend calculations
- ✅ Real-time updates as values change

---

## Test Case 10: Role-Based Access Control

### Steps:
1. Login as patient
2. Try to access admin-only features
3. Login as admin
4. Try to access other patients' data
5. Verify proper error messages

### Expected Results:
- ✅ Patient cannot access admin features
- ✅ Admin can access all features
- ✅ Proper error messages for unauthorized access
- ✅ Role-based UI elements displayed correctly

---

## Test Case 11: ML Prediction Retry Functionality

### Steps:
1. Create patient with all assessments
2. Trigger prediction (may fail if models not loaded)
3. Use "Retry Prediction" button
4. Verify prediction status updates

### Expected Results:
- ✅ Prediction retry button works
- ✅ Failure messages informative
- ✅ Success/failure handled gracefully
- ✅ UI updates after retry

---

## Test Case 12: Session Management

### Steps:
1. Login as admin
2. Leave browser idle for 15+ minutes
3. Try to perform actions
4. Test logout functionality
5. Verify session cleanup

### Expected Results:
- ✅ Session expires after token expiry
- ✅ Proper re-authentication prompts
- ✅ Logout clears session state
- ✅ No data leakage between sessions

---

## Success Criteria

All test cases must pass for the frontend to be considered fully functional:

- ✅ All login flows work correctly
- ✅ Patient registration and assessment flows complete
- ✅ ML predictions trigger and display results
- ✅ PDF generation works
- ✅ Role-based access control enforced
- ✅ Error handling graceful and informative
- ✅ Computed fields calculated correctly
- ✅ Session management secure
- ✅ UI responsive and user-friendly

## Notes

- Some tests may fail if ML models are not loaded in backend
- PDF generation requires proper backend configuration
- Recommendations require GEMINI_API_KEY configuration
- All tests should be run with backend server running
- Test data should be cleaned up after testing
