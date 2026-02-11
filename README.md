# What to Dou - AI-Native Todo Application

A modern, AI-native todo application featuring personal user accounts, secure persistent task storage, and an intelligent AI chatbot. Users can log in and use the chatbot to personalize and manage their tasks through natural conversation — powered by OpenAI's agent framework with MCP tools.

## Current Version: 3.0.0 (AI Chatbot)

The third major release of What to Dou introduces an AI Chatbot that lets you manage tasks through conversation:

- **AI Chatbot Assistant**: Manage tasks by chatting — create, view, update, and complete tasks in natural language
- **Personalized Experience**: The AI understands your context and helps organize tasks based on your workflow
- **Real-time Streaming**: AI responses stream word-by-word via Server-Sent Events for instant feedback
- **Personal User Accounts**: Secure authentication with email/password registration
- **Persistent Storage**: Tasks stored in a PostgreSQL database with Neon
- **Modern UI**: Responsive Next.js interface with ChatKit SDK integration
- **Cross-Device Sync**: Access your tasks from any device with your account

This version transforms the app from a traditional task manager into an AI-native productivity platform.

## Features

### AI Chatbot
- **Conversational Task Management**: Say "Create a task to buy groceries" instead of filling forms
- **Natural Language Queries**: Ask "What are my incomplete tasks?" for instant summaries
- **Smart Actions**: Update, complete, or delete tasks through conversation
- **Streaming Responses**: AI replies appear word-by-word as they're generated
- **Chat/History Toggle**: Switch between current conversation and past chat history

### Authentication & Security
- **User Registration**: Create accounts with email and password
- **Secure Login**: Protected access to personal task data
- **Session Management**: Automatic session handling with JWT tokens
- **Data Isolation**: Users can only access their own tasks — AI included

### Task Management
- **Create Tasks**: Add new tasks with titles, descriptions, and priority levels
- **Update Tasks**: Modify existing task details anytime
- **Delete Tasks**: Remove tasks you no longer need
- **Toggle Completion**: Mark tasks as complete/incomplete with one click
- **Search & Filter**: Find tasks by keyword, priority, or completion status

### Technology Stack
- **Frontend**: Next.js 16 with App Router, TypeScript, Tailwind CSS, ChatKit v1.5.0
- **Backend**: FastAPI with Python, SQLModel ORM, OpenAI Agents SDK
- **AI Layer**: OpenAI Agents SDK with MCP (Model Context Protocol) tools
- **Authentication**: Better Auth for secure user management
- **Database**: PostgreSQL with Neon for cloud hosting
- **Streaming**: Server-Sent Events (SSE) with OpenAI Responses API protocol

## Getting Started

Visit the application at https://hackathon-ii-what-to-dou.vercel.app/ and sign up or log in to get started!

Once logged in, click the **AI Assistant** button on the tasks page to open the chatbot and start managing your tasks through conversation.

## Documentation

For detailed documentation about this application, including:
- How to use the application
- Features and capabilities
- Best practices and troubleshooting

Please refer to our detailed documentation in the `/.docs` directory:
- [Introduction and Getting Started](./.docs/how_to_use_application/introduction.md)
- [Features Overview](./.docs/features_of_app/task_management.md)
- [Authentication Features](./.docs/features_of_app/authentication.md)
- [AI Chatbot Features](./.docs/features_of_app/ai_chatbot.md)
- [Version 1.0.0 - CLI Application](./.docs/version_1_0_0/phase_1_birth_of_application.md)
- [Version 2.0.0 - Full Stack Migration](./.docs/version_2_0_0/phase_2_full_stack_migration.md)
- [Version 3.0.0 - AI Chatbot Integration](./.docs/version_3_0_0/phase_3_ai_chatbot_integration.md)

## Version History

| Version | Phase | Description |
|---------|-------|-------------|
| 1.0.0 | CLI Application | In-memory task management via command line |
| 2.0.0 | Full Stack Migration | Web app with auth, PostgreSQL, and cross-device sync |
| 2.0.1 | Production Release | Deployed to production with security hardening |
| **3.0.0** | **AI Chatbot Integration** | **Conversational AI for personalized task management** |

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
