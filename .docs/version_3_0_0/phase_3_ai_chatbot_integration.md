# What to Dou App - Version 3.0.0 Documentation

## Overview

The "what-to-dou" app has evolved from a full-stack web application into an AI-native task management platform. Version 3.0.0 introduces an intelligent AI Chatbot that allows users to manage their tasks through natural conversation. Users can log in to their personal accounts and use the chatbot to create, update, organize, and personalize their tasks — all through a conversational interface powered by OpenAI's agent framework.

**Author:** Fatima Zohra
**Version:** 3.0.0 (AI Chatbot Integration)
**Date of Update:** February 11, 2026

## What's New in Version 3.0.0

### Core Additions
- **AI Chatbot Assistant:** A conversational AI sidebar that understands natural language for task management
- **Personalized Task Management:** The chatbot learns your context and helps organize tasks based on your workflow
- **Agentic Architecture:** Backend powered by OpenAI Agents SDK with MCP (Model Context Protocol) tools for direct database operations
- **Real-time Streaming:** Server-Sent Events (SSE) deliver AI responses word-by-word for a responsive experience
- **ChatKit UI Integration:** OpenAI's ChatKit SDK provides the chat interface with familiar messaging aesthetics

### Enhanced User Experience
- **Conversational Task Creation:** Tell the chatbot "Add a task to buy groceries" instead of filling forms
- **Natural Language Queries:** Ask "What tasks are due today?" or "Show me my high priority items"
- **Smart Organization:** The AI suggests priorities and helps categorize tasks
- **Instant Feedback:** User messages appear immediately; AI responses stream in real-time
- **Dual View Mode:** Switch between Chat and History views within the sidebar

## Technical Architecture

### AI Integration Stack
- **Frontend:** Next.js 16 with ChatKit v1.5.0 (OpenAI's chat UI SDK)
- **Backend:** FastAPI with OpenAI Agents SDK for agentic AI workflows
- **Protocol:** MCP (Model Context Protocol) connecting AI agents to task database tools
- **Streaming:** Server-Sent Events (SSE) with OpenAI Responses API protocol
- **Authentication:** Better Auth with JWT cookies for secure chatbot sessions

### Key Components
- **ChatProvider:** React context provider managing ChatKit configuration, JWT injection, and SSE stream processing
- **ChatAssistant:** Sidebar component with ChatKit rendering, custom message overlay, and Chat/History view toggle
- **Chat API Endpoint:** FastAPI SSE streaming endpoint with 7-event Atomic Response Initialization protocol
- **MCP Server:** FastMCP server exposing task CRUD tools (create, list, update, delete, complete)
- **Chat Service:** Agent orchestration layer connecting user messages to MCP tool execution

### Streaming Protocol (7-Event Atomic Response)
1. `thread.created` — Establishes conversation thread
2. `conversation.item.created` — Registers user message
3. `response.created` — Initializes AI response with pre-populated output
4. `response.output_text.delta` — Streams AI text word-by-word (repeated)
5. `response.output_text.done` — Signals text completion
6. `response.output_item.done` — Finalizes response item
7. `response.done` — Completes response with full output for fallback rendering

## How It Works

### User Workflow
1. **Login:** Users sign in with their existing account (email and password)
2. **Open Chatbot:** Click the AI Assistant button to open the chat sidebar
3. **Converse:** Type natural language messages to manage tasks
4. **View Results:** See AI responses with task confirmations and information
5. **Switch Views:** Toggle between Chat (messages) and History (past conversations)
6. **Close:** Dismiss the sidebar when done; tasks persist in the database

### Conversation Examples
- "Create a task called 'Prepare presentation' with high priority"
- "Show me all my incomplete tasks"
- "Mark the grocery shopping task as complete"
- "What tasks do I have for this week?"
- "Delete the old meeting notes task"

### System Flow
1. User types a message in the ChatKit input bar
2. Frontend intercepts the request, injects JWT authentication, and sends to backend
3. Backend receives the message and routes it to the AI agent
4. AI agent analyzes intent and executes appropriate MCP tools (create/list/update/delete tasks)
5. Agent generates a natural language response based on tool results
6. Response streams back via SSE events
7. Frontend renders the response in the custom message overlay

## Features and Capabilities

### Chatbot Features
- **Task Creation via Chat:** Create tasks with title, description, and priority through conversation
- **Task Queries:** Ask about your tasks using natural language
- **Task Updates:** Modify tasks by describing the changes in plain English
- **Task Completion:** Mark tasks done by telling the chatbot
- **Task Deletion:** Remove tasks through conversational commands
- **Context Awareness:** The chatbot understands follow-up questions within a conversation

### UI Features
- **Sliding Sidebar:** Chat panel slides in from the right with smooth animation
- **ChatKit Header:** New chat and history icons from OpenAI's ChatKit SDK
- **Custom Message Bubbles:** User messages in light gray bubbles, assistant text in clean typography
- **View Toggle:** Chat/History tabs to switch between message view and ChatKit's native history panel
- **Auto-Scroll:** New messages automatically scroll into view
- **Responsive Design:** Full-screen on mobile, 400-500px sidebar on desktop
- **Keyboard Support:** Escape key to close the sidebar

### Security Features
- **Authenticated Sessions:** All chatbot requests carry JWT tokens
- **User Isolation:** AI agent only accesses the authenticated user's tasks
- **Secure Streaming:** SSE connections authenticated per-request
- **No Data Leakage:** Conversation context is scoped to the individual user

## Migration from Version 2.0.0

### What Changed
- Addition of AI chatbot sidebar on the tasks page
- New backend chat endpoint with SSE streaming
- MCP server connecting AI agents to task database
- ChatKit SDK integration in the frontend
- New conversation and message database tables

### What Stayed the Same
- All existing task management features (create, view, update, delete, toggle)
- Authentication system (Better Auth with email/password)
- Database structure (existing Task table unchanged)
- API endpoints for direct task management
- Responsive web interface and design

### Impact on Users
- Existing accounts work without any changes
- All previously created tasks remain intact
- The chatbot is an additional feature — traditional task management still works
- No migration or data conversion required

## Setup and Configuration

### Additional Prerequisites (beyond Version 2.0.0)
- OpenAI API key for agent processing (set as `GEMINI_API_KEY` or `GROQ_API_KEY` in backend `.env`)
- ChatKit CSS and JS loaded via CDN (automatic in frontend)

### Environment Variables (New)
- `GEMINI_API_KEY` or `GROQ_API_KEY` — API key for AI model access
- `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` — ChatKit domain identifier (optional, defaults to `localhost-dev`)

## Benefits

### For Users
- **Natural Interaction:** Manage tasks by talking to an AI instead of navigating forms
- **Faster Workflow:** Create multiple tasks in rapid succession through conversation
- **Personalized Help:** The AI understands context and provides relevant suggestions
- **Familiar Interface:** Chat UI feels like messaging apps users already know
- **No Learning Curve:** Existing features remain accessible alongside the chatbot

### For the Platform
- **AI-Native Architecture:** MCP-based agent framework ready for advanced AI features
- **Extensible Tools:** New MCP tools can be added to expand chatbot capabilities
- **Streaming Infrastructure:** SSE pipeline supports future real-time features
- **Modern Stack:** OpenAI Agents SDK positions the app at the frontier of AI integration

## Future Development Plans

### Upcoming Features
- **Voice Input:** Speak to the chatbot instead of typing
- **Smart Suggestions:** Proactive task recommendations based on patterns
- **Calendar Integration:** AI-assisted scheduling and deadline management
- **Team Collaboration:** Share conversations and task assignments
- **Multi-Model Support:** Switch between AI providers for different capabilities

### Long-term Vision
- **Autonomous Task Management:** AI proactively manages routine tasks
- **Workflow Automation:** Chain multiple actions through conversational commands
- **Analytics & Insights:** AI-generated productivity reports and trends
- **Plugin Ecosystem:** Third-party MCP tools for expanded functionality

## Conclusion

Version 3.0.0 transforms the what-to-dou app from a traditional task management tool into an AI-native platform. The integration of a conversational chatbot powered by OpenAI's agent framework and MCP tools creates a natural, intuitive way for users to manage their tasks. By maintaining all existing functionality while adding AI capabilities, this version delivers the best of both worlds — structured task management with the ease of natural conversation.

The agentic architecture and streaming infrastructure establish a foundation for increasingly intelligent features, positioning the what-to-dou app at the forefront of AI-powered productivity tools.

---
*Documentation created on February 11, 2026*
*Author: Fatima Zohra*
*Version: 3.0.0*
