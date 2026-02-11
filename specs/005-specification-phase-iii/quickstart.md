# Quickstart Guide: ChatKit Frontend Integration

**Feature**: ChatKit Frontend Integration for AI Chatbot
**Date**: 2026-02-08
**Audience**: Developers implementing the ChatKit frontend

## Prerequisites

Before starting implementation, ensure you have:

1. **Node.js 18+** installed
2. **pnpm** package manager (or npm/yarn)
3. **Git** for version control
4. **Backend API** running on port 7860
5. **Better Auth** configured with PostgreSQL
6. **ChatKit Account** (will be set up during implementation)

## Environment Setup

### 1. Install Dependencies

```bash
cd frontend
pnpm install
```

### 2. Configure Environment Variables

Create or update `.env.local` in the frontend directory:

```env
# ChatKit Configuration (to be obtained during implementation)
NEXT_PUBLIC_CHATKIT_INSTANCE_LOCATOR=your-instance-locator
NEXT_PUBLIC_CHATKIT_KEY=your-chatkit-key

# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:7860

# Better Auth Configuration (already configured)
NEXT_PUBLIC_AUTH_SECRET=your-auth-secret
DATABASE_URL=your-database-url

# Environment
NODE_ENV=development
```

### 3. Verify Backend is Running

```bash
# In backend directory
cd backend
uvicorn main:app --reload --port 7860
```

Verify backend is accessible at `http://localhost:7860/docs`

### 4. Start Frontend Development Server

```bash
cd frontend
pnpm dev
```

Frontend should be accessible at `http://localhost:3000`

## Implementation Order

Follow this order to implement the ChatKit integration:

### Phase 1: Core Setup (Day 1-2)

1. **Install ChatKit SDK**
   ```bash
   pnpm add @chatkit/react @chatkit/types
   ```

2. **Create Type Definitions**
   - File: `frontend/src/types/chat.ts`
   - Copy interfaces from `data-model.md`
   - Validate TypeScript compilation

3. **Create ChatKit Configuration**
   - File: `frontend/src/lib/chatkit-client.ts`
   - Implement `getChatKitConfig()` function
   - Add environment variable validation

4. **Create ChatProvider Component**
   - File: `frontend/src/components/ChatProvider.tsx`
   - Implement component using useChatKit hook from @openai/chatkit-react
   - Configure custom fetch function for JWT authentication
   - Implement error handling

4.5. **Implement Request Type Routing (Critical - FR-017)**
   - File: `frontend/src/components/ChatProvider.tsx`
   - Add request type checking in custom fetch function
   - Intercept `threads.list` requests and return mock response `{data: [], has_more: false}`
   - Prevent state corruption by not sending threads.list to backend
   - Test: Verify browser console shows mock response for threads.list
   - Test: Verify no backend request is sent for threads.list
   - **Why Critical**: Without this, ChatKit state corrupts and UI goes blank after streaming

### Phase 2: UI Components (Day 3-4)

5. **Create ChatAssistant Component**
   - File: `frontend/src/components/chat/ChatAssistant.tsx`
   - Implement sliding sidebar wrapper
   - Integrate ChatKit component from @openai/chatkit-react
   - Add collapsible functionality with animations
   - Implement close button and keyboard shortcuts

6. **Update Tasks Page**
   - File: `frontend/src/app/tasks/page.tsx`
   - Wrap page with ChatProvider component
   - Add toggle button for chat sidebar
   - Integrate ChatAssistant component

### Phase 2.5: Backend Message Metadata (Day 4)

**Purpose**: Add required metadata fields to SSE events for ChatKit message persistence

7. **Add Message Metadata to Backend (Critical - FR-018)**
   - File: `backend/src/api/chat.py`
   - Locate the `thread.message.created` event in `stream_chat_response()` function
   - Add `"status": "completed"` to the message object
   - Add `"created_at": int(time.time())` to the message object
   - Import `time` module at top of file if not already imported
   - Test: Send message, verify it persists in UI after streaming completes
   - Test: Check browser console for `thread.message.created` event with metadata
   - **Why Critical**: Without these fields, ChatKit discards messages after streaming

### Phase 3: Integration & Testing (Day 5)

8. **Test Chat Integration**
   - Verify sidebar opens/closes correctly
   - Test JWT authentication flow
   - Verify message sending and receiving
   - Test error handling scenarios
   - **Critical Tests**:
     - Verify threads.list is intercepted (check console logs)
     - Verify messages persist after streaming completes
     - Send multiple messages and confirm all remain visible

### Phase 4: Backend Integration (Day 6-7)

10. **Extend API Client**
    - File: `frontend/src/lib/api.ts`
    - Add `sendMessage()` function
    - Add `getConversationHistory()` function
    - Implement error handling with retry logic

11. **Create Chat Service**
    - File: `frontend/src/lib/chat-service.ts`
    - Implement business logic layer
    - Handle MCP tool response parsing (FR-006)
    - Add exponential backoff for errors (FR-013)

### Phase 5: Testing (Day 8-9)

12. **Write Unit Tests**
    - Test ChatMessage component rendering
    - Test ChatInput validation
    - Test ChatWindow message display
    - Test error handling logic

13. **Write Integration Tests**
    - Test complete chat flow
    - Test authentication integration
    - Test API client integration

14. **Write E2E Tests**
    - Test user can send and receive messages
    - Test multi-turn conversations
    - Test error scenarios

### Phase 6: Polish & Optimization (Day 10)

15. **Performance Optimization**
    - Implement message virtualization
    - Add lazy loading for chat components
    - Optimize re-renders with React.memo

16. **Error Handling Enhancement**
    - Add user-friendly error messages
    - Implement retry UI
    - Add connection status indicator

17. **Final Testing & Documentation**
    - Test in both dev and prod modes
    - Update README with chat feature
    - Document any configuration changes

## Key Files to Create

### Required Files

```
frontend/src/
├── types/
│   └── chat.ts                      # TypeScript interfaces
├── lib/
│   └── config.ts                    # Environment configuration
├── components/
│   ├── ChatProvider.tsx             # Component using useChatKit hook
│   └── chat/
│       └── ChatAssistant.tsx        # Sidebar wrapper with ChatKit component
└── app/
    └── tasks/
        └── page.tsx                 # Tasks page with chat sidebar
```

### Files to Modify

```
frontend/src/
├── lib/
│   └── api.ts                       # Add chat endpoints
└── components/
    └── Navigation.tsx               # Add chat link
```

## Code Templates

### ChatProvider Template

```typescript
// frontend/src/components/ChatProvider.tsx
'use client';

import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { authClient } from '@/lib/auth-client';
import { CONFIG } from '@/lib/config';
import { ReactNode, useState, useEffect } from 'react';

interface ChatProviderProps {
  children: ReactNode;
}

export function ChatProvider({ children }: ChatProviderProps) {
  const [token, setToken] = useState<string>('');
  const [userId, setUserId] = useState<string>('');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initAuth = async () => {
      try {
        const session = await authClient.getSession();
        if (session?.data?.user?.id && session?.data?.session?.token) {
          setUserId(session.data.user.id);
          setToken(session.data.session.token);
        }
      } catch (err) {
        setError('Authentication failed');
      }
    };
    initAuth();
  }, []);

  const { control } = useChatKit({
    api: {
      url: `${CONFIG.API_BASE_URL}/api/${userId}/chat`,
      domainKey: process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY!,
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

  if (error) {
    return <div className="p-4 text-red-600">{error}</div>;
  }

  return children;
}
```
    maxReconnectAttempts: 5
  };
};
```

### ChatAssistant Template

```typescript
// frontend/src/components/chat/ChatAssistant.tsx
'use client';

import { ChatKit } from '@openai/chatkit-react';
import { useState, useEffect } from 'react';
import { X } from 'lucide-react';

interface ChatAssistantProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export function ChatAssistant({ isOpen = false, onClose }: ChatAssistantProps) {
  const [isExpanded, setIsExpanded] = useState(isOpen);

  useEffect(() => {
    setIsExpanded(isOpen);
  }, [isOpen]);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isExpanded) {
        handleClose();
      }
    };
    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isExpanded]);

  const handleClose = () => {
    setIsExpanded(false);
    onClose?.();
  };

  return (
    <>
      {isExpanded && (
        <div
          className="fixed inset-0 bg-black/20 z-40"
          onClick={handleClose}
        />
      )}
      <div
        className={`
          fixed top-0 right-0 h-full bg-white shadow-2xl z-50
          transition-transform duration-300
          ${isExpanded ? 'translate-x-0' : 'translate-x-full'}
          w-full md:w-[400px] lg:w-[500px]
        `}
      >
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-semibold">AI Assistant</h2>
          <button onClick={handleClose} className="p-2 hover:bg-gray-100 rounded">
            <X className="w-5 h-5" />
          </button>
        </div>
        <div className="h-[calc(100%-64px)]">
          {/* ChatKit component will be rendered here via control prop */}
        </div>
      </div>
    </>
  );
}
```

### Tasks Page Template

```typescript
// frontend/src/app/tasks/page.tsx
'use client';

import { ChatProvider } from '@/components/ChatProvider';
import { ChatAssistant, useChatSidebar } from '@/components/chat/ChatAssistant';
import { TaskList } from '@/components/TaskList';
import { MessageSquare } from 'lucide-react';

export default function TasksPage() {
  const { isOpen, open, close } = useChatSidebar();

  return (
    <ChatProvider>
      <div className="min-h-screen">
        <button onClick={open} className="fixed bottom-6 right-6">
          <MessageSquare /> AI Assistant
        </button>
        <TaskList />
        <ChatAssistant isOpen={isOpen} onClose={close} />
      </div>
    </ChatProvider>
  );
}
```

## Testing Strategy

### Unit Tests

```bash
# Run unit tests
pnpm test

# Run with coverage
pnpm test:coverage
```

Test files to create:
- `frontend/tests/components/ChatWindow.test.tsx`
- `frontend/tests/components/ChatInput.test.tsx`
- `frontend/tests/components/ChatMessage.test.tsx`
- `frontend/tests/lib/chat-service.test.ts`

### Integration Tests

```bash
# Run integration tests
pnpm test:integration
```

Test files to create:
- `frontend/tests/integration/chat-flow.test.tsx`

### E2E Tests

```bash
# Run E2E tests
pnpm test:e2e
```

Test files to create:
- `frontend/tests/e2e/chat.spec.ts`

## Common Issues & Solutions

### Issue 1: ChatKit Connection Fails

**Symptom**: ChatKit fails to connect, shows connection error

**Solution**:
1. Verify ChatKit credentials in `.env.local`
2. Check backend token endpoint is accessible
3. Verify JWT token is valid
4. Check browser console for detailed error

### Issue 2: Messages Not Displaying

**Symptom**: Messages sent but not appearing in chat window

**Solution**:
1. Check ChatKit event listeners are set up
2. Verify state updates in ChatProvider component
3. Check message format matches interface
4. Verify conversation ID is correct

### Issue 3: Authentication Errors

**Symptom**: "Unauthorized" or "Token expired" errors

**Solution**:
1. Verify Better Auth session is active
2. Check JWT token in request headers
3. Verify backend token validation
4. Implement token refresh logic

### Issue 4: Performance Issues

**Symptom**: Slow rendering with many messages

**Solution**:
1. Implement message virtualization
2. Add pagination for message loading
3. Optimize re-renders with React.memo
4. Check for unnecessary state updates

## Development Workflow

### Daily Workflow

1. **Start Backend**
   ```bash
   cd backend
   uvicorn main:app --reload --port 7860
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   pnpm dev
   ```

3. **Run Tests** (in watch mode)
   ```bash
   pnpm test:watch
   ```

4. **Check Linting**
   ```bash
   pnpm lint
   ```

### Before Committing

```bash
# Run all checks
pnpm lint
pnpm test
pnpm build

# If all pass, commit
git add .
git commit -m "feat: implement ChatKit integration"
```

## Success Criteria Checklist

Use this checklist to verify implementation meets requirements:

- [ ] **FR-001**: Chat interface accessible at `/chat` route
- [ ] **FR-002**: ChatWindow displays messages correctly
- [ ] **FR-003**: ChatInput validates and sends messages
- [ ] **FR-004**: ChatKit client configured with JWT tokens
- [ ] **FR-005**: Messages sent to `/api/{user_id}/chat`
- [ ] **FR-006**: MCP tool responses displayed correctly
- [ ] **FR-007**: Stateless operation (JWT + userId per request)
- [ ] **FR-008**: User isolation enforced
- [ ] **FR-009**: Dev/prod environments supported
- [ ] **FR-010**: Authentication validated before sending
- [ ] **FR-011**: Conversation history fetched from backend
- [ ] **FR-012**: Edge cases handled (expired tokens, errors)
- [ ] **FR-013**: Exponential backoff implemented
- [ ] **FR-014**: Lazy loading implemented
- [ ] **FR-015**: Loading states and error feedback provided
- [ ] **FR-016**: Real-time streaming works
- [ ] **FR-017**: Connection pooling and reconnection logic

## Performance Targets

Verify these performance targets are met:

- [ ] **SC-007**: Page load < 2 seconds for 95% of users
- [ ] **SC-003**: Response time < 3 seconds for 90% of interactions
- [ ] **SC-014**: Error display < 1 second for 95% of errors
- [ ] **SC-012**: Real-time streaming for 95% of messages
- [ ] Memory usage < 100MB for 1000+ message conversations

## Next Steps

After completing implementation:

1. **Create tasks.md** using `/sp.tasks` command
2. **Implement TDD workflow**: Write tests → Get approval → Red → Green → Refactor
3. **Deploy to staging** for testing
4. **Gather user feedback**
5. **Iterate and improve**

## Resources

- **Specification**: `specs/005-specification-phase-iii/spec.md`
- **Plan**: `specs/005-specification-phase-iii/plan.md`
- **Data Model**: `specs/005-specification-phase-iii/data-model.md`
- **Contracts**: `specs/005-specification-phase-iii/contracts/`
- **Next.js Docs**: https://nextjs.org/docs
- **ChatKit Docs**: https://pusher.com/docs/chatkit
- **Better Auth Docs**: https://better-auth.com/docs

---

**Quickstart Status**: ✅ Complete
**Ready for Implementation**: ✅ Yes
**Estimated Duration**: 10 days
**Team Size**: 1-2 developers