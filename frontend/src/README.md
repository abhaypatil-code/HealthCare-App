# MedML: AI-Powered Rural Healthcare Platform

This project provides a full-stack solution for medical professionals to manage patients and run predictive models for various diseases. It consists of a Flask backend (serving a REST API and models) and a React frontend.

## Prerequisites

Before you begin, ensure you have the following installed:

* **Python:** 3.10 or newer (with `pip` and `venv`)
* **Node.js:** v18 or newer (with `npm`)
* **Prediction Models:** You must have the four `.pkl` model files:
    * `diabetes.pkl`
    * `heart.pkl`
    * `liver.pkl`
    * `mental_health.pkl`

---

## 1. Backend Setup (Flask API)

1.  **Navigate to the Backend Directory:**
    ```bash
    # From the project root, navigate to the backend folder
    cd medml-backend 
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Python Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Place the Prediction Models:**
    This is a critical step. Create a directory named `models_store` in the **project root** (one level *above* the `medml-backend` directory) and place the four `.pkl` files inside it.

    ```
    /your-project-root
        /models_store  <-- CREATE THIS
            diabetes.pkl
            heart.pkl
            liver.pkl
            mental_health.pkl
        /medml-backend 
        /frontend-src 
    ```

5.  **Configure Environment Variables:**
    Create a `.env` file in the `medml-backend` directory by copying the example.
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file and set `SECRET_KEY` and `JWT_SECRET_KEY` to any strong, random string.

6.  **Initialize and Upgrade the Database:**
    These commands will create your `medml.db` (SQLite) file and build the tables.
    ```bash
    flask db init     # Only if 'migrations' folder doesn't exist
    flask db migrate  # Creates the migration script
    flask db upgrade  # Applies the migration to the DB
    ```

7.  **Create Your First User (Admin/Doctor):**
    We will use the Flask shell to create the first user.
    ```bash
    flask shell
    ```
    In the Python shell that opens, run the following commands:
    ```python
    from app import db
    from app.models import User
    
    # --- Create your user ---
    u = User(username='admin', email='admin@clinic.com', role='admin')
    u.set_password('YourSecurePassword123')
    db.session.add(u)
    db.session.commit()
    
    print(f"User 'admin@clinic.com' created!")
    exit()
    ```

8.  **Run the Backend Server:**
    ```bash
    flask run
    ```
    The backend is now running at `http://127.0.0.1:5000`.

---

## 2. Frontend Setup (React)

1.  **Navigate to the Frontend Directory:**
    Open a **new terminal window** and navigate to the frontend `src` directory (or its parent, wherever `package.json` is).
    ```bash
    # From the project root
    cd frontend-src 
    ```

2.  **Install Node.js Dependencies:**
    ```bash
    npm install
    npm install axios # Install axios if not already in package.json
    ```

3.  **Configure API URL:**
    The frontend needs to know where the backend is.
    
    * **Option 1 (Quick):** Open `src/utils/apiClient.ts` and ensure the `API_BASE_URL` constant points to your backend:
        ```typescript
        const API_BASE_URL = '[http://127.0.0.1:5000/api/v1](http://127.0.0.1:5000/api/v1)';
        ```
    * **Option 2 (Recommended):** Create a `.env.local` file in the `frontend-src` directory and add the following line:
        ```
        VITE_API_BASE_URL=[http://127.0.0.1:5000/api/v1](http://127.0.0.1:5000/api/v1)
        ```
        Then, update `src/utils/apiClient.ts` to use it:
        ```typescript
        const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '[http://127.0.0.1:5000/api/v1](http://127.0.0.1:5000/api/v1)';
        ```

4.  **Run the Frontend Dev Server:**
    ```bash
    npm run dev
    ```
    The frontend is now running, typically at `http://localhost:5173`.

---

## 3. Test Plan & Verification

You now have a fully runnable system.

1.  **Open the App:** Open `http://localhost:5173` in your browser. You should see the "Sign In" page.
2.  **Log In:** Use the credentials you created in the Flask shell (e.g., `admin@clinic.com` and `YourSecurePassword123`).
3.  **View Dashboard:** Upon success, you will be redirected to the "Healthcare Worker Dashboard".
4.  **Add a Patient:**
    * Click "Add New User" (this is the "Add Patient" button).
    * Fill in the form (e.g., Name: "John Doe", DOB: "1980-01-01", Gender: "Male").
    * Click "Save Patient". You should be returned to the dashboard.
5.  **View Patient List:**
    * Click "View Registered Patients".
    * You should see "John Doe" in the list.
    * Click the "View" button for John Doe.
6.  **Run an Assessment:**
    * You are now on the Patient Detail View. Click "Run New Assessment".
    * Select "Diabetes".
    * Fill in the `DiabetesAssessmentForm` with the sample data from Batch 1.
        * `Pregnancies`: 6, `Glucose`: 148, `BloodPressure`: 72, `SkinThickness`: 35, `Insulin`: 0, `BMI`: 33.6, `DiabetesPedigreeFunction`: 0.627, `Age`: 50
    * Click "Save Assessment".
7.  **Verify Result:**
    * You will be returned to the Patient Detail View.
    * The "Disease Risk Assessment Results" card for **Diabetes** should now be updated, showing a "High" or "Medium" risk level.
    * The "Most Recent Assessment Data" card should show the input data you just entered.
8.  **Test Stateless Prediction:**
    * *(Optional - Use Postman/Insomnia)*
    * Send a `POST` request to `http://127.0.0.1:5000/api/v1/predict/heart` with the sample JSON payload for heart disease.
    * You should receive a `200 OK` response with the prediction, without needing a JWT token.