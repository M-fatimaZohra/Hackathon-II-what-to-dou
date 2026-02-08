# UI Pages: AI Native Todo Application

## Overview
This document specifies the pages for the AI Native Todo Application. Each page is designed to serve a specific user need and follows the overall design system. Pages are built using the Next.js App Router with proper routing, data fetching, and error handling.

## Page Structure

### Authentication Pages

#### Sign In Page
**Path**: `/signin`
**Purpose**: Allow users to sign in to their accounts
**Components Used**:
- Components from `src/components/` (TaskList, TaskForm, etc.)

**Features**:
- Email and password input fields
- Form validation
- Loading state during authentication
- Link to sign up page
- Error messaging for failed authentication attempts

**Data Requirements**:
- None (public page)

**User Flow**:
1. User enters email and password
2. Form validation occurs
3. Better Auth API is called
4. On success: redirect to tasks page
5. On failure: show error message

#### Sign Up Page
**Path**: `/signup`
**Purpose**: Allow new users to create accounts
**Components Used**:
- `Layout` (header, navigation)
- `SignupForm`
- `Alert` (for error messages)

**Features**:
- Email and password input fields
- Password confirmation
- Form validation
- Loading state during registration
- Link to login page
- Error messaging for failed registration attempts
- Terms of service agreement (optional)

**Data Requirements**:
- None (public page)

**User Flow**:
1. User enters email and password
2. Form validation occurs
3. Registration API is called
4. On success: automatically log in and redirect to onboarding/dashboard
5. On failure: show error message

#### Forgot Password Page
**Path**: `/forgot-password`
**Purpose**: Allow users to reset their passwords
**Components Used**:
- `Layout` (header, navigation)
- `Input` (for email)
- `Button`
- `Alert` (for messages)

**Features**:
- Email input field
- Form validation
- Loading state during request
- Success message after password reset request
- Link to login page

**Data Requirements**:
- None (public page)

**User Flow**:
1. User enters email address
2. Form validation occurs
3. Password reset API is called
4. On success: show confirmation message
5. On failure: show error message

### Dashboard and Task Management Pages


#### Task List Page
**Path**: `/tasks`
**Purpose**: Display all user tasks with filtering, search capabilities, and AI chat sidebar overlay
**Components Used**:
- `Layout` (header, navigation)
- `ProtectedRoute`
- `TaskList`
- `ChatProvider` (component using useChatKit hook)
- `ChatAssistant` (sidebar overlay with ChatKit SDK)
- `Input` (for search)
- `Select` (for priority filter)
- `Button` (for new task and chat toggle)

**Features**:
- Search functionality
- Priority filtering
- Completion status filtering
- Sort options
- Pagination (if needed)
- Add new task button
- **AI Chat Sidebar Overlay** (Phase III):
  - Persistent sidebar overlay using ChatKit SDK
  - Toggle button to open/close chat
  - Real-time chat with AI agent via SSE streaming
  - JWT authentication via Better Auth
  - Stateless operation (JWT + userId per request)
  - User isolation (all requests scoped to `/api/{user_id}/`)
  - Natural language task management
  - Multi-turn conversation support
- Empty state when no tasks exist
- Loading state during data fetch

**Data Requirements**:
- Authenticated user
- User's tasks with filtering options
- Filter and sort parameters
- JWT token from `authClient.getSession()` for chat
- ChatKit configuration with baseUrl scoped to `/api/{user_id}/chat`

**User Flow**:
1. User navigates to tasks page
2. Page checks authentication via Better Auth
3. If not authenticated: redirect to `/signin`
4. Fetches user's tasks with applied filters
5. Displays tasks in list format
6. **Chat Sidebar Flow** (Phase III):
   - User clicks chat toggle button
   - Sidebar overlay slides in from right
   - ChatProvider initializes with JWT token via custom fetch function
   - ChatAssistant component renders using `<ChatKit />` from `@openai/chatkit-react` with control prop
   - Backend fetches conversation history from Neon DB
   - User types message (e.g., "Create a task to buy groceries")
   - Message sent to `/api/{user_id}/chat` with JWT + userId
   - Backend processes via ChatKitServer → Agent SDK → MCP tools
   - Response streamed via SSE in real-time (TTFT < 500ms)
   - MCP tool response displayed (e.g., "Task created successfully: Buy groceries")
   - Task list automatically updates to show new task
   - User can close sidebar or continue conversation
7. Allows user to interact with tasks (edit, delete, toggle)

**Error Handling**:
- Network errors: Retry with exponential backoff
- Authentication errors: Prompt re-authentication
- Token expiration: Refresh or redirect to signin
- Backend unavailable: Show error with retry option
- Validation errors: Show inline error messages
- SSE connection errors: Automatic reconnection with status indicator

**Performance Targets**:
- Page load: < 2 seconds
- Time to First Token (TTFT): < 500ms for 90% of chat interactions
- SSE streaming: 95% of messages
- Sidebar overlay animation: < 300ms




### Profile and Settings Pages

#### Profile Page
**Path**: `/profile`
**Purpose**: Allow users to view and update their profile information
**Components Used**:
- `Layout` (header, navigation)
- `ProtectedRoute`
- `Input`
- `Button`

**Features**:
- View current profile information
- Update profile information form
- Change password functionality
- Account deletion option (optional)
- Loading state during updates

**Data Requirements**:
- Authenticated user
- User profile data

**User Flow**:
1. User navigates to profile page
2. Page checks authentication
3. Fetches user profile data
4. Displays profile information
5. Allows user to update information

#### Settings Page
**Path**: `/settings`
**Purpose**: Allow users to configure application settings
**Components Used**:
- `Layout` (header, navigation)
- `ProtectedRoute`
- `Select`
- `Input`
- `Button`

**Features**:
- Theme selection (light/dark mode)
- Notification preferences
- Privacy settings
- Data export options (optional)
- Loading state during updates

**Data Requirements**:
- Authenticated user
- User settings data

**User Flow**:
1. User navigates to settings page
2. Page checks authentication
3. Fetches user settings
4. Displays settings form
5. Allows user to update settings

## Page Navigation

### Public Routes
- `/signin` - Sign in page
- `/signup` - Sign up page
- `/forgot-password` - Password reset
- `/` - Landing page (redirects to tasks if authenticated)

### Protected Routes
- `/tasks` - Task list with AI chat sidebar overlay for authenticated users
- `/profile` - User profile for authenticated users
- `/settings` - User settings for authenticated users

## Error Handling

### 404 Page
**Path**: `/not-found`
**Purpose**: Handle non-existent routes
**Components Used**:
- Simple layout with error message
- Link back to dashboard or home
- Search functionality to find content

### 500 Page
**Path**: `/error`
**Purpose**: Handle server-side errors
**Components Used**:
- Simple layout with error message
- Link back to dashboard or home
- Contact support information

### Authentication Error
**Path**: N/A (handled by redirect)
**Purpose**: Handle unauthenticated access to protected routes
**Behavior**: Redirect to login page with return URL parameter

## Loading States

### Global Loading
- Loading spinner during initial page load
- Skeleton screens for content areas
- Progress indicators for form submissions

### Component Loading
- Loading states for individual components
- Button loading states during API calls
- Data fetching indicators

## SEO and Metadata

### Page Titles
- Dynamic page titles based on content
- Consistent branding in titles
- Descriptive titles for search engines

### Meta Descriptions
- Relevant meta descriptions for each page
- Dynamic descriptions based on content
- Consistent branding in descriptions

### Open Graph Tags
- Social media sharing optimization
- Consistent image and description across pages
- Dynamic tags based on page content

## Accessibility

### Page Structure
- Proper heading hierarchy (h1, h2, h3, etc.)
- Semantic HTML elements
- Proper landmark regions

### Navigation
- Skip navigation link for screen readers
- Logical tab order
- Keyboard accessible menus

### Content
- Alt text for images
- Proper ARIA attributes
- Color contrast compliance
- Focus indicators for interactive elements

## Performance

### Data Fetching
- Optimize data fetching for each page
- Implement proper caching strategies
- Use Next.js data fetching methods appropriately (getServerSideProps, getStaticProps, etc.)

### Code Splitting
- Leverage Next.js automatic code splitting
- Dynamic imports for large components
- Optimize bundle sizes per page

### Image Optimization
- Use Next.js Image component
- Proper image sizing and formats
- Lazy loading for images below the fold