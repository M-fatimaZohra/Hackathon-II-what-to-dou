# What to Dou - Full Stack Todo Application

A modern, full-stack todo application featuring personal user accounts for secure, persistent task storage. This application combines a Next.js frontend with a FastAPI backend, providing users with a seamless task management experience across devices.

## Current Version: 2.0.0 (Full Stack)

The second major release of What to Dou transforms from a simple CLI application to a full-stack web application with:

- **Personal User Accounts**: Secure authentication with email/password registration
- **Persistent Storage**: Tasks stored in a PostgreSQL database with Neon
- **Modern UI**: Responsive Next.js interface with Tailwind CSS styling
- **Cross-Device Sync**: Access your tasks from any device with your account
- **Task Management**: Create, update, delete, and mark tasks as complete/incomplete
- **Search & Filter**: Find and organize tasks with advanced filtering options

This version delivers a complete task management solution with security and persistence as core features.

## Features

### Authentication & Security
- **User Registration**: Create accounts with email and password
- **Secure Login**: Protected access to personal task data
- **Session Management**: Automatic session handling
- **Data Isolation**: Users can only access their own tasks

### Task Management
- **Create Tasks**: Add new tasks with titles, descriptions, and priority levels
- **Update Tasks**: Modify existing task details anytime
- **Delete Tasks**: Remove tasks you no longer need
- **Toggle Completion**: Mark tasks as complete/incomplete with one click
- **Search & Filter**: Find tasks by keyword, priority, or completion status

### Technology Stack
- **Frontend**: Next.js 16 with App Router, TypeScript, Tailwind CSS
- **Backend**: FastAPI with Python, SQLModel ORM
- **Authentication**: Better Auth for secure user management
- **Database**: PostgreSQL with Neon for cloud hosting
- **Styling**: Responsive design with accessibility-focused UI components

## Getting Started

Visit the application at https://hackathon-ii-what-to-dou.vercel.app/ and sign up or log in to get started!

## Documentation

For detailed documentation about this application, including:
- How to use the application
- Features and capabilities
- Best practices and troubleshooting

Please refer to our detailed documentation in the `/.docs` directory:
- [Introduction and Getting Started](./.docs/how_to_use_application/introduction.md)
- [Features Overview](./.docs/features_of_app/task_management.md)
- [Authentication Features](./.docs/features_of_app/authentication.md)
- [Version 1.0.0 - CLI Application](./.docs/version_1_0_0/phase_1_birth_of_application.md)
- [Version 2.0.0 - Full Stack Migration](./.docs/version_2_0_0/phase_2_full_stack_migration.md)

## Contributing

We welcome contributions to enhance the functionality of What to Dou. Feel free to fork the repository, create a feature branch, and submit a pull request.

### Development Guidelines
- Follow the existing code style and patterns
- Write tests for new features
- Update documentation as needed
- Ensure cross-browser compatibility

## License

This project is open source and available under the MIT License.

---

**Author:** Fatima Zohra