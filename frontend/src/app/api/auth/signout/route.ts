import { auth } from '@/lib/auth';
import { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    await auth.api.signOut({
      headers: request.headers,
    });

    return Response.json({ success: true });
  } catch (error) {
    return Response.json({ error: 'Failed to sign out' }, { status: 500 });
  }
}