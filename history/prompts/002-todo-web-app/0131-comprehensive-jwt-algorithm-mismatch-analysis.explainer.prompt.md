---
id: 0131
title: comprehensive-jwt-algorithm-mismatch-analysis
stage: explainer
date: 2026-01-19
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["auth", "jwt", "debug", "analysis", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - analysis only
tests:
  - JWT algorithm mismatch analysis
  - Connection termination analysis
---

## Prompt

Analyze the connection termination and JWT algorithm mismatch issues in the authentication system and provide a comprehensive report on the problems and solutions.

## Response snapshot

Comprehensive Analysis of Connection Termination and JWT Algorithm Issues:

### 1. Connection Termination Errors
The "Connection terminated unexpectedly" errors are occurring in the PostgreSQL client connection pool. This is likely due to:
- Database connection timeouts
- Pool exhaustion
- Network instability between the application and the database

### 2. JWT Algorithm Mismatch (Critical Issue)
The logs clearly show the core problem:
```
DEBUG: Token received, attempting decode...
DEBUG: JWT Decode Failed: The specified alg value is not allowed
```

This confirms the JWT token is using the EdDSA algorithm (as seen in previous analysis), but the backend Python handler is configured to only allow specific algorithms (likely HS256) and rejects EdDSA tokens.

### 3. Why Better Auth is Not Using HS256 Strategy

Despite configuration attempts, Better Auth is still generating EdDSA tokens instead of HS256. Here are the possible reasons:

**Minor Possibilities:**
1. **Configuration Override**: Another part of auth.ts configuration might be overriding JWT algorithm settings
2. **Better Auth Version**: Different versions of Better Auth may have different default behaviors
3. **Plugin Loading Order**: The JWT plugin might not be loaded in the correct order
4. **Environment Variables**: Missing or incorrect BETTER_AUTH_SECRET might cause fallback to default algorithm

**Major Possibilities:**
1. **Incorrect Plugin Configuration**: The JWT plugin might not be configured properly to enforce HS256
2. **Backend Verification Mismatch**: Python backend's JWT verification is rejecting EdDSA tokens
3. **Session Strategy Conflict**: The session strategy might be overriding JWT plugin settings

### Solutions:

1. **Immediate Fix**: Update backend JWT verification to accept both EdDSA and HS256 algorithms
2. **Long-term Fix**: Identify why Better Auth isn't respecting HS256 configuration and fix it
3. **Security Consideration**: EdDSA is actually more secure than HS256, so consider if this algorithm mismatch is really a problem or just an assumption about the required algorithm

The authentication flow is failing because the frontend generates an EdDSA token but the backend only accepts HS256, causing all API requests to return 401 Unauthorized.

## Outcome

- 🔍 Analysis: Identified JWT algorithm mismatch as root cause
- 📁 Files: None modified - analysis only
- 🧪 Tests: Algorithm mismatch diagnosis
- 🧠 Issue: Frontend/backend algorithm configuration inconsistency

## Evaluation notes (flywheel)

- Failure modes observed: Algorithm mismatch between frontend token generation and backend verification
- Graders run and results (PASS/FAIL): N/A - analysis only
- Prompt variant (if applicable): Comprehensive analysis prompt
- Next experiment (smallest change to try): Update backend to accept both algorithms