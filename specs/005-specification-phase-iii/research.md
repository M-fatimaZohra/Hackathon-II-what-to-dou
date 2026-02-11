# Research: ChatKit Frontend Integration

**Feature**: ChatKit Frontend Integration for AI Chatbot
**Date**: 2026-02-08
**Status**: Complete

## Research Objectives

1. Evaluate ChatKit React SDK capabilities and integration patterns
2. Analyze existing Next.js 16 App Router architecture
3. Determine authentication integration approach with Better Auth
4. Identify performance optimization strategies
5. Research error handling and reconnection patterns

## Findings

### 1. ChatKit React SDK Integration

**Decision**: Use ChatKit React SDK for real-time messaging capabilities

**Rationale**:
- Provides WebSocket-based real-time communication out of the box
- Native React hooks and context providers for easy integration
- Built-in presence management and typing indicators
- Handles connection management and reconnection automatically
- Supports file attachments and rich message formats

**Alternatives Considered**:
- **Custom WebSocket implementation**: Rejected due to complexity and maintenance overhead
- **Socket.io**: Rejected as ChatKit provides more chat-specific features
- **Firebase Realtime Database**: Rejected to maintain backend control and user isolation

**Integration Pattern**:
```typescript
// Hook-based pattern with ChatKit SDK using CustomApiConfig
import { ChatKit, useChatKit } from '@openai/chatkit-react';

function ChatProvider({ children }) {
  const { control } = useChatKit({
    api: {
      // CustomApiConfig for self-hosted backend
      domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || 'localhost-dev',
      url: `${CONFIG.API_BASE_URL}/api/${userId}/chat`,

      // Custom fetch with request type routing and JWT injection
      fetch: async (url, options) => {
        const originalBody = JSON.parse(options.body as string);

        // CRITICAL: Intercept threads.list requests (FR-017)
        // Backend doesn't implement thread listing endpoint
        if (originalBody.type === 'threads.list') {
          return new Response(JSON.stringify({
            data: [],
            has_more: false
          }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
          });
        }

        // Handle threads.create and threads.runs.create
        // Transform to backend format
        const transformedBody = {
          message: originalBody.params?.input?.content || '',
          conversation_id: originalBody.params?.thread_id
            ? parseInt(originalBody.params.thread_id, 10)
            : undefined
        };

        // Inject JWT Authorization header
        return fetch(url, {
          ...options,
          body: JSON.stringify(transformedBody),
          headers: {
            ...options.headers,
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
        });
      },
    },
  });

  return <ChatKit control={control} className="h-full w-full" />;
}
```

**ChatKit SDK Configuration Types**:

The @openai/chatkit-react SDK supports two mutually exclusive configuration types:

1. **HostedApiConfig** (OpenAI-hosted backend):
```typescript
{
  getClientSecret: () => Promise<string>
}
```

2. **CustomApiConfig** (Self-hosted backend) - **USED IN THIS PROJECT**:
```typescript
{
  domainKey: string,      // Required for domain verification
  url: string,            // Backend endpoint URL
  fetch?: typeof fetch    // Optional custom fetch for auth injection
}
```

**CRITICAL**: You CANNOT mix properties from both types. Using `url` (CustomApiConfig) with `getClientSecret` (HostedApiConfig) causes SDK validation error: "Invalid input → at api"

**Why CustomApiConfig**:
- Allows self-hosted backend with custom SSE format
- Acts as pass-through - doesn't enforce ChatKit protocol
- Custom fetch function enables JWT injection
- Backend can use any response format for MCP tool flexibility

**Backend Response Format**:
Backend uses custom SSE format (not ChatKit protocol):
```json
{
  "type": "response.output_text.delta",
  "delta": "Hello, "
}
```

ChatKit SDK with CustomApiConfig accepts this format directly - no translation needed.

**ChatKit Multi-Request Architecture** (Discovered during implementation - PHR-0052):

ChatKit SDK sends multiple request types during operation:
- **threads.list**: Sent on mount to load conversation history
- **threads.create**: Sent when user creates new conversation
- **threads.runs.create**: Sent for messages in existing conversations

**Critical Finding**: Backend only implements a single `/api/{user_id}/chat` endpoint, not separate endpoints for each request type. The custom fetch function MUST intercept `threads.list` requests and return mock responses, otherwise:
1. `threads.list` gets transformed to `{message: ''}`
2. Backend returns error or invalid response
3. ChatKit stores broken response internally
4. When streaming completes, ChatKit reconciles state and clears UI (blank screen)

**Solution**: Request type routing in custom fetch function (see updated integration pattern below).

**Message Persistence Requirements** (Discovered during implementation - PHR-0052):

ChatKit SDK requires specific metadata fields in SSE events to persist messages after streaming:
- `status: "completed"` - Indicates message is fully processed
- `created_at: timestamp` - Unix timestamp for message ordering

Without these fields, ChatKit discards messages when `response.done` event is received, causing messages to disappear from UI after streaming completes.

### 2. Next.js 16 App Router Architecture

**Decision**: Use App Router with Server Components for pages and Client Components for interactive chat UI

**Rationale**:
- App Router is the recommended approach for Next.js 16
- Server Components reduce client-side JavaScript bundle
- Client Components ('use client') for interactive chat features
- File-based routing simplifies page structure
- Built-in loading and error states

**Existing Architecture Analysis**:
- Current structure: `src/app/` for pages, `src/components/` for components
- Better Auth already integrated with `authClient.getSession()`
- API client in `src/lib/api.ts` with JWT token handling
- Tailwind CSS v4 for styling

**Integration Approach**:
- Add `/chat/page.tsx` as new route
- Create chat components in `src/components/`
- Extend existing API client for chat endpoints
- Reuse existing authentication flow

### 3. Authentication Integration

**Decision**: Use Better Auth JWT tokens for ChatKit authentication via backend token endpoint

**Rationale**:
- Better Auth already provides JWT tokens via `authClient.getSession()`
- Backend can validate JWT and generate ChatKit tokens
- Maintains user isolation and security
- Single authentication flow for entire application

**Implementation Pattern**:
```typescript
// Frontend: ChatKit token provider
const tokenProvider = new TokenProvider({
  url: '/api/chatkit/token',
  headers: {
    Authorization: `Bearer ${authClient.getSession().accessToken}`
  }
});

// Backend: Token generation endpoint
@app.post("/api/chatkit/token")
async def get_chatkit_token(current_user: User = Depends(get_current_user)):
    token = generate_chatkit_token(current_user.id)
    return {"token": token}
```

### 4. Performance Optimization Strategies

**Decision**: Implement virtualized lists, lazy loading, and message caching

**Rationale**:
- Large conversation histories (1000+ messages) require optimization
- Virtualized lists render only visible messages
- Lazy loading reduces initial bundle size
- Message caching reduces API calls

**Strategies**:
1. **Virtualized Lists**: Use `react-window` or `react-virtualized` for message lists
2. **Code Splitting**: Lazy load chat components with `React.lazy()`
3. **Message Caching**: Cache recent messages in memory (last 100 messages)
4. **Pagination**: Load older messages on scroll with 50-message batches
5. **Debouncing**: Debounce input events to reduce re-renders

**Performance Targets**:
- Page load: <2 seconds for 95% of users
- Message delivery: <3 seconds for 90% of interactions
- Memory usage: <100MB for 1000+ message conversations

### 5. Error Handling and Reconnection

**Decision**: Implement exponential backoff with intelligent retry logic

**Rationale**:
- Network interruptions are common in web applications
- Exponential backoff prevents server overload
- User feedback improves experience during errors
- Automatic reconnection maintains conversation continuity

**Error Handling Pattern**:
```typescript
class ErrorHandler {
  private retryAttempts = 0;
  private maxRetries = 5;
  private baseDelay = 1000;

  async handleError(error: Error) {
    if (this.retryAttempts < this.maxRetries) {
      const delay = this.baseDelay * Math.pow(2, this.retryAttempts);
      await this.wait(delay);
      this.retryAttempts++;
      return this.retry();
    }
    throw new Error('Max retries exceeded');
  }
}
```

**Error Categories**:
1. **Network Errors**: Retry with exponential backoff
2. **Authentication Errors**: Prompt user to re-authenticate
3. **Validation Errors**: Display error message, no retry
4. **Server Errors**: Retry with backoff, fallback to error state

### 6. Stateless Architecture

**Decision**: Maintain stateless frontend with all conversation state in backend

**Rationale**:
- Required by FR-007 for scalability
- Enables user isolation (FR-008)
- Simplifies frontend logic
- Backend manages conversation history and context

**Implementation**:
- Each request includes JWT + userId
- Frontend does not persist conversation state
- Conversation history fetched from backend on page load
- Real-time updates via ChatKit, but state source is backend

### 7. Environment Configuration

**Decision**: Use environment variables with separate dev/prod configurations

**Rationale**:
- Required by FR-009 for dev/prod support
- Enables different logging levels
- Allows test/mock data in development
- Maintains security in production

**Configuration Pattern**:
```typescript
// src/lib/config.ts
export const config = {
  isDevelopment: process.env.NODE_ENV === 'development',
  chatkit: {
    instanceLocator: process.env.VITE_CHATKIT_INSTANCE_LOCATOR,
    debug: process.env.NODE_ENV === 'development',
    logging: process.env.NODE_ENV === 'development' ? 'verbose' : 'error'
  },
  api: {
    baseUrl: process.env.VITE_API_URL || 'http://localhost:7860'
  }
};
```

## Technology Stack Summary

**Frontend**:
- Next.js 16.1.1 (App Router)
- React 19.2.3
- TypeScript 5.3
- ChatKit React SDK
- Better Auth 1.4.10
- Tailwind CSS v4

**Testing**:
- Jest (unit tests)
- React Testing Library (component tests)
- Playwright (E2E tests)

**Development Tools**:
- pnpm (package manager)
- ESLint (linting)
- Prettier (formatting)

## Best Practices

1. **Component Architecture**:
   - Use composition over inheritance
   - Keep components small and focused
   - Separate presentational and container components

2. **State Management**:
   - Use React Context for global chat state
   - Use local state for component-specific state
   - Avoid prop drilling with context providers

3. **Error Handling**:
   - Always provide user feedback for errors
   - Implement graceful degradation
   - Log errors for debugging

4. **Performance**:
   - Lazy load components when possible
   - Memoize expensive computations
   - Use virtualized lists for large datasets

5. **Security**:
   - Validate all user input
   - Use JWT tokens for authentication
   - Implement proper CORS configuration
   - Sanitize message content

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| ChatKit SDK breaking changes | High | Pin SDK version, test before upgrading |
| Network connectivity issues | Medium | Implement exponential backoff and offline mode |
| Performance degradation with large conversations | Medium | Implement virtualization and pagination |
| Authentication token expiration | Low | Implement token refresh logic |
| Cross-browser compatibility | Low | Test on major browsers, use polyfills |

## Next Steps

1. Create data-model.md with TypeScript interfaces
2. Create contracts/ with API specifications
3. Create quickstart.md with setup instructions
4. Proceed to tasks.md for implementation breakdown

---

**Research Status**: ✅ Complete
**All NEEDS CLARIFICATION items**: ✅ Resolved
**Ready for Phase 1**: ✅ Yes