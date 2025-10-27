// HealthCare App/src/App.tsx
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LoginPage from './components/auth/LoginPage';
import AdminDashboard from './components/admin/AdminDashboard';
import PatientDashboard from './components/patient/PatientDashboard';
import AppLayout from './components/layout/AppLayout';
import { Toaster } from './components/ui/sonner';

/**
 * Handles root-level routing logic
 * - If loading, show nothing (or a global spinner)
 * - If authenticated, redirect from '/' or '/login' to the correct dashboard
 * - If not authenticated, redirect from '/' to '/login'
 */
const AppRoutes = () => {
  const { isAuthenticated, role, loading } = useAuth();

  if (loading) {
    // Wait for auth check to complete before rendering routes
    return null; // Or a full-page loader
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={
          isAuthenticated ? (
            <Navigate to={role === 'admin' ? '/admin' : '/patient'} replace />
          ) : (
            <LoginPage />
          )
        }
      />

      {/* Admin Protected Routes */}
      <Route element={<ProtectedRoute requiredRole="admin" />}>
        <Route path="/admin/*" element={<AdminDashboard />} />
      </Route>
      
      {/* Patient Protected Routes */}
      <Route element={<ProtectedRoute requiredRole="patient" />}>
        <Route element={<AppLayout />}> {/* Patient dashboard uses the AppLayout */}
          <Route path="/patient" element={<PatientDashboard />} />
          {/* --- FIX: Add placeholder routes for other patient nav items --- */}
          {/* These routes are not in the MVP but are in the layout, preventing 404s if clicked. */}
          <Route path="/patient/profile" element={<div className="p-8"><h2>Patient Profile Page</h2><p>This feature is coming soon.</p></div>} />
          <Route path="/patient/appointments" element={<div className="p-8"><h2>My Appointments Page</h2><p>This feature is coming soon.</p></div>} />
          <Route path="/patient/reports" element={<div className="p-8"><h2>My Reports Page</h2><p>This feature is coming soon.</p></div>} />
        </Route>
      </Route>

      {/* --- FIX: Add explicit root path redirect --- */}
      <Route
        path="/"
        element={
          <Navigate 
            to={isAuthenticated ? (role === 'admin' ? '/admin' : '/patient') : '/login'} 
            replace 
          />
        }
      />

      {/* Root Redirect Logic (Catch-all for any other path) */}
      <Route
        path="*"
        element={
          <Navigate 
            to={isAuthenticated ? (role === 'admin' ? '/admin' : '/patient') : '/login'} 
            replace 
          />
        }
      />
    </Routes>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppRoutes />
        <Toaster />
      </Router>
    </AuthProvider>
  );
}

export default App;