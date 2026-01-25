'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { authClient } from '@/lib/auth-client';

export default function SignInPage() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const { data, error: signInError } = await authClient.signIn.email({
        email,
        password,
        callbackURL: "/tasks",
      });

      if (signInError) {
        setError(signInError.message || 'Sign in failed');
      } else if (data) {
        // Redirect to tasks page on successful signin
        router.push('/tasks');
      }
    } catch (err) {
      setError('An error occurred during sign in');
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#FFFBED] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-[#1B1C1C]">
            Sign in to your account
          </h2>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
              <span className="block sm:inline">{error}</span>
            </div>
          )}
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <label htmlFor="email" className="sr-only">Email address</label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-[#1B1C1C] border-opacity-30 placeholder-[#1B1C1C] text-[#1B1C1C] rounded-t-md focus:outline-none focus:ring-[#f2d16f] focus:border-[#f2d16f] focus:z-10 sm:text-sm"
                placeholder="Email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div className="mt-4">
              <label htmlFor="password" className="sr-only">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                className="appearance-none rounded-none relative block w-full px-3 py-2 border border-[#1B1C1C] border-opacity-30 placeholder-[#1B1C1C] text-[#1B1C1C] rounded-b-md focus:outline-none focus:ring-[#f2d16f] focus:border-[#f2d16f] focus:z-10 sm:text-sm"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-[#1B1C1C] bg-[#f2d16f] hover:bg-[#FFE9A8] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#f2d16f]"
            >
              Sign in
            </button>
          </div>
        </form>
        <div className="text-center">
          <Link
            href="/signup"
            className="font-medium text-[#1B1C1C] hover:text-[#f2d16f]"
          >
            Don't have an account? Sign up
          </Link>
        </div>
      </div>
    </div>
  );
}