import { signIn } from '@/lib/actions/auth-action';
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { email, password } = await request.json();

    // Call the server action
    const result = await signIn(email, password);

    if ('error' in result && result.error) {
      return Response.json({ error: result.error.message || 'Sign in failed' }, { status: 400 });
    }

    return Response.json({ success: true });
  } catch (error) {
    return Response.json({ error: 'Failed to sign in' }, { status: 500 });
  }
}