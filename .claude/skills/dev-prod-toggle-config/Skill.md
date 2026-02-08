---
name: dev-prod-toggle-config
description: Configures the dynamic environment toggle (developer vs production) for the frontend. Use this when setting up or modifying lib/config.ts to handle environment-specific logic like secure cookies and base URLs.
---

# Dev-Prod Toggle Config Skill

This skill creates a centralized `config.ts` that dynamically adjusts application settings based on the `NEXT_PUBLIC_MOD` environment variable.

## File Generation
Create or update `frontend/src/lib/config.ts` with the following structure:

```typescript
const MOD = process.env.NEXT_PUBLIC_MOD || 'production';
export const IS_DEV = MOD === 'developer';

export const CONFIG = {
  API_BASE_URL: IS_DEV ? 'http://localhost:8000' : process.env.NEXT_PUBLIC_API_URL,
  AUTH_BASE_URL: IS_DEV ? 'http://localhost:3000' : process.env.NEXT_PUBLIC_BASE_URL,
  COOKIE_SECURE: !IS_DEV,
  HTTP_ONLY_TOKEN: !IS_DEV,
  REFRESH_CACHE: !IS_DEV,
};
```

## Usage Rules
- NEVER hardcode true or false for security settings in auth.ts.
- ALWAYS use CONFIG.COOKIE_SECURE for cookie attributes.
- Use IS_DEV for conditional logging or debug overlays in the UI.
