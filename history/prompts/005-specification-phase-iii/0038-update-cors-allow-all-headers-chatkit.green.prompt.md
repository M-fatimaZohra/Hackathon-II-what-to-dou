---
id: 0038
title: Update CORS allow all headers ChatKit
stage: green
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: [cors-config, chatkit-compatibility, headers, security-relaxation]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - backend/src/main.py (updated)
tests:
 - none (manual testing required)
---

## Prompt

In main.py: Update CORSMiddleware to use allow_headers=["*"] to allow chatkit header

## Response snapshot

**Context**: After fixing the OPTIONS preflight dependency issue, needed to ensure CORS allows all headers that ChatKit SDK might send.

**Change Made**: Updated CORS middleware configuration in main.py to allow all headers instead of restricting to specific headers.

**Before**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],  # Restrictive
)
```

**After**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # Allow all headers for ChatKit SDK compatibility
)
```

**Rationale**: ChatKit SDK may send custom headers beyond Authorization and Content-Type. Restricting headers could cause CORS preflight failures if ChatKit adds additional headers in requests.

## Outcome

- ✅ Impact: Updated CORS middleware to allow all headers, ensuring ChatKit SDK can send any custom headers without CORS blocking. This prevents potential preflight failures if ChatKit uses additional headers beyond Authorization and Content-Type.
- 🧪 Tests: No automated tests. Manual testing: restart backend, test chat from frontend, verify no CORS errors in browser console
- 📁 Files: Updated backend/src/main.py (line 36-41, changed allow_headers from specific list to ["*"])
- 🔁 Next prompts: Restart backend server, Test chat integration end-to-end, Verify no CORS errors in browser console, Send test message and confirm streaming works
- 🧠 Reflection: This is a pragmatic fix for development. In production, we should monitor what headers ChatKit actually uses and restrict to that specific list for better security. Using ["*"] is acceptable for development but should be tightened in production once we know the exact headers needed.

## Evaluation notes (flywheel)

- Failure modes observed: None - straightforward configuration change
- Graders run and results (PASS/FAIL): CORS configuration: PASS (allows all headers), Security consideration: NOTE (should restrict in production), ChatKit compatibility: PASS (no header restrictions)
- Prompt variant (if applicable): User provided explicit instruction to update CORS configuration
- Next experiment (smallest change to try): Restart backend, test chat, monitor browser console for any remaining CORS errors, verify streaming response works

