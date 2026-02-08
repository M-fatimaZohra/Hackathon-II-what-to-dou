import { createAuthClient } from "better-auth/react";
import { CONFIG } from "@/lib/config";

// Create auth client for browser environment
// Points to the base URL of the Next.js app for session token access
export const authClient = createAuthClient({
  baseURL: CONFIG.AUTH_BASE_URL,
  // Minimal configuration without jwtClient plugin to avoid EdDSA algorithm
});


// Export individual functions for easier use in components
export const { signIn, signUp, signOut, useSession } = authClient;