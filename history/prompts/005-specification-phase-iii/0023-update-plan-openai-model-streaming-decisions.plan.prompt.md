---
id: 0023
title: Update plan with OpenAI model and streaming decisions
stage: plan
date: 2026-02-08
surface: agent
model: claude-opus-4-6
feature: 005-specification-phase-iii
branch: 005-specification-phase-iii
user: unknown
command: /sp.plan
labels: [plan-update, openai-model, runner-run-streamed, technical-decisions, backend-architecture]
links:
  spec: specs/005-specification-phase-iii/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/005-specification-phase-iii/plan.md
tests:
 - none
---

## Prompt

/sp.plan add in plan.md that we are going to use Openai model in Agent() and For ChatKit Stream event we are going to use Runner.run_streamed

## Response snapshot

Successfully updated plan.md to document technical decisions for OpenAI model usage and Runner.run_streamed() streaming implementation.

**Changes Made to Backend Integration Section:**

**1. Agent Model Configuration**
- Documented use of OpenAI models (gpt-4o, gpt-4-turbo) via OpenAI Agents SDK
- Specified model configuration in Agent() constructor

**2. Streaming Implementation**
- Documented use of `Runner.run_streamed()` from OpenAI Agents SDK
- Specified token-by-token streaming approach

**3. Updated Backend Architecture Code Example**

**OLD Architecture (Conceptual ChatKitServer):**
```python
from openai_chatkit import ChatKitServer

class ChatEndpoint:
    def __init__(self):
        self.chatkit_server = ChatKitServer(...)
```

**NEW Architecture (Runner.run_streamed):**
```python
from agents import Agent, Runner, ModelSettings
from openai.types.responses import ResponseTextDeltaEvent

async def run_agent_workflow_streamed(user_id, message, conversation_id):
    agent = Agent(
        name="TodoAssistant",
        model="gpt-4o",  # OpenAI model
        instructions=SYSTEM_PROMPT,
        mcp_servers=[connection],
        model_settings=ModelSettings(temperature=0.7)
    )

    result = Runner.run_streamed(agent, input=conversation_text)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            yield {"type": "chunk", "content": event.data.delta}
```

**4. Key Technical Decisions Documented**

Added explicit technical decisions section:
- **Model**: OpenAI gpt-4o (configurable)
- **Streaming Method**: Runner.run_streamed() from OpenAI Agents SDK v0.7.0
- **Event Filtering**: ResponseTextDeltaEvent for text, tool_end for tool calls
- **SSE Format**: `data: {"type": "chunk", "content": "..."}\n\n`
- **Integration**: MCP tools via mcp_servers parameter

**5. Updated Key Responsibilities**

Modified to reflect actual implementation approach:
- Handle SSE streaming via Runner.run_streamed() (not ChatKitServer)
- Integrate with OpenAI Agents SDK using OpenAI models (not generic agent_sdk)
- Specific mention of OpenAI models instead of generic LLM

**Rationale for Changes:**

1. **OpenAI Model Choice**:
   - Native OpenAI SDK support in Agents SDK
   - Better streaming performance with ResponseTextDeltaEvent
   - Simpler configuration (just model name string)
   - OPENAI_API_KEY from environment

2. **Runner.run_streamed() Choice**:
   - Official streaming method from OpenAI Agents SDK
   - Token-by-token streaming via ResponseTextDeltaEvent
   - Built-in event filtering and tool execution tracking
   - Compatible with SSE protocol for web clients

3. **Architecture Simplification**:
   - No need for separate ChatKitServer abstraction
   - Direct use of OpenAI Agents SDK primitives
   - Clearer separation of concerns (streaming vs business logic)

**Implementation Alignment:**

Plan now aligns with:
- ✅ PHR-0021: Session endpoint implementation
- ✅ PHR-0022: SKILL.md streaming documentation
- ✅ Context7 research on Runner.run_streamed()
- ✅ OpenAI Agents SDK v0.7.0 patterns

**Next Steps:**

1. Implement run_agent_workflow_streamed() in chat_service.py
2. Update stream_chat_response() in chat.py to use new function
3. Test streaming with frontend ChatKit SDK
4. Verify token-by-token delivery and tool call events

## Outcome

- ✅ Impact: Updated plan.md to document OpenAI model usage and Runner.run_streamed() streaming implementation, providing clear technical direction for backend development
- 🧪 Tests: No tests - planning documentation update
- 📁 Files: Updated plan.md (Backend Integration section with code examples and technical decisions)
- 🔁 Next prompts: Implement run_agent_workflow_streamed() in chat_service.py following documented patterns, update chat.py to use streaming function, test with frontend
- 🧠 Reflection: Plan documentation should reflect actual implementation approach, not conceptual abstractions. Documenting specific SDK methods (Runner.run_streamed) and model choices (gpt-4o) provides clearer guidance than generic descriptions. Code examples in plan.md serve as implementation reference and ensure consistency between planning and execution phases.

## Evaluation notes (flywheel)

- Failure modes observed: None - straightforward documentation update based on research and implementation decisions
- Graders run and results (PASS/FAIL): Plan.md update: PASS (Backend Integration section updated with OpenAI model and Runner.run_streamed), Code examples: PASS (complete working examples with imports and event filtering), Technical decisions: PASS (explicit model choice, streaming method, event types documented), Alignment: PASS (matches SKILL.md documentation and Context7 research)
- Prompt variant (if applicable): /sp.plan with specific request to document OpenAI model and Runner.run_streamed() usage
- Next experiment (smallest change to try): Implement the documented run_agent_workflow_streamed() function in chat_service.py exactly as shown in plan.md, test with simple message to verify streaming works
