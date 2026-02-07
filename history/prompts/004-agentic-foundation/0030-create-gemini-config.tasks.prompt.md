---
id: 0030
title: create-gemini-config
stage: tasks
date: 2026-02-04
surface: agent
model: haiku-4-5
feature: 004-agentic-foundation
branch: 004-agentic-foundation
user: user
command: /sp.implement
labels: ["config", "gemini", "agents", "setup"]
links:
  spec: specs/004-agentic-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/configs/gemini_config.py
  - specs/004-agentic-foundation/tasks.md
tests:
  - null
---

## Prompt

# Goal: Create Gemini Model Configuration

Please create `backend/src/configs/gemini_config.py`.

### Requirements:
1. **Apply Skill:** Use the `openai-agents-core` logic to build the model configuration.
2. **Model Setup:** Use the `## 1. Gemini Model Configuration` procedure:
    - Initialize `AsyncOpenAI` with `base_url="https://generativelanguage.googleapis.com/v1beta/openai/"` and `api_key` from environment variables.
    - Set `set_tracing_disabled(True)`.
    - Define `GEMINI_MODEL` using `OpenAIChatCompletionsModel` with `model="gemini-2.0-flash"`.
3. **System Prompt:** Define a `SYSTEM_PROMPT` constant that identifies the agent as "TodoAssistant" and instructs it to use the task tools (create, list, update, delete, complete) based on user input.

## Response snapshot

Successfully created the gemini_config.py file with the required configuration:

1. **Applied the openai-agents-core skill** for model configuration as requested
2. **Implemented the Gemini Model Configuration** with:
   - AsyncOpenAI client initialized with the correct base URL for Gemini API
   - API key loaded from environment variables using os.getenv("GEMINI_API_KEY")
   - set_tracing_disabled(True) to prevent 401 errors without OpenAI key
   - GEMINI_MODEL defined using OpenAIChatCompletionsModel with "gemini-2.0-flash"
3. **Created the SYSTEM_PROMPT** that identifies the agent as "TodoAssistant" and instructs it to use the task tools based on user input
4. **Added proper imports** for all required modules including AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, os, and dotenv
5. **Loaded environment variables** using load_dotenv() to ensure the GEMINI_API_KEY is available
6. **Updated tasks.md** to mark T014 as completed

The gemini_config.py file is now ready for use by the chatbot service and follows the recommended patterns from the openai-agents-core skill.

## Outcome

- ✅ Impact: Created complete Gemini model configuration with proper API setup and system prompt
- 🧪 Tests: No tests affected by config file creation
- 📁 Files: Created backend/src/configs/gemini_config.py and updated tasks.md
- 🔁 Next prompts: Ready to continue with agent initialization and service implementation
- 🧠 Reflection: Configuration properly implements the openai-agents-core skill recommendations

## Evaluation notes (flywheel)

- Failure modes observed: None - config file created successfully with all requirements met
- Graders run and results (PASS/FAIL): Not applicable for configuration file creation
- Prompt variant (if applicable): Gemini model configuration task
- Next experiment (smallest change to try): Implement the chat service using this configuration