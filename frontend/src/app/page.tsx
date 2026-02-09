// Root page component
// Landing page for the Todo application that redirects authenticated users to dashboard
// and unauthenticated users to the sign-in page

'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';
import Link from 'next/link';

export default function HomePage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  // Redirect based on authentication status
  useEffect(() => {
    if (!loading) {
      if (user?.isAuthenticated) {
        router.push('/dashboard');
      } else {
        router.push('/signin');
      }
    }
  }, [user, loading, router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-purple-100">
      <div className="flex flex-col items-center justify-center min-h-screen py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <div className="mx-auto h-16 w-16 rounded-full bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h1 className="mt-4 text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
              Todo App
            </h1>
            <p className="mt-2 text-lg text-gray-600">
              Manage your tasks efficiently
            </p>
          </div>
          <div className="mt-8 bg-white rounded-2xl shadow-xl p-8 text-center border border-gray-100">
            {loading ? (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
              </div>
            ) : (
              <div className="space-y-6">
                <p className="text-gray-600 text-lg">
                  {user?.isAuthenticated
                    ? "Redirecting to dashboard..."
                    : "Get started with our task management platform"}
                </p>
                
                <div className="mt-8">
                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Link
                      href="/signup"
                      className="px-6 py-3 bg-gradient-to-r from-indigo-600 to-indigo-700 text-white font-medium rounded-xl shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    >
                      Create Account
                    </Link>
                    <Link
                      href="/signin"
                      className="px-6 py-3 bg-white text-gray-800 font-medium rounded-xl border border-gray-300 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200"
                    >
                      Sign In
                    </Link>
                  </div>
                  
                  <div className="mt-6 text-sm text-gray-500">
                    <p>By signing up, you agree to our Terms of Service and Privacy Policy</p>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          <div className="mt-8 text-center text-sm text-gray-500">
            <p>Designed and developed by Muhammad Waseem</p>
          </div>
        </div>
      </div>
    </div>
  );
}