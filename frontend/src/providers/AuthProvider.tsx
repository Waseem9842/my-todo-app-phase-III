// Auth Provider component
// Provides authentication context to the application

'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { storeToken, getToken, removeToken, getUserIdFromToken, isAuthenticated, decodeToken } from '@/lib/auth';

// Define the authentication context type
interface AuthContextType {
  user: {
    id: string | null;
    email: string | null;
    name: string | null;
    isAuthenticated: boolean;
  } | null;
  login: (token: string) => void;
  logout: () => void;
  loading: boolean;
}

// Create the authentication context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Auth Provider component props
interface AuthProviderProps {
  children: ReactNode;
}

// Auth Provider component implementation
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<{
    id: string | null;
    email: string | null;
    name: string | null;
    isAuthenticated: boolean;
  } | null>(null);
  const [loading, setLoading] = useState(true);

  // Check authentication status on initial load
  useEffect(() => {
    const checkAuth = async () => {
      try {
        if (isAuthenticated()) {
          const token = getToken();
          const decodedToken = decodeToken(token);

          setUser({
            id: decodedToken?.sub || decodedToken?.user_id || decodedToken?.id || null,
            email: decodedToken?.email || null,
            name: decodedToken?.name || decodedToken?.user_name || null,
            isAuthenticated: true
          });
        } else {
          setUser({
            id: null,
            email: null,
            name: null,
            isAuthenticated: false
          });
        }
      } catch (error) {
        console.error('Error checking authentication status:', error);
        setUser({
          id: null,
          email: null,
          name: null,
          isAuthenticated: false
        });
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  // Login function
  const login = (token: string) => {
    // Store the token
    storeToken(token);

    // Update user state with details from token
    const decodedToken = decodeToken(token);

    setUser({
      id: decodedToken?.sub || decodedToken?.user_id || decodedToken?.id || null,
      email: decodedToken?.email || null,
      name: decodedToken?.name || decodedToken?.user_name || null,
      isAuthenticated: true
    });
  };

  // Logout function
  const logout = () => {
    // Remove the token
    removeToken();

    // Update user state
    setUser({
      id: null,
      email: null,
      name: null,
      isAuthenticated: false
    });
  };

  // Value to provide through context
  const value = {
    user,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};