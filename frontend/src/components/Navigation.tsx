'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { Inter, Satisfy } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

const satisfy = Satisfy({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

interface User {
  id: string;
  email: string;
  name: string;
}

export default function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Check if user is logged in on initial load
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const response = await fetch('/api/auth/session');
        if (response.ok) {
          const userData = await response.json();
          if (userData?.user) {
            setUser({
              id: userData.user.id,
              email: userData.user.email,
              name: userData.user.name || userData.user.email.split('@')[0]
            });
          }
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const handleSignOut = async () => {
    try {
      const response = await fetch('/api/auth/signout', {
        method: 'POST',
      });

      if (response.ok) {
        setUser(null);
        window.location.href = '/';
      }
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  if (loading) {
    return (
      <nav className="bg-[#FFFBED] shadow-md fixed w-full top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <Link href="/" className="text-3xl font-bold text-[#1B1C1C]" style={satisfy.style}>
                What to Dou
              </Link>
            </div>
            <div className="flex items-center">
              <span className="text-[#1B1C1C]">Loading...</span>
            </div>
          </div>
        </div>
      </nav>
    );
  }

  return (
    <nav className="bg-[#FFFBED] shadow-md fixed w-full top-0 z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="text-3xl font-bold text-[#1B1C1C]" style={satisfy.style}>
              What to Dou
            </Link>
            <div className="hidden md:ml-10 md:flex md:space-x-8">
              <Link
                href="/"
                className="text-[#1B1C1C] hover:text-[#1B1C1C] px-3 py-2 rounded-md text-sm font-medium"
                style={inter.style}
              >
                Home
              </Link>
              <Link
                href="/tasks"
                className="text-[#1B1C1C] hover:text-[#1B1C1C] px-3 py-2 rounded-md text-sm font-medium"
                style={inter.style}
              >
                My Tasks
              </Link>
            </div>
          </div>
          <div className="flex items-center md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              className="text-[#1B1C1C] hover:text-[#1B1C1C] p-2"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                {isOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
          <div className="hidden md:flex md:items-center">
            {user ? (
              // User is logged in - show profile dropdown
              <div className="relative">
                <button
                  className="flex items-center space-x-2 px-4 py-2 bg-[#f2d16f] text-[#1B1C1C] rounded-md hover:bg-[#FFE9A8] text-sm font-medium"
                  style={inter.style}
                >
                  <span>{user.name}</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </button>

                {/* Dropdown menu */}
                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50">
                  <div className="px-4 py-2 border-b">
                    <p className="text-sm font-medium text-[#1B1C1C]">{user.name}</p>
                    <p className="text-xs text-gray-500 truncate">{user.email}</p>
                  </div>
                  <div className="py-1">
                    <Link
                      href="/tasks"
                      className="block px-4 py-2 text-sm text-[#1B1C1C] hover:bg-[#FFE9A8]"
                      style={inter.style}
                    >
                      My Tasks
                    </Link>
                    <button
                      onClick={handleSignOut}
                      className="w-full text-left px-4 py-2 text-sm text-[#1B1C1C] hover:bg-[#FFE9A8]"
                      style={inter.style}
                    >
                      Sign out
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              // User is not logged in - show sign in/up buttons
              <div className="flex space-x-4">
                <Link
                  href="/signin"
                  className="px-4 py-2 text-[#1B1C1C] hover:bg-[#FFE9A8] rounded-md text-sm font-medium"
                  style={inter.style}
                >
                  Sign In
                </Link>
                <Link
                  href="/signup"
                  className="px-4 py-2 bg-[#f2d16f] text-[#1B1C1C] rounded-md hover:bg-[#FFE9A8] text-sm font-medium"
                  style={inter.style}
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Mobile menu */}
        {isOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              <Link
                href="/"
                className="text-[#1B1C1C] hover:text-[#1B1C1C] block px-3 py-2 rounded-md text-base font-medium"
                style={inter.style}
                onClick={() => setIsOpen(false)}
              >
                Home
              </Link>
              <Link
                href="/tasks"
                className="text-[#1B1C1C] hover:text-[#1B1C1C] block px-3 py-2 rounded-md text-base font-medium"
                style={inter.style}
                onClick={() => setIsOpen(false)}
              >
                My Tasks
              </Link>

              {user ? (
                <>
                  <div className="border-t border-gray-200 pt-2">
                    <div className="px-4 py-2 border-b">
                      <p className="text-sm font-medium text-[#1B1C1C]">{user.name}</p>
                      <p className="text-xs text-gray-500 truncate">{user.email}</p>
                    </div>
                    <Link
                      href="/tasks"
                      className="text-[#1B1C1C] hover:text-[#1B1C1C] block px-3 py-2 rounded-md text-base font-medium"
                      style={inter.style}
                      onClick={() => setIsOpen(false)}
                    >
                      My Tasks
                    </Link>
                    <button
                      onClick={() => {
                        handleSignOut();
                        setIsOpen(false);
                      }}
                      className="w-full text-left text-[#1B1C1C] hover:text-[#1B1C1C] block px-3 py-2 rounded-md text-base font-medium"
                      style={inter.style}
                    >
                      Sign out
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <Link
                    href="/signin"
                    className="text-[#1B1C1C] hover:text-[#1B1C1C] block px-3 py-2 rounded-md text-base font-medium"
                    style={inter.style}
                    onClick={() => setIsOpen(false)}
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/signup"
                    className="text-[#1B1C1C] hover:text-[#1B1C1C] block px-3 py-2 rounded-md text-base font-medium"
                    style={inter.style}
                    onClick={() => setIsOpen(false)}
                  >
                    Sign Up
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
}