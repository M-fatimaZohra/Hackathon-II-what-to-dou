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

### 2. AI Chatbot Components (Phase III: Agentic Foundation)

#### ChatInterface
**Purpose**: Main chat interface for interacting with the AI agent
**Location**: `src/components/chat/chat-interface.tsx`
**Props**:
- `userId`: String, required - The ID of the authenticated user
- `onTaskCreated`: Callback when AI creates a task
- `onTaskUpdated`: Callback when AI updates a task
- `onTaskDeleted`: Callback when AI deletes a task
- `onConversationStart`: Callback when new conversation starts
- `onConversationEnd`: Callback when conversation ends

**State**:
- `messages`: Array of chat messages (user and AI)
- `inputValue`: Current user input text
- `isLoading`: Whether AI is processing the request
- `conversationId`: Current conversation ID (null for new conversation)
- `error`: Error message if chat fails

#### ChatMessage
**Purpose**: Displays a single chat message from user or AI
**Location**: `src/components/chat/chat-message.tsx`
**Props**:
- `message`: Message object with content, role (user/assistant), and timestamp
- `isOwnMessage`: Whether this is the current user's message
- `showAvatar`: Whether to show avatar (default: true)

**State**:
- `isExpanded`: Whether long messages are expanded

#### ChatInput
**Purpose**: Input field for sending messages to the AI agent
**Location**: `src/components/chat/chat-input.tsx`
**Props**:
- `value`: Current input value
- `onChange`: Handler for input changes
- `onSend`: Handler for sending message
- `disabled`: Whether input is disabled (default: false)
- `placeholder`: Input placeholder text (default: "Type your task request...")

**State**:
- `isFocused`: Whether input is focused

#### ConversationHistory
**Purpose**: Displays conversation history and allows switching between conversations
**Location**: `src/components/chat/conversation-history.tsx`
**Props**:
- `conversations`: Array of conversation objects
- `onConversationSelect`: Callback when conversation is selected
- `onConversationDelete`: Callback when conversation is deleted
- `loading`: Whether conversations are loading

**State**:
- `selectedConversationId`: Currently selected conversation ID
- `showDeleteConfirm`: Whether to show delete confirmation

#### TaskSuggestion
**Purpose**: Displays suggested tasks based on AI interpretation of user input
**Location**: `src/components/chat/task-suggestion.tsx`
**Props**:
- `suggestions`: Array of suggested tasks
- `onAccept`: Callback when suggestion is accepted
- `onReject`: Callback when suggestion is rejected
- `showActions`: Whether to show accept/reject buttons (default: true)

**State**:
- `accepted`: Whether the suggestion has been accepted



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