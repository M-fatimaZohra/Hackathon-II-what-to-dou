# How to Use the What to Dou Web Application

## Introduction

The What to Dou app is a modern, full-stack web application designed for efficient task management with personal user accounts. This application allows you to create, manage, and track your tasks through an intuitive web interface with secure authentication, persistent storage, and cross-device synchronization.

## Getting Started

### Prerequisites
- Node.js 18+ for the frontend application
- Python 3.9+ for the backend services
- PostgreSQL database (Neon recommended)
- Package managers: npm for frontend, uv/pip for backend

### Installation and Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd what-to-dou
   ```

2. **Setup Backend:**
   ```bash
   cd backend
   uv sync --all-extras
   cp .env.example .env  # Update with your database credentials
   uv run alembic upgrade head  # Initialize database
   uv run python -m src.main
   ```

3. **Setup Frontend:**
   ```bash
   cd frontend
   npm install
   cp .env.local.example .env.local  # Update with your backend URL
   npm run dev
   ```

### Running the Application
- **Backend API:** `uv run python -m src.main` (runs on http://localhost:8000)
- **Frontend App:** `npm run dev` (runs on http://localhost:3000)
- Access the web application at http://localhost:3000

## Application Features

### 1. User Authentication
- **Sign Up:** Create a new account with email and password
- **Sign In:** Secure login to access your personal task list
- **Sign Out:** Secure logout with session termination
- **Session Management:** Automatic session handling with JWT tokens

### 2. Task Management
- **Create Tasks:** Add new tasks with title, description, and priority level
- **View Tasks:** See all your tasks in an organized list format
- **Update Tasks:** Modify existing task details anytime
- **Delete Tasks:** Remove tasks you no longer need
- **Toggle Completion:** Mark tasks as complete/incomplete with one click

### 3. Advanced Features
- **Search Tasks:** Find tasks by keyword in title or description
- **Filter Tasks:** Sort by priority level (low, medium, high, urgent) or completion status
- **Priority Levels:** Assign importance levels to tasks
- **Persistent Storage:** All tasks saved in the database permanently

## Best Practices

### For Optimal Use
- Use descriptive titles that clearly indicate the task purpose
- Add relevant details in the description field when needed
- Assign appropriate priority levels to important tasks
- Regularly review all tasks to maintain organization
- Log out properly when using shared computers

### Tips for Efficiency
- Add tasks immediately when they come to mind
- Use the search feature to quickly find specific tasks
- Filter by priority or completion status to focus on important items
- Organize tasks by assigning proper priority levels
- Use the toggle feature to track your progress

## Understanding the Interface

The application follows a modern, responsive web design approach:
1. **Navigation:** Clear navigation between different sections
2. **Task Forms:** Intuitive forms for creating and updating tasks
3. **Real-time Feedback:** Immediate updates after successful operations
4. **Error Handling:** User-friendly error messages when issues occur
5. **Responsive Design:** Optimized for desktop, tablet, and mobile devices

## Security Considerations

- **Personal Data:** Tasks are isolated to individual user accounts
- **Secure Authentication:** Passwords are encrypted and sessions are secured
- **Data Protection:** All data stored securely in PostgreSQL database
- **Session Management:** Automatic session expiration for security

## Troubleshooting

Common issues and solutions:
- **Login Issues:** Verify your email and password are correct
- **Task Not Found:** Check that you're signed in to the correct account
- **Connection Errors:** Ensure both frontend and backend servers are running
- **Database Issues:** Verify your database connection settings in .env file

## Next Steps

This full-stack implementation provides a solid foundation for advanced features. Future enhancements will include due dates, task sharing, notifications, and analytics to further improve your task management experience.