'use client';

import React, { useEffect } from 'react';
import { useAuth } from '@/providers/AuthProvider';
import { useRouter } from 'next/navigation';

export default function DashboardClientLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { user, loading } = useAuth();
  const router = useRouter();

  // Redirect to sign in if not authenticated
  useEffect(() => {
    if (!loading && (!user || !user.isAuthenticated)) {
      router.push('/signin');
    }
  }, [user, loading, router]);

  // Show loading state while checking auth
  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // If not authenticated, show nothing (will redirect via useEffect)
  if (!user || !user.isAuthenticated) {
    return null;
  }

  return <>{children}</>;
}
