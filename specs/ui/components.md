# UI Components: AI Native Todo Application

## Overview
This document specifies the reusable UI components for the AI Native Todo Application. The components follow a consistent design system using Tailwind CSS for styling, with clear interfaces and proper TypeScript typing. All components are designed to be responsive and accessible.

## Component Categories


### 1. Task Components

#### TaskList
**Purpose**: Displays a list of tasks with filtering and search capabilities
**Location**: `src/components/TaskList.tsx`
**Props**: None (fetches tasks internally using apiClient)

**Features**:
- Displays all user tasks
- Search and filter capabilities
- Ability to add, edit, and delete tasks
- Toggle task completion status
- Loading and error states

#### TaskStatusToggle
**Purpose**: Toggle button for marking tasks as complete/incomplete
**Location**: `src/components/TaskStatusToggle.tsx`
**Props**:
- `taskId`: The ID of the task to toggle
- `completed`: Current completion status
- `onToggle`: Callback when toggle is clicked

**Features**:
- Visual indication of completion status
- Interactive toggle functionality
- Loading state during API calls

#### SearchFilter
**Purpose**: Provides search and filter functionality for task lists
**Location**: `src/components/SearchFilter.tsx`
**Props**:
- `onFilterChange`: Callback when filter parameters change

**Features**:
- Search input for task titles/descriptions
- Priority filter dropdown
- Completion status filter
- Real-time filtering as user types

#### TaskForm
**Purpose**: Form for creating or editing tasks
**Location**: `src/components/TaskForm.tsx`
**Props**: None (handles creation internally)

**Features**:
- Title input field
- Description text area
- Priority selection dropdown
- Form validation
- Loading state during submission
- Ability to add new tasks

### 2. AI Chatbot Components (Phase III: ChatKit Integration)

#### ChatProvider
**Purpose**: Component using useChatKit hook for ChatKit SDK integration with JWT authentication
**Location**: `src/components/ChatProvider.tsx`
**Props**:
- `children`: React.ReactNode

**Features**:
- Uses useChatKit hook from @openai/chatkit-react
- Configures custom fetch function for JWT authentication
- Configures baseUrl scoped to `/api/{user_id}/chat` with JWT verification
- Handles SSE connection management via SDK
- Implements error handling for authentication failures
- Enforces stateless operation and user isolation

#### ChatAssistant
**Purpose**: Wrapper component that integrates ChatKit SDK's `<ChatKit />` component for sidebar overlay
**Location**: `src/components/chat/ChatAssistant.tsx`
**Props**:
- `conversationId`: string | null - Current conversation ID
- `onClose`: () => void - Callback to close sidebar
- `isOpen`: boolean - Sidebar visibility state

**Features**:
- Uses `@openai/chatkit-react` SDK's `<ChatKit />` component with control prop
- Displays as persistent sidebar overlay on tasks page
- Handles message input and display via SDK
- Supports SSE streaming for real-time responses
- Receives control object from useChatKit hook
- No manual ChatWindow, ChatInput, or ChatMessage components needed

**SDK Integration**:
```typescript
import { ChatKit, useChatKit } from '@openai/chatkit-react';

export function ChatAssistant({ conversationId, onClose, isOpen }) {
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

  return (
    <div className="sidebar-overlay">
      <ChatKit control={control} className="h-full" />
      <button onClick={onClose}>Close</button>
    </div>
  );
}
```



### 3. Layout Components

#### Navigation
**Purpose**: Main navigation menu
**Location**: `src/components/Navigation.tsx`

**Features**:
- Navigation links to different parts of the application
- Mobile-responsive design
- Active link highlighting

## Component Interfaces

### Task Interface
```typescript
interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high' | 'urgent';
  created_at: string;
  updated_at: string;
}
```

### User Interface
```typescript
interface User {
  id: string;
  email: string;
  created_at: string;
}
```


### Typography
- **Heading 1**: `font-bold text-3xl` - Main page titles
- **Heading 2**: `font-bold text-2xl` - Section titles
- **Heading 3**: `font-bold text-xl` - Subsection titles
- **Body**: `text-base` - Main content text
- **Small**: `text-sm` - Secondary text and captions

### Spacing
- **Gap**: Use consistent spacing with Tailwind classes (gap-1, gap-2, gap-4, etc.)
- **Padding**: Use consistent padding (p-2, p-4, p-6, etc.)
- **Margin**: Use consistent margins (m-2, m-4, m-6, etc.)

### Responsive Design
- **Mobile**: Up to 640px - Single column layout
- **Tablet**: 641px to 1024px - Adapted layouts with some multi-column elements
- **Desktop**: 1025px and above - Full multi-column layouts

## Accessibility Guidelines

### Keyboard Navigation
- All interactive elements must be keyboard accessible
- Proper focus management for modals and dropdowns
- Logical tab order throughout the application

### Screen Reader Support
- Proper ARIA labels and descriptions
- Semantic HTML elements
- Skip links for main content

### Color Contrast
- Maintain WCAG AA contrast ratios (4.5:1 for normal text)
- Sufficient contrast for interactive elements
- Color should not be the only indicator of state

## State Management

### Component State
- Use React hooks (useState, useEffect, etc.) for component-level state
- Use context for application-wide state that affects multiple components
- Implement proper loading and error states for all data-dependent components

### Data Fetching
- Use custom hooks for data fetching operations
- Implement proper error handling and retry mechanisms
- Show loading states during data operations
- Cache frequently accessed data appropriately

## Testing Strategy

### Component Testing
- Test all components with Jest and React Testing Library
- Test component rendering with various props
- Test user interactions and state changes
- Test accessibility attributes and keyboard navigation

### Integration Testing
- Test component combinations and interactions
- Test data flow between components
- Test authentication flow integration
- Test API integration with components

## Performance Considerations

### Rendering Optimization
- Use React.memo for components that render frequently with same props
- Implement virtual scrolling for large lists
- Use lazy loading for non-critical components
- Optimize images and assets

### Bundle Size
- Implement code splitting where appropriate
- Use tree-shaking to remove unused code
- Optimize dependencies and consider alternatives for heavy libraries
- Implement dynamic imports for large components

## Component Composition

### Higher-Order Components
- Create HOCs for common functionality (authentication check, loading states)
- Use render props for flexible component composition
- Implement custom hooks for reusable logic

### Compound Components
- Create component groups that work together (e.g., Accordion, Tabs)
- Share state between related components
- Provide consistent APIs across component families