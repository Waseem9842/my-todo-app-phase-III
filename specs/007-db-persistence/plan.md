# Implementation Plan: Database Models, Migrations & Persistence for AI Todo Chatbot

**Branch**: `007-db-persistence` | **Date**: 2026-01-29 | **Spec**: [specs/007-db-persistence/spec.md](specs/007-db-persistence/spec.md)
**Input**: Feature specification from `/specs/007-db-persistence/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of database persistence layer for the AI Todo Chatbot using SQLModel and Neon PostgreSQL. This includes defining the data models for Task, Conversation, and Message entities, implementing Alembic-based migrations, and ensuring proper user isolation with robust error handling. The implementation will provide the foundation for reliable data persistence across system restarts and concurrent user access.

## Technical Context

**Language/Version**: Python 3.13+ (as per constitution and existing backend)
**Primary Dependencies**: SQLModel, Alembic, Neon PostgreSQL driver, Pydantic, FastAPI
**Storage**: Neon Serverless PostgreSQL (as per constitution)
**Testing**: pytest with SQLModel testing utilities
**Target Platform**: Linux server (backend service)
**Project Type**: Backend service (extension of existing backend)
**Performance Goals**: <2 seconds for conversation history reconstruction (as per spec SC-002)
**Constraints**: Stateless design with no in-memory state between requests (as per constitution and spec)
**Scale/Scope**: Multi-user support with 100% user isolation accuracy (as per spec SC-003)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Stateless Architecture**: Database operations remain stateless with no in-memory storage between requests - CONFIRMED
- **Database as Source of Truth**: All conversation history and task data persisted in Neon PostgreSQL - CONFIRMED
- **Authentication & Authorization**: User isolation enforced via user_id scoping - CONFIRMED
- **Technology Constraints**: Using approved stack (SQLModel, Neon PostgreSQL, FastAPI) - CONFIRMED
- **Clear Separation of Concerns**: Backend handles persistence, no business logic in models - CONFIRMED
- **Post-Design Verification**: All design artifacts comply with constitution - CONFIRMED
- **Post-Design Verification**: All research, data-model, quickstart, and contracts artifacts comply with constitution - CONFIRMED

## Project Structure

### Documentation (this feature)

```text
specs/007-db-persistence/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (extension of existing backend)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task_model.py          # Task entity with user isolation (updated)
│   │   ├── conversation_model.py  # Conversation entity with user_id
│   │   ├── message_model.py       # Message entity with conversation reference
│   │   └── user_model.py          # User entity (existing)
│   ├── services/
│   │   ├── task_service.py        # Task operations with user validation
│   │   ├── conversation_service.py # Conversation operations with user validation
│   │   └── message_service.py     # Message operations with user validation
│   ├── database/
│   │   ├── database.py            # Database connection/config
│   │   └── migrations/            # Alembic migration files
│   └── api/
│       └── mcp_endpoints.py       # MCP tool endpoints (existing)
├── requirements.txt               # Add Alembic for migrations
└── tests/
    ├── unit/
    │   ├── models/
    │   └── services/
    └── integration/
        └── test_db_persistence.py # Database persistence tests
```

**Structure Decision**: Extending existing backend structure following established patterns in the codebase. The database persistence layer will be implemented as enhancements to existing models and services, with new migration scripts as needed. This follows the constitution's principle of clear separation of concerns while leveraging existing backend infrastructure.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [N/A - All constitution gates passed] | [N/A] | [N/A] |