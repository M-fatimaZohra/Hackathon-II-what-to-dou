/**
 * Environment Configuration
 *
 * Dynamically configures API endpoints and security settings based on NEXT_PUBLIC_MOD.
 * - developer: Local development with relaxed security
 * - production: Production with strict security
 */

const MOD = process.env.NEXT_PUBLIC_MOD || 'production';
export const IS_DEV = MOD === 'developer';

export interface ConfigType {
  API_BASE_URL: string;
  AUTH_BASE_URL: string;
  COOKIE_SECURE: boolean;
  HTTP_ONLY_TOKEN: boolean;
  REFRESH_CACHE: boolean;
}

export const CONFIG: ConfigType = {
  // API Base URL - used for all backend API calls
  // Development: Always use localhost with /api suffix
  // Production: Use environment variable (must be set)
  API_BASE_URL: IS_DEV
    ? 'http://localhost:7860/api'
    : process.env.NEXT_PUBLIC_API_URL!,

  // Auth Base URL - used for authentication redirects
  // Development: Always use localhost
  // Production: Use environment variable (must be set)
  AUTH_BASE_URL: IS_DEV
    ? 'http://localhost:3000'
    : process.env.NEXT_PUBLIC_BASE_URL!,

  // Cookie Security - enforce HTTPS in production
  COOKIE_SECURE: !IS_DEV,

  // HTTP Only Token - prevent JavaScript access to auth tokens
  HTTP_ONLY_TOKEN: !IS_DEV,

  // Refresh Cache - disable caching in development for fresh data
  REFRESH_CACHE: !IS_DEV,
};

// Validation: Ensure required environment variables are set
if (!process.env.NEXT_PUBLIC_MOD && !IS_DEV) {
  console.warn(
    'NEXT_PUBLIC_MOD not set, defaulting to production mode. Set NEXT_PUBLIC_MOD=developer for development.'
  );
}

export default CONFIG;
