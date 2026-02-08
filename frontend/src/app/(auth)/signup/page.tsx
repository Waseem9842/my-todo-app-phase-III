// Signup page component
// Provides a form for new users to create an account

'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/Card';
import { manualSignUp } from '@/lib/better-auth-client';

// Signup page component implementation
export default function SignupPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const router = useRouter();
  const { login } = useAuth();

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Additional client-side validation
    if (password.length > 72) {
      setError('Password cannot be longer than 72 characters. Please use a shorter password.');
      setLoading(false);
      return;
    }

    try {
      // Call the manual sign-up API
      const result = await manualSignUp(email, password, name);

      if (result?.token) {
        // Store the token in our auth context
        login(result.token);
        // Redirect to dashboard
        router.push('/dashboard');
        router.refresh();
      } else {
        setError('Signup successful but no token received');
      }
    } catch (err) {
      let errorMessage = err instanceof Error ? err.message : 'An error occurred during signup';
      
      // Provide more specific error message for password length
      if (errorMessage.includes('Password cannot be longer than 72 characters')) {
        errorMessage = 'Password cannot be longer than 72 characters. Please use a shorter password.';
      }
      
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl">Create an account</CardTitle>
        <CardDescription>
          Enter your information to create your account
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
              <span className="block sm:inline">{error}</span>
            </div>
          )}
          <div className="space-y-2">
            <label htmlFor="name" className="text-sm font-medium">Full Name</label>
            <Input
              id="name"
              type="text"
              placeholder="John Doe"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium">Email</label>
            <Input
              id="email"
              type="email"
              placeholder="name@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <label htmlFor="password" className="text-sm font-medium">Password</label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
              maxLength={72}
              placeholder="Enter your password (max 72 chars)"
            />
            <p className="text-xs text-gray-500">
              Password must be between 6 and 72 characters
            </p>
            {password.length > 66 && (
              <p className="text-xs text-yellow-600">
                Password approaching maximum length (72 characters)
              </p>
            )}
          </div>
        </CardContent>
        <CardFooter className="flex flex-col">
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Creating Account...' : 'Sign Up'}
          </Button>
          <p className="mt-4 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link href="/signin" className="font-medium text-primary hover:underline">
              Sign in
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  );
}