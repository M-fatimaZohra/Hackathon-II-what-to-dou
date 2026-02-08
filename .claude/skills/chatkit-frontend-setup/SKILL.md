---
name: chatkit-frontend-setup
description: Automates the setup of the OpenAI ChatKit Advanced Integration. It creates the Auth-aware Provider and the Sidebar component.
---

# ChatKit Frontend Setup Skill

This skill automates the creation of two critical components for ChatKit Advanced Integration: an auth-aware ChatProvider and a sliding sidebar ChatAssistant component.

## Component 1: ChatProvider.tsx

**Purpose**: Wraps @openai/chatkit-react's ChatKitProvider with Better Auth JWT injection

**Location**: `frontend/src/components/ChatProvider.tsx`

**Implementation**:

```typescript
'use client';

import { ChatKitProvider } from '@openai/chatkit-react';
import { authClient } from '@/lib/auth-client';
import { CONFIG } from '@/lib/config';
import { ReactNode, useEffect, useState } from 'react';

interface ChatProviderProps {
  children: ReactNode;
}

export function ChatProvider({ children }: ChatProviderProps) {
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Validation: Check NEXT_PUBLIC_OPENAI_DOMAIN_KEY is available
  useEffect(() => {
    if (!process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY) {
      setError('NEXT_PUBLIC_OPENAI_DOMAIN_KEY is not configured');
      console.error('ChatKit SDK initialization failed: Missing NEXT_PUBLIC_OPENAI_DOMAIN_KEY');
      return;
    }
    setIsReady(true);
  }, []);

  // Async headers function to inject JWT from Better Auth
  const getHeaders = async () => {
    try {
      const session = await authClient.getSession();

      if (!session?.user?.id || !session?.accessToken) {
        throw new Error('No active session or missing user ID');
      }

      return {
        'Authorization': `Bearer ${session.accessToken}`,
        'Content-Type': 'application/json',
      };
    } catch (error) {
      console.error('Failed to get auth headers:', error);
      throw error;
    }
  };

  // Dynamically build baseUrl using CONFIG and user.id from session
  const getBaseUrl = async () => {
    try {
      const session = await authClient.getSession();

      if (!session?.user?.id) {
        throw new Error('User ID not available in session');
      }

      // Build baseUrl: CONFIG.API_BASE_URL + /api/{user_id}/chat
      return `${CONFIG.API_BASE_URL}/api/${session.user.id}/chat`;
    } catch (error) {
      console.error('Failed to build baseUrl:', error);
      throw error;
    }
  };

  // Error state rendering
  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded-md">
        <p className="text-red-800 font-semibold">ChatKit Configuration Error</p>
        <p className="text-red-600 text-sm">{error}</p>
      </div>
    );
  }

  // Loading state while validating environment
  if (!isReady) {
    return <div className="p-4">Initializing ChatKit...</div>;
  }

  return (
    <ChatKitProvider
      baseUrl={getBaseUrl}
      headers={getHeaders}
      domainKey={process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY!}
      onError={(error) => {
        console.error('ChatKit error:', error);
        setError(error.message);
      }}
    >
      {children}
    </ChatKitProvider>
  );
}
```

**Key Features**:
- ✅ Wraps @openai/chatkit-react's ChatKitProvider
- ✅ Async headers function retrieves JWT from authClient.getSession()
- ✅ Dynamic baseUrl construction using CONFIG.API_BASE_URL and user.id
- ✅ Environment validation for NEXT_PUBLIC_OPENAI_DOMAIN_KEY
- ✅ Error handling for missing session or configuration
- ✅ Loading state during initialization

---

## Component 2: ChatAssistant.tsx

**Purpose**: Sliding sidebar component that renders ChatKit's <ChatView />

**Location**: `frontend/src/components/chat/ChatAssistant.tsx`

**Implementation**:

```typescript
'use client';

import { ChatView } from '@openai/chatkit-react';
import { useState, useEffect } from 'react';
import { X } from 'lucide-react'; // or any icon library

interface ChatAssistantProps {
  conversationId?: string | null;
  onClose?: () => void;
}

export function ChatAssistant({ conversationId, onClose }: ChatAssistantProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  // Handle Escape key to close sidebar
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isExpanded) {
        setIsExpanded(false);
        onClose?.();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isExpanded, onClose]);

  const handleClose = () => {
    setIsExpanded(false);
    onClose?.();
  };

  return (
    <>
      {/* Backdrop overlay when expanded */}
      {isExpanded && (
        <div
          className="fixed inset-0 bg-black/20 z-40 transition-opacity duration-300"
          onClick={handleClose}
        />
      )}

      {/* Sliding sidebar */}
      <div
        className={`
          fixed top-0 right-0 h-full bg-white shadow-2xl z-50
          transition-transform duration-300 ease-in-out
          ${isExpanded ? 'translate-x-0' : 'translate-x-full'}
          w-full md:w-[400px] lg:w-[500px]
        `}
      >
        {/* Sidebar header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">AI Assistant</h2>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-100 rounded-md transition-colors"
            aria-label="Close chat"
          >
            <X className="w-5 h-5 text-gray-600" />
          </button>
        </div>

        {/* ChatView component */}
        <div className="h-[calc(100%-64px)] overflow-hidden">
          <ChatView
            conversationId={conversationId}
            className="h-full"
            placeholder="Ask me to manage your tasks..."
          />
        </div>
      </div>
    </>
  );
}

// Export hook for controlling sidebar state
export function useChatSidebar() {
  const [isOpen, setIsOpen] = useState(false);

  const open = () => setIsOpen(true);
  const close = () => setIsOpen(false);
  const toggle = () => setIsOpen(prev => !prev);

  return { isOpen, open, close, toggle };
}
```

**Key Features**:
- ✅ Sliding sidebar with Tailwind CSS transitions (< 300ms)
- ✅ Renders <ChatView /> component inside
- ✅ Handles collapsed vs expanded state
- ✅ Backdrop overlay when expanded
- ✅ Close button and Escape key support
- ✅ Responsive design (full screen mobile, 400-500px desktop)
- ✅ Includes useChatSidebar hook for state management

---

## Usage in Tasks Page

**Location**: `frontend/src/app/tasks/page.tsx`

**Implementation**:

```typescript
'use client';

import { ChatProvider } from '@/components/ChatProvider';
import { ChatAssistant, useChatSidebar } from '@/components/chat/ChatAssistant';
import { TaskList } from '@/components/TaskList';
import { MessageSquare } from 'lucide-react';

export default function TasksPage() {
  const { isOpen, open, close } = useChatSidebar();

  return (
    <ChatProvider>
      <div className="container mx-auto p-6">
        {/* Toggle button */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">My Tasks</h1>
          <button
            onClick={open}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            <MessageSquare className="w-5 h-5" />
            AI Assistant
          </button>
        </div>

        {/* Task list */}
        <TaskList />

        {/* Chat sidebar */}
        {isOpen && <ChatAssistant onClose={close} />}
      </div>
    </ChatProvider>
  );
}
```

---

## Validation Logic

**Environment Check**: The ChatProvider component includes validation to ensure `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` is available before initializing the SDK.

**Validation Flow**:
1. On component mount, check if `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` exists
2. If missing: Display error message and log to console
3. If present: Set `isReady` to true and proceed with initialization
4. During runtime: Validate session exists before building headers/baseUrl
5. On error: Display user-friendly error message and log details

**Error States Handled**:
- Missing NEXT_PUBLIC_OPENAI_DOMAIN_KEY
- No active session (user not authenticated)
- Missing user ID in session
- JWT token retrieval failure
- ChatKit SDK initialization errors

---

## Usage Rules

1. **ALWAYS validate environment variables** before SDK initialization
2. **NEVER hardcode API URLs** - use CONFIG.API_BASE_URL from config.ts
3. **ALWAYS use async functions** for headers and baseUrl (they fetch session data)
4. **ALWAYS handle authentication errors** gracefully with user feedback
5. **ALWAYS wrap the tasks page** with ChatProvider before using ChatAssistant
6. **ALWAYS implement keyboard shortcuts** (Escape key) for accessibility
7. **ALWAYS use responsive design** (mobile: full screen, desktop: fixed width)

---

## Dependencies Required

```json
{
  "dependencies": {
    "@openai/chatkit-react": "latest",
    "lucide-react": "latest"
  }
}
```

---

## Environment Variables Required

```env
# .env.local
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_domain_key_here
NEXT_PUBLIC_MOD=developer
NEXT_PUBLIC_API_URL=http://localhost:7860
NEXT_PUBLIC_BASE_URL=http://localhost:3000
```

---

## Testing Checklist

- [ ] ChatProvider validates NEXT_PUBLIC_OPENAI_DOMAIN_KEY on mount
- [ ] ChatProvider fetches JWT from authClient.getSession()
- [ ] ChatProvider builds baseUrl with user.id from session
- [ ] ChatAssistant sidebar slides in/out smoothly (< 300ms)
- [ ] ChatAssistant renders <ChatView /> correctly
- [ ] Escape key closes sidebar
- [ ] Click outside (backdrop) closes sidebar
- [ ] Responsive design works on mobile and desktop
- [ ] Error states display user-friendly messages
- [ ] Authentication errors trigger re-authentication prompt
