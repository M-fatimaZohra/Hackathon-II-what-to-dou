# UI Components: AI Native Todo Application

## Overview
This document specifies the reusable UI components for the AI Native Todo Application. The components follow a consistent design system using Tailwind CSS for styling, with clear interfaces and proper TypeScript typing. All components are designed to be responsive and accessible.

## Component Categories

### 1. Authentication Components

#### AuthProvider
**Purpose**: Provides authentication context to the application
**Location**: `src/providers/auth-provider.tsx`
**Props**: None
**Context Provided**:
- `user`: Current user object or null
- `loading`: Authentication loading state
- `login`: Login function
- `logout`: Logout function
- `signup`: Signup function

#### LoginForm
**Purpose**: Handles user login functionality
**Location**: `src/components/auth/login-form.tsx`
**Props**:
- `onSuccess`: Callback function called after successful login
- `onError`: Callback function called after login error
- `showSignupLink`: Whether to show link to signup page (default: true)

**State**:
- `email`: User email input
- `password`: User password input
- `loading`: Submit button loading state
- `error`: Error message display

#### SignupForm
**Purpose**: Handles user registration functionality
**Location**: `src/components/auth/signup-form.tsx`
**Props**:
- `onSuccess`: Callback function called after successful signup
- `onError`: Callback function called after signup error
- `showLoginLink`: Whether to show link to login page (default: true)

**State**:
- `email`: User email input
- `password`: User password input
- `confirmPassword`: Password confirmation input
- `loading`: Submit button loading state
- `error`: Error message display

#### LoginButton
**Purpose**: Provides a login button that triggers authentication flow
**Location**: `src/components/auth/login-button.tsx`
**Props**:
- `children`: Button content (default: "Login")
- `variant`: Button style variant (primary, secondary, ghost)
- `className`: Additional CSS classes

#### LogoutButton
**Purpose**: Provides a logout button that triggers logout flow
**Location**: `src/components/auth/logout-button.tsx`
**Props**:
- `children`: Button content (default: "Logout")
- `variant`: Button style variant (primary, secondary, ghost)
- `className`: Additional CSS classes

### 2. Task Components

#### TaskList
**Purpose**: Displays a list of tasks with filtering and search capabilities
**Location**: `src/components/tasks/task-list.tsx`
**Props**:
- `tasks`: Array of task objects to display
- `onTaskClick`: Callback when a task is clicked
- `onTaskToggle`: Callback when task completion is toggled
- `onTaskDelete`: Callback when task is deleted
- `loading`: Whether the task list is loading
- `emptyMessage`: Message to show when no tasks exist (default: "No tasks found")

**State**:
- `filter`: Current filter state (all, completed, incomplete)
- `searchQuery`: Current search query
- `priorityFilter`: Priority filter (all, low, medium, high, urgent)

#### TaskItem
**Purpose**: Displays a single task with interactive elements
**Location**: `src/components/tasks/task-item.tsx`
**Props**:
- `task`: Task object to display
- `onToggle`: Callback when task completion is toggled
- `onEdit`: Callback when task edit is requested
- `onDelete`: Callback when task delete is requested
- `showActions`: Whether to show action buttons (default: true)

**State**:
- `isHovered`: Whether the task item is being hovered
- `showDeleteConfirm`: Whether to show delete confirmation

#### TaskForm
**Purpose**: Form for creating or editing tasks
**Location**: `src/components/tasks/task-form.tsx`
**Props**:
- `initialData`: Initial task data for editing (optional)
- `onSubmit`: Callback when form is submitted
- `onCancel`: Callback when form is cancelled
- `submitText`: Text for submit button (default: "Save Task")

**State**:
- `title`: Task title input
- `description`: Task description input
- `priority`: Task priority selection
- `errors`: Form validation errors
- `submitting`: Submit button loading state

#### TaskDetail
**Purpose**: Displays detailed information about a single task
**Location**: `src/components/tasks/task-detail.tsx`
**Props**:
- `task`: Task object to display
- `onEdit`: Callback when edit is requested
- `onBack`: Callback when back button is clicked

### 3. UI Components

#### Button
**Purpose**: Reusable button component with various styles
**Location**: `src/components/ui/button.tsx`
**Props**:
- `variant`: Style variant (primary, secondary, ghost, link) (default: primary)
- `size`: Size variant (sm, md, lg) (default: md)
- `loading`: Whether button is in loading state
- `disabled`: Whether button is disabled
- `children`: Button content
- `onClick`: Click handler
- `className`: Additional CSS classes

#### Input
**Purpose**: Reusable input component with validation
**Location**: `src/components/ui/input.tsx`
**Props**:
- `type`: Input type (text, email, password, etc.) (default: text)
- `placeholder`: Input placeholder text
- `value`: Input value
- `onChange`: Change handler
- `error`: Error message to display
- `label`: Label text (optional)
- `required`: Whether field is required
- `className`: Additional CSS classes

#### Select
**Purpose**: Reusable select component
**Location**: `src/components/ui/select.tsx`
**Props**:
- `options`: Array of option objects {value: string, label: string}
- `value`: Current selected value
- `onChange`: Change handler
- `placeholder`: Placeholder text
- `error`: Error message to display
- `label`: Label text (optional)
- `className`: Additional CSS classes

#### Modal
**Purpose**: Reusable modal component
**Location**: `src/components/ui/modal.tsx`
**Props**:
- `isOpen`: Whether modal is open
- `onClose`: Close handler
- `title`: Modal title
- `children`: Modal content
- `size`: Modal size (sm, md, lg, xl) (default: md)

#### LoadingSpinner
**Purpose**: Loading indicator component
**Location**: `src/components/ui/loading-spinner.tsx`
**Props**:
- `size`: Spinner size (sm, md, lg) (default: md)
- `className`: Additional CSS classes

#### Alert
**Purpose**: Alert message component for notifications
**Location**: `src/components/ui/alert.tsx`
**Props**:
- `type`: Alert type (success, error, warning, info) (default: info)
- `message`: Alert message content
- `showIcon`: Whether to show icon (default: true)
- `onClose`: Close handler (optional)
- `className`: Additional CSS classes

### 4. Layout Components

#### Header
**Purpose**: Application header with navigation and user controls
**Location**: `src/components/layout/header.tsx`
**Props**: None
**State**:
- `mobileMenuOpen`: Whether mobile menu is open

#### Navigation
**Purpose**: Main navigation menu
**Location**: `src/components/layout/navigation.tsx`
**Props**:
- `items`: Array of navigation items {name: string, href: string, current: boolean}

#### ProtectedRoute
**Purpose**: Wrapper component that requires authentication
**Location**: `src/components/layout/protected-route.tsx`
**Props**:
- `children`: Content to render when authenticated
- `fallback`: Fallback content when not authenticated (default: redirect to login)

#### Layout
**Purpose**: Main application layout with header, sidebar, and content
**Location**: `src/components/layout/layout.tsx`
**Props**:
- `children`: Main content
- `sidebar`: Sidebar content (optional)
- `header`: Custom header (optional)

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

## Design System

### Color Palette
- **Primary**: `#3B82F6` (blue-500) - Primary actions and highlights
- **Secondary**: `#6B7280` (gray-500) - Secondary actions and text
- **Success**: `#10B981` (emerald-500) - Success states and positive actions
- **Warning**: `#F59E0B` (amber-500) - Warning states
- **Error**: `#EF4444` (red-500) - Error states and destructive actions
- **Background**: `#FFFFFF` (white) - Main background
- **Surface**: `#F9FAFB` (gray-50) - Secondary surfaces
- **Text**: `#1F2937` (gray-800) - Primary text
- **Text Secondary**: `#6B7280` (gray-500) - Secondary text

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