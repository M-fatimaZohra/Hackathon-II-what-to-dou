import { auth } from '@/lib/auth';
import { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (session) {
      return Response.json({
        user: {
          id: session.user.id,
          email: session.user.email,
          name: session.user.name,
        }
      });
    } else {
      return Response.json({ user: null }, { status: 401 });
    }
  } catch (error) {
    return Response.json({ error: 'Failed to get session' }, { status: 500 });
  }
}