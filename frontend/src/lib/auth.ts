import { betterAuth } from "better-auth";
import { Pool } from "pg";

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
      refreshCache: true,
    },
  },
  baseURL: process.env.NEXT_PUBLIC_BASE_URL!, // Use environment variable for base URL
  trustedOrigins: [process.env.NEXT_PUBLIC_BASE_URL!], // Use environment variable for trusted origins
  plugins: [],
  advanced: {
    cookies: {
      session_token: {
        attributes: {
          httpOnly: true,
          secure: true,
          sameSite: "lax",
          path: "/",
        },
      },
      session_data: {
        attributes: {
          httpOnly: false, // Changed to false to allow JWT extraction by ApiClient for cross-domain requests
          secure: true,
          sameSite: "lax",
          path: "/",
        },
      },
    },
  },
});