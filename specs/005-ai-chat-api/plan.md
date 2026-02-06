# Implementation Plan: AI Agent & Stateless Chat API for Todo Management

**Branch**: `005-ai-chat-api` | **Date**: 2026-01-29 | **Spec**: [specs/005-ai-chat-api/spec.md](specs/005-ai-chat-api/spec.md)
**Input**: Feature specification from `/specs/005-ai-chat-api/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a stateless chat API powered by OpenAI Agents SDK that uses MCP tools to manage todo tasks via natural language. The system will provide a POST /api/{user_id}/chat endpoint that accepts natural language input, processes it through an AI agent, and invokes appropriate MCP tools for todo management operations. Conversation state will be persisted in the database to maintain context across requests while keeping each individual request stateless.

## Technical Context

**Language/Version**: Python 3.13+ (as per constitution and existing backend)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK, Official MCP SDK, SQLModel, Neon PostgreSQL driver, Better Auth
**Storage**: Neon Serverless PostgreSQL (as per constitution)
**Testing**: pytest (consistent with existing backend structure)
**Target Platform**: Linux server (backend service)
**Project Type**: Backend service (integrated with existing backend)
**Performance Goals**: <10 seconds response time for typical natural language requests (as per spec SC-006)
**Constraints**: Stateless design with no in-memory storage between requests (as per constitution and spec)
**Scale/Scope**: Multi-user support with 100% user isolation accuracy (as per spec SC-005)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Stateless Architecture**: API must remain stateless with conversation state persisted in database - CONFIRMED
- **MCP-First Tooling**: All task operations through MCP tools only - CONFIRMED
- **Database as Source of Truth**: All conversation history persisted in Neon PostgreSQL - CONFIRMED
- **Authentication & Authorization**: User isolation enforced via user_id through JWT - CONFIRMED
- **Technology Constraints**: Using approved stack (Python FastAPI, SQLModel, Neon PostgreSQL, OpenAI Agents SDK) - CONFIRMED
- **Post-Design Verification**: All design artifacts comply with constitution - CONFIRMED

## Project Structure

### Documentation (this feature)

```text
specs/005-ai-chat-api/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (integrated with existing backend)

```text
backend/
├── src/
│   ├── models/
│   │   ├── conversation_model.py    # Conversation entity
│   │   ├── message_model.py         # Message entity
│   │   └── task_model.py            # Task entity (reused from existing)
│   ├── services/
│   │   ├── conversation_service.py  # Conversation management
│   │   ├── message_service.py       # Message handling
│   │   ├── task_service.py          # Task operations (enhanced)
│   │   └── ai_agent_service.py      # AI agent integration
│   ├── api/
│   │   ├── chat_endpoints.py        # Main chat API endpoint
│   │   └── mcp_endpoints.py         # MCP tool endpoints (existing)
│   ├── auth/
│   │   └── jwt_auth.py              # JWT validation middleware
│   └── database/
│       └── database.py              # Database connection/config
├── requirements.txt                 # Add OpenAI Agents SDK
└── tests/
    ├── unit/
    │   ├── test_conversation_service.py
    │   └── test_ai_agent_service.py
    ├── integration/
    │   ├── test_chat_endpoint.py
    │   └── test_mcp_tools.py        # Existing MCP tests
    └── contract/
        └── test_agent_responses.py
```

**Structure Decision**: Integrating with existing backend structure following the established patterns in the codebase. The chat API will be implemented as new endpoints and services within the existing backend application, reusing existing task models and MCP endpoints. This follows the constitution's principle of clear separation of concerns while leveraging the existing backend infrastructure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A - All constitution gates passed] | [N/A] | [N/A] |
