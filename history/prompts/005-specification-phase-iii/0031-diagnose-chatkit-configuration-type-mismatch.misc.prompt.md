---
id: 0031
title: Diagnose ChatKit configuration type mismatch
stage: misc
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.analyze
labels: [chatkit-diagnosis, configuration-mismatch, sdk-validation, spec-compliance]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/plan.md (read)
 - specs/005-specification-phase-iii/research.md (read)
 - specs/005-specification-phase-iii/quickstart.md (read)
 - frontend/src/components/ChatProvider.tsx (analyzed)
 - frontend/src/lib/config.ts (analyzed)
tests:
 - none
---

## Prompt

now find the error of why the handshake between chatbot frontend and backend is failing

first look at the following console and errors records

[User provided detailed error logs showing:]
- ChatKit Configuration Error: "ChatKit.create(): ✖ Invalid input → at api"
- FatalAppError from ChatKit SDK during initialization
- IntegrationError: "Command onSetOptions not supported"
- Frontend console: All auth requests returning 200 OK
- Backend console: Only /tasks requests visible, NO /chat requests
- No network errors, authentication working correctly

## Response snapshot

**Diagnosis Methodology:**

Conducted systematic analysis following /sp.analyze workflow:
1. Read plan.md, research.md, quickstart.md for intended architecture
2. Compared specification with actual implementation
3. Analyzed ChatKit SDK documentation via Context7
4. Identified configuration type mismatch as root cause

**Root Cause Identified:**

**Configuration Type Mismatch** - Implementation mixes incompatible ChatKit SDK configuration types.

### ChatKit SDK Has Two Mutually Exclusive Config Types:

**1. HostedApiConfig** (OpenAI-hosted backend):
```typescript
{
  getClientSecret: () => Promise<string>
}
```

**2. CustomApiConfig** (Self-hosted backend):
```typescript
{
  domainKey: string,      // REQUIRED
  url: string,            // REQUIRED
  fetch?: typeof fetch    // Optional (for JWT injection)
}
```

**You CANNOT mix properties from both types.**

### What the Plan Specifies (research.md lines 34-56):

```typescript
const { control } = useChatKit({
  api: {
    url: `${CONFIG.API_BASE_URL}/api/${userId}/chat`,
    domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY,
    fetch: (url, options) => {
      return fetch(url, {
        ...options,
        headers: {
          ...options.headers,
          'Authorization': `Bearer ${token}`,
        },
      });
    },
  },
});
```

**Type**: CustomApiConfig ✅
**Properties**: url ✅, domainKey ✅, fetch ✅

### What the Code Actually Does (ChatProvider.tsx lines 77-94):

```typescript
const { control } = useChatKit({
  api: {
    url: `${CONFIG.API_BASE_URL}/${userId}/chat`,
    getClientSecret: async () => {
      return currentToken;
    },
  },
});
```

**Type**: Mixed (INVALID) ❌
**Properties**:
- url (from CustomApiConfig) ✅
- getClientSecret (from HostedApiConfig) ❌ INCOMPATIBLE
- Missing domainKey ❌ REQUIRED for CustomApiConfig
- Missing fetch ❌ NEEDED for JWT injection

### Why It Fails:

1. SDK validates configuration during initialization
2. Detects `url` property → expects CustomApiConfig
3. Finds `getClientSecret` → invalid for CustomApiConfig
4. Missing `domainKey` → required for CustomApiConfig
5. **Validation fails BEFORE any network requests**

### Evidence Supporting Diagnosis:

- ✅ Backend logs show ZERO requests to `/chat` endpoint
- ✅ Only `/tasks` requests visible (those work fine with JWT)
- ✅ Error occurs at SDK initialization, not during handshake
- ✅ Error message: "Invalid input → at api" (configuration validation)
- ✅ No 401/403/500 errors (authentication never attempted)

### Specification Compliance Analysis:

| Requirement | Plan Spec | Implementation | Status |
|-------------|-----------|----------------|--------|
| Config Type | CustomApiConfig | Mixed | ❌ FAIL |
| `url` | Required | Present | ✅ PASS |
| `domainKey` | Required | Missing | ❌ FAIL |
| `fetch` | Required | Missing | ❌ FAIL |
| `getClientSecret` | Not in plan | Present (wrong) | ❌ FAIL |

**Compliance Score**: 1/5 (20%)

### Additional Findings:

1. **Missing Environment Variable**: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` not defined anywhere
2. **Implementation Drift**: Code deviated from documented plan during multiple failed iterations
3. **No Handshake Failure**: Error occurs before any backend communication attempts

### Recommended Fix:

Update ChatProvider.tsx to match plan specification:

```typescript
const { control } = useChatKit({
  api: {
    // CustomApiConfig for self-hosted backend
    domainKey: 'localhost-dev',  // Placeholder for development
    url: `${CONFIG.API_BASE_URL}/${userId}/chat`,

    // Custom fetch to inject JWT
    fetch: async (url: string, options?: RequestInit) => {
      const currentToken = tokenRef.current;

      if (!currentToken) {
        throw new Error('Authentication token not available');
      }

      return fetch(url, {
        ...options,
        headers: {
          ...options?.headers,
          'Authorization': `Bearer ${currentToken}`,
          'Content-Type': 'application/json',
        },
      });
    },
  },
  onError: (err) => {
    console.error('ChatKit error:', err);
    // ... existing error handling
  },
});
```

## Outcome

- ✅ Impact: Identified root cause of ChatKit integration failure through systematic spec-to-implementation analysis - configuration type mismatch where implementation mixed incompatible CustomApiConfig and HostedApiConfig properties, causing SDK validation to reject configuration before any network requests
- 🧪 Tests: No automated tests - diagnosis based on error analysis, documentation review, and SDK specification research via Context7
- 📁 Files: Analyzed frontend/src/components/ChatProvider.tsx (found invalid mixed config), specs/005-specification-phase-iii/plan.md (found correct CustomApiConfig spec), specs/005-specification-phase-iii/research.md (found intended architecture), frontend/src/lib/config.ts (verified environment setup)
- 🔁 Next prompts: Apply recommended fix to ChatProvider.tsx (replace getClientSecret with domainKey + fetch), Add NEXT_PUBLIC_OPENAI_DOMAIN_KEY to environment configuration, Test ChatKit UI renders without validation errors, Verify backend receives authenticated /chat requests with JWT, Validate SSE streaming works end-to-end
- 🧠 Reflection: This diagnosis revealed the importance of consulting specification documents BEFORE attempting fixes. Multiple implementation iterations failed because they were based on assumptions rather than documented architecture. The plan.md clearly specified CustomApiConfig with domainKey and fetch properties, but implementation used getClientSecret from a different configuration type. The error was NOT a handshake failure - it was SDK input validation failing before any network communication. This highlights the value of systematic analysis: read specs → compare with code → identify deviation → apply documented solution.

## Evaluation notes (flywheel)

- Failure modes observed: Implementation drift from specification (code deviated during failed iterations), Configuration type confusion (mixed incompatible SDK types), Missing environment variables (NEXT_PUBLIC_OPENAI_DOMAIN_KEY not configured), Assumption-based debugging (multiple fixes attempted without consulting plan)
- Graders run and results (PASS/FAIL): Spec compliance: FAIL (20% - only url property correct), Configuration type: FAIL (mixed CustomApiConfig and HostedApiConfig), Required properties: FAIL (missing domainKey and fetch), Error diagnosis: PASS (correctly identified SDK validation failure), Root cause analysis: PASS (found configuration type mismatch), Documentation review: PASS (systematically compared plan vs implementation)
- Prompt variant (if applicable): /sp.analyze with explicit instruction to read all files, check plan.md for solution, compare specs with code, then report diagnosis
- Next experiment (smallest change to try): Update ChatProvider.tsx api configuration to use CustomApiConfig exclusively (add domainKey: 'localhost-dev', replace getClientSecret with fetch function that injects Authorization header), then test if ChatKit UI initializes without "Invalid input" error
