---
id: 0106
title: jwt-token-analysis-eddsa-vs-hs256
stage: explainer
date: 2026-01-18
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.analyze"
labels: ["auth", "jwt", "debug", "security", "analysis"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - frontend/src/lib/auth.ts
  - backend/auth_handler.py
tests:
  - JWT token decoding
---

## Prompt

now, this is one analysis test for you.

better auth is now generating tokens but we dont know why backend is unable to decode JWT token,
i will provide you the recent generated JWT  token
[TOKEN CENSORED FOR SECURITY]

what you have to do

use same BETTER_AUTH_SECRET and algorthm as frontend/ and decode it and print result on log

## Response snapshot

## JWT Token Analysis

**Decoded Header:**
```json
{
  "alg": "EdDSA",
  "kid": "[CENSORED]"
}
```

**Decoded Payload:**
```json
{
  "iat": [TIMESTAMP],
  "name": "[CENSORED]",
  "email": "[CENSORED]",
  "emailVerified": false,
  "image": null,
  "createdAt": "[TIMESTAMP]",
  "updatedAt": "[TIMESTAMP]",
  "id": "[CENSORED]",
  "sub": "[CENSORED]",
  "exp": [TIMESTAMP],
  "iss": "better-auth",
  "aud": "http://localhost:3000"
}
```

## Analysis

The issue is now clear! The JWT token is using the **EdDSA** algorithm (Edwards-curve Digital Signature Algorithm) with Curve25519, not **HS256** as we configured in the frontend. This explains why the backend can't decode the token:

1. **Frontend Configuration**: We configured Better Auth to use HS256 algorithm in `frontend/src/lib/auth.ts`
2. **Actual Token**: The token is actually signed with EdDSA algorithm
3. **Backend Expectation**: The backend expects HS256 and tries to decode with the configured algorithm

## Root Cause

Despite configuring the `signingAlgorithm: "HS256"` in the frontend, Better Auth is still using EdDSA. This could be because:

1. The configuration isn't being applied correctly
2. Better Auth is overriding the configuration
3. The JWT plugin configuration format might be incorrect

Looking at the current configuration in `frontend/src/lib/auth.ts`:
```typescript
jwt({
  jwt: {
    issuer: "better-auth",
    signingAlgorithm: "HS256",
  }
})
```

The JWT plugin is still generating tokens with EdDSA instead of HS256. The algorithm in the token header (`"alg": "EdDSA"`) indicates that the signing algorithm setting isn't taking effect.

## Solution Required

The frontend auth configuration needs to be fixed to ensure Better Auth generates tokens with HS256 algorithm that matches what the backend expects.

## Outcome

- ✅ Impact: Identified JWT algorithm mismatch as the root cause of decoding failures
- 🧪 Tests: JWT token decoded successfully showing EdDSA algorithm instead of HS256
- 📁 Files: Analysis of frontend/src/lib/auth.ts and backend/auth_handler.py reveals mismatch
- 🔁 Next prompts: Need to fix Better Auth JWT configuration to use HS256
- 🧠 Reflection: Configuration override or format issue is preventing HS256 enforcement

## Evaluation notes (flywheel)

- Failure modes observed: JWT algorithm mismatch between frontend generation and backend expectation
- Graders run and results (PASS/FAIL): PASS - identified root cause of JWT decoding issue
- Prompt variant (if applicable): JWT analysis and debugging prompt
- Next experiment (smallest change to try): Update Better Auth JWT configuration to enforce HS256