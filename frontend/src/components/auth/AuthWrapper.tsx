// Component to wrap protected routes with authentication check
'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AuthService } from '../../services/authService';

interface AuthWrapperProps {
  children: React.ReactNode;
  redirectPath?: string; // Path to redirect to if not authenticated (default: '/login')
}

export const AuthWrapper: React.FC<AuthWrapperProps> = ({
  children,
  redirectPath = '/signin'
}) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null); // null = checking
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const authStatus = AuthService.isAuthenticated();
        setIsAuthenticated(authStatus);

        if (!authStatus) {
          // Redirect to login if not authenticated
          router.push(redirectPath);
        }
      } catch (error) {
        console.error('Error checking authentication status:', error);
        setIsAuthenticated(false);
        router.push(redirectPath);
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, []); // Empty dependency array to run only once on mount

  // While checking authentication, show loading indicator
  if (isAuthenticated === null || isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // If not authenticated, return null since we redirected
  if (!isAuthenticated) {
    return null;
  }

  // If authenticated, render children
  return <>{children}</>;
};