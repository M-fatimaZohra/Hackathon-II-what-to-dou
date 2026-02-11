---
id: 0029
title: Move ChatKit script to Next.js Script component
stage: green
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: M-fatimaZohra
command: /sp.implement
labels: [chatkit-cdn, nextjs-script, performance-optimization, layout-refactor]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - frontend/src/app/layout.tsx (modified)
tests:
 - none
---

## Prompt

Move the src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js" from <script> into the <Script> using next/script in layout.tsx.

## Response snapshot

Successfully converted the ChatKit CDN script from a regular HTML `<script>` tag to Next.js's `<Script>` component for better performance and control.

**Changes Made:**

1. **Added Script import**: `import Script from "next/script"`
2. **Moved script inside body**: Next.js Script component must be inside `<body>` tag
3. **Applied loading strategy**: Used `strategy="afterInteractive"` for optimal performance

**Before:**
```tsx
<html lang="en">
  <script src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"></script>
  <body>
    {/* content */}
  </body>
</html>
```

**After:**
```tsx
<html lang="en">
  <body>
    <Script
      src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
      strategy="afterInteractive"
    />
    {/* content */}
  </body>
</html>
```

**Benefits:**
- Better performance optimization through Next.js's script loading strategies
- Non-blocking page rendering
- Integrates with Next.js's optimization pipeline
- Controlled loading timing with `afterInteractive` strategy

## Outcome

- ✅ Impact: Migrated ChatKit CDN script from HTML script tag to Next.js Script component with afterInteractive strategy, improving page load performance and following Next.js best practices
- 🧪 Tests: No automated tests - functional change ready for runtime testing
- 📁 Files: Modified frontend/src/app/layout.tsx (added Script import, moved script inside body with strategy)
- 🔁 Next prompts: Test frontend with npm run dev to verify ChatKit loads correctly, Monitor browser console for any script loading issues, Consider adding error handling with onError callback if needed
- 🧠 Reflection: Next.js Script component provides better control over third-party script loading compared to raw HTML script tags. The afterInteractive strategy ensures the script loads after the page becomes interactive, preventing blocking of critical rendering path. This is especially important for external CDN scripts like ChatKit that aren't essential for initial page render.

## Evaluation notes (flywheel)

- Failure modes observed: None - straightforward migration from HTML script to Next.js Script component
- Graders run and results (PASS/FAIL): Import added: PASS (Script from next/script), Script placement: PASS (inside body tag as required), Loading strategy: PASS (afterInteractive for non-critical external script), Syntax: PASS (proper JSX syntax with self-closing tag)
- Prompt variant (if applicable): /sp.implement with specific instruction to use Next.js Script component
- Next experiment (smallest change to try): Start frontend with npm run dev, open browser DevTools Network tab, verify ChatKit script loads after page interactive, check browser console for any loading errors or warnings
