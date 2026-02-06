---
id: 1
title: "update-constitution-agentic-mcp"
stage: "constitution"
date_iso: "2026-01-28"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution"
labels:
  - "constitution"
  - "agentic"
  - "mcp"
  - "todo-app"
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - ".specify/memory/constitution.md"
tests_yaml: []
---

# PHR: Update Constitution to Agentic, MCP-Based Todo Application

## Outcome
Updated the project constitution from version 3.0.0 to 4.0.0 to reflect the shift toward an AI-powered, agentic todo application with Model Context Protocol (MCP) integration.

## Evaluation
The constitution was successfully updated to reflect the new project direction focusing on agentic development, MCP-first tooling, and AI agent discipline. The new constitution establishes 10 core principles compared to the previous 6, with emphasis on stateless architecture, MCP integration, and deterministic behavior.

## Prompt Text
```
/sp.constitution

Project Name:
AI-Powered Todo Application (Agentic, MCP-based)

Project Goal:
Build a production-grade, multi-phase Todo application evolving from a traditional CRUD system into an AI-powered, agent-driven system using MCP (Model Context Protocol), OpenAI Agents SDK, and a stateless backend architecture.

This constitution applies globally to ALL specs (past, current, and future).

────────────────────────────────
CORE PRINCIPLES
────────────────────────────────

1. Agentic Development Workflow
- Follow strict Agentic Dev Stack:
  Write spec → Generate plan → Break into tasks → Implement
- No manual coding or architectural decisions outside specs
- Each spec must have a single, clear responsibility

2. Stateless Architecture
- Backend APIs must remain stateless
- Conversation, auth state, and task state must persist in the database
- No in-memory session storage or global server state

3. MCP-First Tooling
- All task mutations and reads MUST happen through MCP tools
- AI agents are NOT allowed direct database access
- MCP tools must be stateless and deterministic
- Tools may read/write database but must not store memory internally

4. AI Agent Discipline
- AI agents must:
  - Use MCP tools for all task operations
  - Follow behavior rules defined in agent specs
  - Confirm user actions clearly and politely
  - Handle errors gracefully and transparently
- Agents must never hallucinate task state

5. Clear Separation of Concerns
- Frontend: UI only (no business logic)
- Backend API: Routing, orchestration, persistence
- Agent: Reasoning and tool selection
- MCP Server: Tool execution only
- Database: Source of truth

6. Authentication & Authorization
- Authentication must be enforced using Better Auth
- All APIs, MCP tools, and agent actions must be scoped by `user_id`
- No anonymous task access
- Auth tokens must be validated server-side

7. Database as Source of Truth
- Neon PostgreSQL is the single source of truth
- All conversation history, messages, and tasks must be persisted
- Server restarts must not affect conversation continuity

8. Deterministic & Inspectable Behavior
- Every agent action must be traceable:
  - User message
  - Tool calls
  - Tool results
  - Final response
- Tool calls must be included in API responses for observability

9. Technology Constraints (Hard Rules)
- Frontend: OpenAI ChatKit
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- Authentication: Better Auth
- No additional frameworks unless explicitly approved in a spec

10. Spec Quality Rules
- Every spec must define:
  - Objective
  - Scope (In / Out)
  - Success criteria
  - Constraints
  - Non-goals
- Specs must be implementation-ready
- Specs must not overlap responsibilities

────────────────────────────────
NON-GOALS (GLOBAL)
────────────────────────────────

- No vendor comparisons
- No ethical or philosophical AI discussions
- No UI polish beyond functional UX
- No manual state management
- No hidden logic outside specs

────────────────────────────────
SUCCESS DEFINITION
────────────────────────────────

The project is successful when:
- Users can manage todos via UI and natural language
- AI agents reliably use MCP tools
- Conversations resume correctly after restarts
- System is modular, inspectable, and production-ready
- All behavior is spec-driven and reproducible

This constitution is binding for all current and future specs.
```

## Response Text
Updated the constitution file to version 4.0.0, implementing all 10 core principles from the user input. The new constitution emphasizes agentic development, MCP-first tooling, AI agent discipline, and stateless architecture. The file includes an update impact report showing the version change from 3.0.0 to 4.0.0, and all principles were converted to the proper format with Roman numerals.