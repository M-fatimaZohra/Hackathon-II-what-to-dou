import { betterAuth } from "better-auth";
import { Pool } from "pg";
import { CONFIG } from "@/lib/config";

// Create a more optimized database pool configuration
const dbPool = new Pool({
  connectionString: process.env.DATABASE_URL,
  // Optimize connection pooling for better performance
  max: 20, // Maximum number of clients in the pool
  min: 5,  // Minimum number of clients in the pool
  idleTimeoutMillis: 30000, // Close idle clients after 30 seconds
  connectionTimeoutMillis: 10000, // Return an error after 10 seconds if connection could not be established
  maxUses: 750, // Close (and replace) a connection after this many uses
  allowExitOnIdle: true, // Allow this pool to be garbage collected when idle
});

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET!,
  database: dbPool,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  session: {
    expiresIn: 604800, // 7 days in seconds
    cookieCache: {
      enabled: true,
      strategy: "jwt", // This ensures HS256 JWT tokens are generated
      maxAge: 60 * 60 * 24 * 7, // 7 days
      httpOnly: false, // Changed to false to allow JWT extraction by ApiClient for cross-domain requests
      refreshCache: CONFIG.REFRESH_CACHE, // Use CONFIG for cache refresh setting
    },
  },
  baseURL: CONFIG.AUTH_BASE_URL, // Use CONFIG for base URL (respects IS_DEV)
  trustedOrigins: [CONFIG.AUTH_BASE_URL], // Use CONFIG for trusted origins (respects IS_DEV)
  plugins: [],
  advanced: {
    cookies: {
      session_token: {
        attributes: {
          httpOnly: CONFIG.HTTP_ONLY_TOKEN, // Use CONFIG for httpOnly (false in dev for debugging, true in prod)
          secure: CONFIG.COOKIE_SECURE, // Use CONFIG for secure flag (false in dev, true in prod)
          sameSite: "lax",
          path: "/",
        },
      },
      session_data: {
        attributes: {
          httpOnly: false, // Always false to allow JWT extraction by ApiClient for cross-domain requests
          secure: CONFIG.COOKIE_SECURE, // Use CONFIG for secure flag (false in dev, true in prod)
          sameSite: "lax",
          path: "/",
        },
      },
    },
  },
});