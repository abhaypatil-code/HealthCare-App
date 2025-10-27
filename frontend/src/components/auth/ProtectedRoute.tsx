// HealthCare App/src/components/auth/ProtectedRoute.tsx
import React from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Skeleton } from '../ui/skeleton'; // For loading state

interface ProtectedRouteProps {
  requiredRole: 'admin' | 'patient';
}

/**
 * Protects routes based on authentication status and user role.
 */
const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ requiredRole }) => {
  const { isAuthenticated, role, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    // Show a loading skeleton while auth state is being verified
    return (
      <div className="flex flex-col space-y-3 p-8">
        <Skeleton className="h-[125px] w-full rounded-xl" />
        <div className="space-y-2">
          <Skeleton className="h-4 w-full" />
          <Skeleton className="h-4 w-4/5" />
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    // User is not logged in, redirect to login page
    // Pass the original location to redirect back after login
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (role !== requiredRole) {
    // User is logged in, but has the wrong role.
    // Redirect them to their correct dashboard.
    const redirectTo = role === 'admin' ? '/admin' : '/patient';
    return <Navigate to={redirectTo} replace />;
  }

  // User is authenticated and has the correct role, render the child routes
  return <Outlet />;
};

export default ProtectedRoute;