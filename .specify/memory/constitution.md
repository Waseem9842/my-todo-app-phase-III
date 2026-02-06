<!-- SYNC IMPACT REPORT -->
<!-- Version change: 3.0.0 → 4.0.0 -->
<!-- Modified principles: Completely replaced old principles with new agentic/MCP-focused ones -->
<!-- Added sections: MCP-First Tooling, AI Agent Discipline, Deterministic & Inspectable Behavior -->
<!-- Removed sections: Old Phase II principles -->
<!-- Templates requiring updates: ✅ Updated plan-template.md, spec-template.md, tasks-template.md -->
<!-- Follow-up TODOs: None -->

# AI-Powered Todo Application (Agentic, MCP-based) Constitution

## Core Principles

### I. Agentic Development Workflow
Follow strict Agentic Dev Stack: Write spec → Generate plan → Break into tasks → Implement. No manual coding or architectural decisions outside specs. Each spec must have a single, clear responsibility.

### II. Stateless Architecture
Backend APIs must remain stateless. Conversation, auth state, and task state must persist in the database. No in-memory session storage or global server state.

### III. MCP-First Tooling
All task mutations and reads MUST happen through MCP tools. AI agents are NOT allowed direct database access. MCP tools must be stateless and deterministic. Tools may read/write database but must not store memory internally.

### IV. AI Agent Discipline
AI agents must:
- Use MCP tools for all task operations
- Follow behavior rules defined in agent specs
- Confirm user actions clearly and politely
- Handle errors gracefully and transparently
Agents must never hallucinate task state.

### V. Clear Separation of Concerns
- Frontend: UI only (no business logic)
- Backend API: Routing, orchestration, persistence
- Agent: Reasoning and tool selection
- MCP Server: Tool execution only
- Database: Source of truth

### VI. Authentication & Authorization
Authentication must be enforced using Better Auth. All APIs, MCP tools, and agent actions must be scoped by `user_id`. No anonymous task access. Auth tokens must be validated server-side.

### VII. Database as Source of Truth
Neon PostgreSQL is the single source of truth. All conversation history, messages, and tasks must be persisted. Server restarts must not affect conversation continuity.

### VIII. Deterministic & Inspectable Behavior
Every agent action must be traceable:
- User message
- Tool calls
- Tool results
- Final response
Tool calls must be included in API responses for observability.

### IX. Technology Constraints (Hard Rules)
- Frontend: OpenAI ChatKit
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK
- Authentication: Better Auth
- No additional frameworks unless explicitly approved in a spec

### X. Spec Quality Rules
Every spec must define:
- Objective
- Scope (In / Out)
- Success criteria
- Constraints
- Non-goals
Specs must be implementation-ready and must not overlap responsibilities.

## Non-Goals (Global)

- No vendor comparisons
- No ethical or philosophical AI discussions
- No UI polish beyond functional UX
- No manual state management
- No hidden logic outside specs

## Success Definition

The project is successful when:
- Users can manage todos via UI and natural language
- AI agents reliably use MCP tools
- Conversations resume correctly after restarts
- System is modular, inspectable, and production-ready
- All behavior is spec-driven and reproducible

## Governance

This constitution is binding for all current and future specs. The project goal is to build a production-grade, multi-phase Todo application evolving from a traditional CRUD system into an AI-powered, agent-driven system using MCP (Model Context Protocol), OpenAI Agents SDK, and a stateless backend architecture. Amendments require explicit specification updates and must maintain the agentic development workflow.

**Version**: 4.0.0 | **Ratified**: 2026-01-22 | **Last Amended**: 2026-01-28