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
      // The interceptor will handle refresh, but if /me fails *after* refresh,
      // we log out.
      logout(); // Clear state
      return null;
    }
  };

  /**
   * Handles user logout.
   */
  const logout = () => {
    const accessToken = localStorage.getItem('authToken');
    if (accessToken) {
        // Inform the backend to blocklist the token
        apiClient.post('/auth/logout').catch(err => {
            console.error("Logout API call failed", err);
        });
    }
    localStorage.removeItem('authToken');
    localStorage.removeItem('refreshToken'); // <-- ADDED
    setToken(null);
    setUser(null);
    setRole(null);
    setIsAuthenticated(false);
    delete apiClient.defaults.headers.common['Authorization'];
  };


  /**
   * Runs on app startup. Checks for an existing token and validates it.
   */
  useEffect(() => {
    const validateToken = async () => {
      const storedAccessToken = localStorage.getItem('authToken');
      const storedRefreshToken = localStorage.getItem('refreshToken');

      if (storedAccessToken) {
        try {
          const decoded: JwtPayload = jwtDecode(storedAccessToken);
          if (decoded.exp * 1000 > Date.now()) {
            setToken(storedAccessToken);
            await fetchUserProfile();
          } else {
            // Access token expired, interceptor will handle refresh on next API call
            console.log("Access token expired, will refresh on next call.");
          }
        } catch (e) {
          console.error("Invalid access token", e);
          // Token is invalid, try to refresh
        }
      } else if (storedRefreshToken) {
        // --- FIX: Proactively refresh if no access token but refresh token exists ---
        try {
          console.log("No access token, attempting refresh...");
          const { data } = await apiClient.post(
            '/auth/refresh',
            {},
            { headers: { 'Authorization': `Bearer ${storedRefreshToken}` } }
          );
          localStorage.setItem('authToken', data.access_token);
          localStorage.setItem('refreshToken', data.refresh_token);
          setToken(data.access_token);
          await fetchUserProfile(); // Now fetch profile with new token
        } catch (error) {
          console.error("Startup refresh failed", error);
          logout(); // Refresh failed, clear everything
        }
      }
      
      setLoading(false);
    };

    validateToken();

    // --- ADDED: Listen for logout event from apiClient interceptor ---
    const handleLogoutEvent = () => {
        console.warn("Received auth-logout event. Logging out.");
        logout();
    };
    window.addEventListener('auth-logout', handleLogoutEvent);
    return () => {
        window.removeEventListener('auth-logout', handleLogoutEvent);
    };
    // --- End of Add ---

  }, []);

  /**
   * Handles Admin login.
   */
  const adminLogin = async (payload: AdminLoginPayload) => {
    const { data } = await apiClient.post('/auth/admin/login', payload);
    const { access_token, refresh_token } = data;
    
    localStorage.setItem('authToken', access_token);
    localStorage.setItem('refreshToken', refresh_token); // <-- ADDED
    setToken(access_token);
    
    // Set header for immediate use
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

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
    const { access_token, refresh_token } = data;

    localStorage.setItem('authToken', access_token);
    localStorage.setItem('refreshToken', refresh_token); // <-- ADDED
    setToken(access_token);

    // Set header for immediate use
    apiClient.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
    
    const decoded: JwtPayload = jwtDecode(access_token);
    setRole(decoded.sub.role);

    await fetchUserProfile(); // Fetch and set user data
    setIsAuthenticated(true);
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