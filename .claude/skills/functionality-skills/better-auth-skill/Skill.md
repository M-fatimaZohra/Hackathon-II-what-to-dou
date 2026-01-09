# Skill Name

better-auth-integration

---

## Skill Purpose

Implements and validates Better Auth integration in a Next.js application with a FastAPI backend using JWT-based authorization. Enforces strict separation between frontend authentication and backend authorization.

---

## Skill Tasks

* Configure Better Auth with email/password and social providers
* Initialize Better Auth in Next.js using a centralized auth configuration
* Expose authentication endpoints via Next.js route handlers
* Implement server actions for signup, signin, and logout
* Ensure authentication logic runs only on the server
* Prevent client-side identity injection or user impersonation
* Guide JWT verification logic in FastAPI without issuing JWTs from frontend
* Validate environment variable usage across frontend and backend

---

## How the Skill Performs Its Tasks

Frontend responsibilities:
* Handles user authentication and session management only
* Uses Better Auth as identity provider
* Never accesses the database directly
* Never generates or signs backend JWTs
* Sends authenticated requests using Authorization headers

Backend responsibilities:
* Validates JWTs using a shared secret
* Derives user identity from JWT payload (sub claim)
* Rejects requests with mismatched path user_id and JWT subject
* Owns authorization, data access, and business logic

Authentication flow:
* User signs up or signs in via Better Auth
* Better Auth establishes a secure session and cookies
* Frontend retrieves session context when needed
* Backend receives requests with Bearer JWT
* Backend middleware verifies JWT signature and claims
* Backend injects user identity into request state

Security constraints:
* user_id must never be accepted from client payloads
* JWT_SECRET must be a static, high-entropy secret
* JWT_SECRET is shared between frontend auth issuer and backend verifier
* Tokens are verified, not stored, in environment variables
* Public routes must be explicitly whitelisted

Environment variables:
Frontend:
* BETTER_AUTH_SECRET
* JWT_FRONT_URL

Backend:
* BETTER_AUTH_SECRET
* DATABASE_URL
* JWT_BACKEND_URL

Common mistakes to prevent:
* Installing database clients in the frontend
* Using Prisma-specific patterns when backend uses SQLModel
* Trusting client-provided user identifiers
* Generating JWT secrets per user
* Mixing authentication and authorization responsibilities

---

## Required Inputs

* Project structure with Next.js frontend and FastAPI backend
* Authentication requirements and provider preferences
* Environment variable configuration preferences
* Database connection details for backend

Example:
```
Integrate Better Auth with email/password and Google OAuth for the Next.js frontend, connecting to our FastAPI backend with JWT verification.
```

---

## Expected Output

* Clean Better Auth setup in Next.js
* Secure JWT verification in FastAPI
* Production-ready authentication architecture
* Maintainable, testable, and extensible auth system
* Proper separation of authentication and authorization concerns

Focus: security, maintainability, and clear separation of concerns between frontend and backend.