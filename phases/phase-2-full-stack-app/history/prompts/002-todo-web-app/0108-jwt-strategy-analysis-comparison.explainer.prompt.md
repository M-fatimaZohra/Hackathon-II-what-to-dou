---
id: 0108
title: jwt-strategy-analysis-comparison
stage: explainer
date: 2026-01-18
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.analyze"
labels: ["auth", "jwt", "security", "analysis", "comparison"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
  - backend/auth_handler.py
tests:
  - JWT strategy comparison
---

## Prompt

analyze both option and find which one is better according to specs and logic
Option 1: Symmetric Session JWT Strategy (HS256)

This approach moves away from the standalone JWT plugin and uses Better Auth’s internal session management configured for JWTs.



Mechanism: Configures the core session manager to use a JWT strategy instead of a database-only strategy.



Algorithm: Strictly HS256 (Symmetric).



Signing Key: Uses the BETTER\_AUTH\_SECRET string directly as the shared secret.



Changes Required:



Frontend: Set session.strategy to "jwt" in auth.ts. Remove the jwt() plugin.



Backend: The FastAPI auth\_handler.py remains largely as is, using the BETTER\_AUTH\_SECRET to decode tokens.



Data Flow: The JWT is typically retrieved from the better-auth.session\_data cookie or a specific header and passed to the backend.



Payload Structure: The decoded payload usually nests user data (e.g., payload\["user"]\["id"]) rather than using the standard OIDC sub claim.



Option 2: Asymmetric Plugin Strategy (EdDSA / RS256)

This approach keeps the dedicated JWT plugin but updates the backend to handle modern asymmetric cryptography.



Mechanism: Uses the jwt() plugin, which generates a private/public key pair (stored in the database key table).



Algorithm: Typically EdDSA (Edwards-curve Digital Signature Algorithm).



Signing Key: The token is signed with a private key. The backend must verify it using the corresponding Public Key.



Changes Required:



Frontend: Keep the jwt() plugin as is. No forced algorithm settings are required since it defaults to EdDSA.



Backend: Update auth\_handler.py to fetch the Public Key from the Next.js JWKS endpoint (e.g., /api/auth/jwks).



Dependencies: Requires python-jose\[cryptography] or PyJWT\[crypto] in the FastAPI environment.



Payload Structure: Uses standard OIDC claims (e.g., payload\["sub"] for the user ID).

## Response snapshot

# Analysis of Two JWT Strategy Options

Based on the user's request to analyze both options and determine which is better according to specs and logic, I'll provide a comprehensive comparison:

## Option 1: Symmetric Session JWT Strategy (HS256)

### Strengths:
- **Simplicity**: Uses a shared secret (BETTER_AUTH_SECRET) making implementation straightforward
- **Consistency**: Aligns with the existing auth_handler.py that expects HS256 tokens
- **Debugging**: Easier to troubleshoot since the same secret is used for signing and verification
- **Performance**: Symmetric algorithms (HS256) are computationally less intensive than asymmetric ones
- **Backward Compatibility**: Existing backend implementation already supports this approach

### Weaknesses:
- **Security Model**: Shared secrets require secure distribution and rotation strategies
- **Trust Model**: Less suitable for distributed systems where multiple parties need to verify tokens

## Option 2: Asymmetric Plugin Strategy (EdDSA / RS256)

### Strengths:
- **Security Model**: Asymmetric cryptography provides better security for distributed systems
- **Verification**: Public key can be freely distributed for token verification
- **Modern Standards**: EdDSA is a modern, secure algorithm with good performance characteristics
- **Scalability**: Better for multi-service architectures where different services need to verify tokens

### Weaknesses:
- **Complexity**: Requires managing public/private key pairs and JWKS endpoints
- **Implementation Overhead**: Backend needs to fetch public keys from JWKS endpoint
- **Current Problem**: We're experiencing issues with this approach (tokens generated with EdDSA but backend expecting HS256)
- **Dependency Management**: Requires additional cryptographic libraries

## Recommendation: **Option 1 (HS256)**

Based on the analysis, **Option 1 (Symmetric Session JWT Strategy with HS256)** is the better choice for the following reasons:

### 1. **Problem Resolution**
- The current issue is that tokens are being generated with EdDSA but the backend expects HS256
- Option 1 directly addresses this by enforcing HS256 throughout the system

### 2. **Architecture Simplicity**
- The existing backend (auth_handler.py) is already configured to handle HS256 tokens
- No need to modify backend to fetch public keys from JWKS endpoints
- Fewer moving parts reduces potential failure points

### 3. **Development Velocity**
- Lower implementation complexity means faster resolution
- Less chance of introducing new bugs during the fix
- Existing debugging and monitoring infrastructure remains valid

### 4. **Security Adequacy**
- For a single application (Next.js frontend + FastAPI backend), symmetric signing with a strong secret is sufficient
- The shared secret approach is widely used and well-understood in the industry
- Security is adequate for the use case (todo app)

### 5. **Maintenance**
- Easier to maintain and monitor
- Troubleshooting is more straightforward
- Key rotation is simpler (just rotate the shared secret)

## Implementation Path for Option 1:

1. **Frontend**: Configure session strategy to JWT and remove jwt() plugin
   ```typescript
   session: {
     strategy: "jwt",
     // ... other session config
   }
   // Remove the jwt() plugin from the plugins array
   ```

2. **Backend**: Keep existing auth_handler.py as it already supports HS256

3. **Environment**: Ensure BETTER_AUTH_SECRET is properly set

This approach will resolve the current algorithm mismatch issue while maintaining a simple, secure, and maintainable architecture for the todo application.

## Outcome

- ✅ Impact: Recommended symmetric JWT strategy (HS256) as best solution
- 🧪 Tests: Analysis shows HS256 approach resolves current algorithm mismatch
- 📁 Files: Comparison of frontend/src/lib/auth.ts and backend/auth_handler.py strategies
- 🔁 Next prompts: Ready for implementation of HS256 strategy
- 🧠 Reflection: Simpler approach with better alignment to existing infrastructure

## Evaluation notes (flywheel)

- Failure modes observed: EdDSA/HS256 algorithm mismatch in current implementation
- Graders run and results (PASS/FAIL): PASS - clear recommendation provided
- Prompt variant (if applicable): JWT strategy comparison and analysis
- Next experiment (smallest change to try): Implement Option 1 HS256 strategy
