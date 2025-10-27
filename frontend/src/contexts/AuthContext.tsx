// HealthCare App/src/contexts/AuthContext.tsx
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import apiClient from '../utils/apiClient';
import { AdminUser, PatientUser, AdminLoginPayload, PatientLoginPayload } from '../types';
import { jwtDecode } from 'jwt-decode'; // Added dependency: npm install jwt-decode

// Define the shape of the JWT payload
interface JwtPayload {
  sub: {
    id: number;
    role: 'admin' | 'patient';
  };
  exp: number;
}

// Define the context state
interface AuthContextType {
  isAuthenticated: boolean;
  user: AdminUser | PatientUser | null;
  role: 'admin' | 'patient' | null;
  loading: boolean;
  token: string | null;
  adminLogin: (payload: AdminLoginPayload) => Promise<void>;
  patientLogin: (payload: PatientLoginPayload) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<AdminUser | PatientUser | null>(null);
  const [role, setRole] = useState<'admin' | 'patient' | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('authToken'));
  const [loading, setLoading] = useState(true); // Start loading until auth is checked

  /**
   * Fetches the user's profile using the /auth/me endpoint.
   * This is called after a successful login or on initial app load if a token exists.
   */
  const fetchUserProfile = async () => {
    try {
      const { data } = await apiClient.get('/auth/me');
      setUser(data); // data is either AdminUser or PatientUser
      
      // Re-confirm role from the /me endpoint response
      const userRole = data.role || (data.abha_id ? 'patient' : 'admin');
      setRole(userRole);
      
      setIsAuthenticated(true);
      return userRole;
    } catch (error) {
      console.error('Failed to fetch user profile', error);
      // If /me fails, the token is invalid or expired
      logout();
      return null;
    }
  };

  /**
   * Runs on app startup. Checks for an existing token and validates it.
   */
  useEffect(() => {
    const validateToken = async () => {
      const storedToken = localStorage.getItem('authToken');
      if (storedToken) {
        try {
          // Check token expiration
          const decoded: JwtPayload = jwtDecode(storedToken);
          if (decoded.exp * 1000 > Date.now()) {
            setToken(storedToken);
            await fetchUserProfile();
          } else {
            // Token is expired
            logout();
          }
        } catch (error) {
          // Token is invalid
          console.error("Invalid token", error);
          logout();
        }
      }
      setLoading(false);
    };

    validateToken();
  }, []);

  /**
   * Handles Admin login.
   */
  const adminLogin = async (payload: AdminLoginPayload) => {
    const { data } = await apiClient.post('/auth/admin/login', payload);
    const { access_token } = data;
    
    localStorage.setItem('authToken', access_token);
    setToken(access_token);

    // Decode token to set role immediately for routing
    const decoded: JwtPayload = jwtDecode(access_token);
    setRole(decoded.sub.role);

    await fetchUserProfile(); // Fetch and set user data
    setIsAuthenticated(true);
  };

  /**
   * Handles Patient login.
   */
  const patientLogin = async (payload: PatientLoginPayload) => {
    const { data } = await apiClient.post('/auth/patient/login', payload);
    const { access_token } = data;

    localStorage.setItem('authToken', access_token);
    setToken(access_token);
    
    // Decode token to set role immediately for routing
    const decoded: JwtPayload = jwtDecode(access_token);
    setRole(decoded.sub.role);

    await fetchUserProfile(); // Fetch and set user data
    setIsAuthenticated(true);
  };

  /**
   * Handles user logout.
   */
  const logout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
    setUser(null);
    setRole(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        user,
        role,
        loading,
        token,
        adminLogin,
        patientLogin,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};