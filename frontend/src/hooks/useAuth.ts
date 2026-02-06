// Custom hook for authentication state management
import { useState, useEffect, useCallback } from 'react';
import { AuthService } from '../services/authService';

interface UseAuthReturn {
  user: { user_id: string } | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: { email: string; password: string }) => Promise<boolean>;
  logout: () => void;
  refreshToken: () => Promise<boolean>;
}

export const useAuth = (): UseAuthReturn => {
  const [user, setUser] = useState<{ user_id: string } | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Check authentication status on mount and set up listener for changes
  useEffect(() => {
    const checkAuthStatus = () => {
      try {
        const authStatus = AuthService.isAuthenticated();
        setIsAuthenticated(authStatus);

        if (authStatus) {
          const currentUser = AuthService.getCurrentUser();
          setUser(currentUser);
        } else {
          setUser(null);
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
        setIsAuthenticated(false);
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };

    // Initial check
    checkAuthStatus();

    // Set up a timer to periodically check token validity (every 5 minutes)
    const interval = setInterval(() => {
      const token = AuthService.getToken();
      if (token) {
        try {
          const payload = parseJwtPayload(token);
          const currentTime = Math.floor(Date.now() / 1000);

          // If token expires in less than 5 minutes, try to refresh
          if (payload.exp && payload.exp - currentTime < 300) {
            refreshToken();
          }
        } catch (error) {
          console.error('Error checking token expiration:', error);
        }
      }
    }, 5 * 60 * 1000); // 5 minutes

    return () => clearInterval(interval);
  }, []);

  const login = useCallback(async (credentials: { email: string; password: string }): Promise<boolean> => {
    setIsLoading(true);
    try {
      // In a real implementation, this would call the Better Auth login endpoint
      // For now, we'll simulate a successful login
      // const response = await authService.login(credentials);
      // const token = response.token;

      // For simulation purposes, we'll assume login is successful
      // and set a mock token
      const mockToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjk5OTk5OTk5OTl9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c';

      AuthService.setToken(mockToken);

      const authStatus = AuthService.isAuthenticated();
      setIsAuthenticated(authStatus);

      if (authStatus) {
        const currentUser = AuthService.getCurrentUser();
        setUser(currentUser);
        return true;
      }

      return false;
    } catch (error) {
      console.error('Login error:', error);
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    AuthService.clearToken();
    setIsAuthenticated(false);
    setUser(null);
  }, []);

  const refreshToken = useCallback(async (): Promise<boolean> => {
    try {
      const success = await AuthService.refreshToken();
      if (success) {
        const authStatus = AuthService.isAuthenticated();
        setIsAuthenticated(authStatus);

        if (authStatus) {
          const currentUser = AuthService.getCurrentUser();
          setUser(currentUser);
        }
      }
      return success;
    } catch (error) {
      console.error('Refresh token error:', error);
      return false;
    }
  }, []);

  // Helper function to parse JWT payload
  const parseJwtPayload = (token: string): { [key: string]: any } => {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    return JSON.parse(jsonPayload);
  };

  const clearAuth = useCallback(() => {
    AuthService.clearToken();
    setIsAuthenticated(false);
    setUser(null);
  }, []);

  return {
    user,
    isAuthenticated,
    isLoading,
    login,
    logout: clearAuth,
    refreshToken
  };
};