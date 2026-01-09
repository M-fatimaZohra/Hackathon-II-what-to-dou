'use server'

import { headers } from 'next/headers';
import { auth } from '../auth';

export const signUp = async (name: string, email: string, password: string) => {
  try {
    const result = await auth.api.signUpEmail({
      body: {
        name,
        email,
        password,
        callbackURL: '/tasks'
      },
      headers: await headers()
    });
    return result;
  } catch (error) {
    return { error: { message: error instanceof Error ? error.message : 'Sign up failed' } };
  }
};

export const signIn = async (email: string, password: string) => {
  try {
    const result = await auth.api.signInEmail({
      body: {
        email,
        password,
        callbackURL: '/tasks'
      },
      headers: await headers()
    });
    return result;
  } catch (error) {
    return { error: { message: error instanceof Error ? error.message : 'Sign in failed' } };
  }
};

export const logOut = async () => {
  const result = await auth.api.signOut({ headers: await headers() });
  return result;
};