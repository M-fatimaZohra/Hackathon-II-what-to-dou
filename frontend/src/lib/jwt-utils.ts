/**
 * JWT Utility Functions
 *
 * Shared utilities for extracting and validating JWT tokens from Better Auth cookies.
 * Used by both apiClient and ChatProvider to ensure consistent authentication.
 */

/**
 * Extracts JWT token from Better Auth cookies and validates HS256 algorithm.
 *
 * Checks for cookies in this order:
 * 1. __Secure-better-auth.session_data (production)
 * 2. better-auth.session_data (development)
 * 3. __Secure-better-auth.session_token (production fallback)
 * 4. better-auth.session_token (development fallback)
 *
 * @returns JWT token string if found and valid, null otherwise
 */
export function getJwtTokenFromCookie(): string | null {
  if (typeof document === 'undefined') {
    // Not in browser context (SSR)
    return null;
  }

  // Extract JWT token - check for both production (__Secure-) and development cookie names
  const cookies = document.cookie.split(';');

  // Define the cookie name patterns to check in order of preference
  const cookiePatterns = [
    '__Secure-better-auth.session_data=',  // Production secure session_data
    'better-auth.session_data=',           // Development session_data
    '__Secure-better-auth.session_token=', // Production secure session_token
    'better-auth.session_token='           // Development session_token
  ];

  for (let cookie of cookies) {
    cookie = cookie.trim();

    // Check if this cookie matches any of our target patterns
    for (const pattern of cookiePatterns) {
      if (cookie.startsWith(pattern)) {
        // Extract the cookie value after the equals sign
        const cookieValue = cookie.substring(pattern.length);

        let token = cookieValue;

        // Decode the token if it's URL-encoded
        try {
          token = decodeURIComponent(token);
        } catch (e) {
          continue; // Try next cookie
        }

        // Implement validation: verify if it is a 3-part string (split by dots)
        const parts = token.split('.');
        if (parts.length !== 3) {
          continue; // Try next cookie
        }

        // If it has 3 parts, decode the header (handling Base64URL characters - and _) and check if alg === "HS256"
        try {
          let headerPart = parts[0];
          // Handle Base64URL encoding by converting to Base64
          headerPart = headerPart.replace(/-/g, '+').replace(/_/g, '/');

          // Add padding if needed for base64 decoding
          let headerPadded = headerPart;
          while (headerPadded.length % 4 !== 0) {
            headerPadded += '=';
          }

          const headerJson = atob(headerPadded);
          const header = JSON.parse(headerJson);

          // Check if alg === "HS256" - remove strict checks for the typ header field as it may be undefined
          if (header.alg === 'HS256') {
            return token; // Return the token that satisfies the HS256 requirement
          } else {
            continue; // Try next cookie
          }
        } catch (e) {
          continue; // Try next cookie
        }
      }
    }
  }

  return null;
}
