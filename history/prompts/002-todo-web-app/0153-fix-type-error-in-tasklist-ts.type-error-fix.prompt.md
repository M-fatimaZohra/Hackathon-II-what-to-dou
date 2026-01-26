---
id: 0153
title: fix-type-error-in-tasklist-ts
stage: refactor
date: 2026-01-23
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-todo-web-app
branch: 002-todo-web-app
user: A.ZEE
command: "/sp.implement"
labels: ["typescript", "type-error", "api", "compatibility"]
links:
  spec: null
  plan: null
  tasks: null
  test: null
files:
  - frontend/src/components/TaskList.tsx
tests:
  - TypeScript type error resolved
  - API compatibility maintained
  - Filter functionality preserved
  - Null to undefined conversion implemented
---

## Prompt

go to components/TaskList.tsx do this changes to solve given error

Error:
./src/components/TaskList.tsx:56:28
Type error: Argument of type '{ search: string; priority: string | null; completed: boolean | null; }' is not assignable to parameter of type '{ search?: string | undefined; priority?: string | undefined; completed?: boolean | null | undefined; }'.
  Types of property 'priority' are incompatible.
    Type 'string | null' is not assignable to type 'string | undefined'.
      Type 'null' is not assignable to type 'string | undefined'.

using the filters
  55 |       const tasksData = await Promise.race([
> 56 |         apiClient.getTasks(filters),
     |                            ^
  57 |         timeoutPromise
  58 |       ]) as Task[];
  59 |
Next.js build worker exited with code: 1 and signal: null

Solution:
   // Convert null values to undefined for API compatibility
      const apiFilters = {
        search: filters.search || undefined,
        priority: filters.priority ?? undefined,
        completed: filters.completed ?? undefined,
      };

      // Race the API call against the timeout, passing the filters
      const tasksData = await Promise.race([
        apiClient.getTasks(apiFilters),

## Response snapshot

Successfully fixed the TypeScript type error in TaskList.tsx by converting null values to undefined for API compatibility:

### Changes Made:
1. Added a conversion layer to transform the filters object before passing to the API client
2. Used nullish coalescing operators (`??`) to convert `null` values to `undefined`
3. Maintained the `||` operator for search field to handle empty strings as well
4. Preserved all existing functionality while fixing the type mismatch

### Result:
- ✅ TypeScript type error resolved
- ✅ API client now receives properly typed parameters
- ✅ Filter functionality remains intact
- ✅ Search, priority, and completion status filters work as expected
- ✅ All existing functionality preserved

## Outcome

- Impact: Fixed critical build error preventing application compilation
- Tests: TypeScript compilation now passes without errors
- Files: Updated TaskList.tsx with proper type conversion
- Next prompts: Ready for continued development
- Reflection: Proper type handling is crucial for API compatibility