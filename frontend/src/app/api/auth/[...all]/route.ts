import { toNextJsHandler } from 'better-auth/next-js';
import { auth } from '@/lib/auth';

// Export GET and POST methods using toNextJsHandler
export const { GET, POST } = toNextJsHandler(auth);