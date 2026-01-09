---
id: "0001"
title: "Authentication Architecture Plan - Next.js + FastAPI + NeonDB"
stage: "general"
date_iso: "2026-01-07"
surface: "agent"
model: "claude-haiku-4-5-20251001"
feature: "none"
branch: "002-todo-web-app"
user: "developer"
command: "search about better auth implementation on next.js to create Authentication feature and then connect it with python fastapi backend and neondb batabase"
labels: ["authentication", "better-auth", "nextjs", "fastapi", "neondb", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "frontend/lib/auth.ts"
  - "frontend/app/api/auth/[...all]/route.ts"
  - "frontend/lib/auth-client.ts"
  - "backend/main.py"
  - "backend/auth.py"
  - "backend/database.py"
tests_yaml: []
prompt_text: |
  search about better auth implementation on next.js to create Authentication feature and then connect it with python fastapi backend and neondb batabase
response_text: |
  # Authentication Implementation Plan: Next.js + FastAPI + NeonDB

  ## Current Understanding from Research

  From the Better Auth documentation, I've learned:

  1. **Better Auth** is a full-stack authentication library that primarily runs on the frontend and Node.js/Edge environments
  2. It has built-in database adapters for PostgreSQL, MySQL, SQLite, MongoDB, and others (including NeonDB via PostgreSQL adapter)
  3. It supports email/password, social login, and various other authentication methods
  4. It has built-in Next.js integration

  However, there's an important architectural consideration: **Better Auth is designed to run as a Node.js service**, not as a Python/FastAPI service. This means we need to think about how to bridge these technologies.

  ## Recommended Architecture

  Since Better Auth doesn't natively run on Python/FastAPI, I recommend a **hybrid approach**:

  ### Option 1: Better Auth as Authentication Service (Recommended)
  ```
  Next.js Frontend ←→ Better Auth (Node.js Service) ←→ NeonDB (PostgreSQL)
                        ↓
                 FastAPI Backend ←→ NeonDB (PostgreSQL)
  ```

  ### Option 2: Separate Authentication Systems
  - Use Better Auth for Next.js frontend authentication
  - Implement separate authentication in FastAPI using the same NeonDB
  - Share session/user data between systems

  ## Detailed Implementation Plan

  ### Phase 1: Setting up Better Auth with NeonDB

  First, let's implement Better Auth with NeonDB for the Next.js frontend:

  1. **Install Better Auth in the Next.js frontend**:
  ```bash
  npm install better-auth
  ```

  2. **Configure Better Auth with NeonDB (PostgreSQL adapter)**:
  ```typescript
  // lib/auth.ts
  import { betterAuth } from "better-auth";
  import { Pool } from "pg";

  export const auth = betterAuth({
    database: new Pool({
      connectionString: process.env.NEON_DATABASE_URL!,
    }),
    emailAndPassword: {
      enabled: true,
    },
    socialProviders: {
      // Add providers like GitHub, Google, etc. as needed
    },
  });
  ```

  3. **Create the API route handler in Next.js**:
  ```typescript
  // app/api/auth/[...all]/route.ts
  import { auth } from "@/lib/auth";
  import { toNextJsHandler } from "better-auth/next-js";

  export const { GET, POST } = toNextJsHandler(auth);
  ```

  4. **Create the client instance**:
  ```typescript
  // lib/auth-client.ts
  import { createAuthClient } from "better-auth/react";

  export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  });
  ```

  ### Phase 2: Connecting FastAPI to the Same NeonDB

  1. **Setup FastAPI with NeonDB**:
  ```python
  # backend/main.py
  from fastapi import FastAPI, Depends
  from sqlalchemy import create_engine
  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy.orm import sessionmaker
  import os

  DATABASE_URL = os.getenv("NEON_DATABASE_URL")

  engine = create_engine(DATABASE_URL)
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

  Base = declarative_base()

  app = FastAPI()

  def get_db():
      db = SessionLocal()
      try:
          yield db
      finally:
          db.close()
  ```

  2. **Share user session information between systems**:
  Since Better Auth manages sessions in the database, your FastAPI endpoints can verify user authentication by checking session tokens against the Better Auth session table.

  ### Phase 3: Cross-Service Authentication

  For FastAPI to recognize authenticated users from Better Auth, you can:

  1. **Pass session tokens from frontend to FastAPI**:
  ```javascript
  // In Next.js, when making requests to FastAPI
  const response = await fetch('http://localhost:8000/api/protected', {
    headers: {
      'Authorization': `Bearer ${session.token}`, // or however you want to pass it
      'Cookie': document.cookie // to include session cookies
    }
  });
  ```

  2. **Verify sessions in FastAPI**:
  ```python
  # backend/auth.py
  from fastapi import HTTPException, Depends
  from typing import Optional
  from sqlmodel import Session, select
  from .models import Session as AuthSession  # Better Auth session table
  from .database import get_db

  async def verify_auth(token: str, db: Session = Depends(get_db)):
      # Check if the session exists in Better Auth's session table
      statement = select(AuthSession).where(AuthSession.token == token)
      session = db.exec(statement).first()

      if not session or session.expires_at < datetime.utcnow():
          raise HTTPException(status_code=401, detail="Invalid session")

      return session.user_id
  ```

  ## Alternative Approach: Pure FastAPI Authentication

  If you prefer to keep everything in FastAPI, you could implement authentication entirely in FastAPI using libraries like `fastapi-users` or `Authlib`, but this would mean losing Better Auth's rich feature set and Next.js integration.

  ## NeonDB Configuration

  NeonDB is PostgreSQL-compatible, so it works well with both Better Auth's PostgreSQL adapter and FastAPI's typical database stack.

  Environment variables needed:
  ```
  NEXT_PUBLIC_BASE_URL=http://localhost:3000
  NEON_DATABASE_URL=your_neon_connection_string
  BETTER_AUTH_SECRET=your_secret_key
  BETTER_AUTH_URL=http://localhost:3000
  ```

  ## Implementation Steps Summary

  1. Set up Better Auth in Next.js with NeonDB
  2. Create API routes for authentication in Next.js
  3. Set up FastAPI with NeonDB connection
  4. Implement session verification mechanism between Next.js and FastAPI
  5. Create shared user context between frontend and backend services

  This approach allows you to leverage Better Auth's robust authentication features while maintaining your FastAPI backend for business logic.
outcome: "Successfully researched and documented an architecture plan for connecting Next.js with Better Auth, FastAPI backend, and NeonDB database."
evaluation: "The plan addresses the core challenge of bridging Better Auth (Node.js) with FastAPI (Python) while using a shared NeonDB database."
---