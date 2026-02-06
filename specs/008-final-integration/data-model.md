# Data Model: Final Integration, Security & Readiness for AI Todo Platform

## Entities

### Authenticated Session
Represents a validated user session with JWT token, user_id, and session metadata for cross-service validation.

**Fields**:
- `user_id`: String (Primary identifier from JWT token, required)
- `jwt_token`: String (Valid JWT token for authentication, required)
- `session_start_time`: DateTime (When the session began)
- `last_activity_time`: DateTime (Most recent activity in the session)
- `expires_at`: DateTime (When the session expires based on JWT expiry)

**Validation Rules**:
- user_id must match the one in the JWT token
- jwt_token must be a valid, non-expired JWT
- expires_at must be in the future

**Relationships**:
- Associated with many operations during the session

### System Health Status
Represents the operational state of the integrated system with individual service statuses and overall readiness.

**Fields**:
- `service_name`: String (Name of the service being monitored)
- `status`: String (Service status: healthy, degraded, unavailable)
- `timestamp`: DateTime (When the status was recorded)
- `dependencies`: Array (Status of dependent services like database, MCP server)
- `response_time_ms`: Integer (Response time in milliseconds)
- `message`: String (Additional status information)

**Validation Rules**:
- status must be one of the allowed values
- response_time_ms must be non-negative
- timestamp must be current

**Relationships**:
- Part of overall system status aggregation

### Operation Log
Represents a record of agent actions and tool calls with timestamps, user context, and operation outcomes for observability.

**Fields**:
- `id`: String or Number (Unique identifier for the log entry)
- `user_id`: String (ID of the user associated with the operation)
- `operation_type`: String (Type of operation: chat_interaction, tool_call, auth_check, etc.)
- `tool_name`: String (Name of the tool called, if applicable)
- `request_payload`: JSON (Original request data)
- `response_payload`: JSON (Response data returned)
- `timestamp`: DateTime (When the operation occurred)
- `duration_ms`: Integer (Time taken to complete the operation)
- `success`: Boolean (Whether the operation succeeded)
- `error_message`: String (Error message if operation failed, optional)

**Validation Rules**:
- user_id must be valid
- operation_type must be one of the allowed values
- timestamp must be current
- duration_ms must be non-negative

**Relationships**:
- Associated with specific user sessions
- Related to specific conversation contexts

## State Transitions

### Session Status
- Initial state: `status = "active"` (when user authenticates)
- Transition trigger: Inactivity or explicit logout
- Final state: `status = "expired"` or `status = "terminated"`

### Health Status
- Healthy state: `status = "healthy"` (all dependencies available)
- Transition trigger: Service or dependency failure
- Degraded state: `status = "degraded"` (some issues but operational)
- Unavailable state: `status = "unavailable"` (critical failure)
- Recovery: Returns to healthy when dependencies are restored

## Access Control Rules

### JWT Token Validation
- Each API request must include a valid JWT token in the Authorization header
- The token must not be expired
- The user_id in the token must match the requested resource ownership
- Invalid tokens result in 401 Unauthorized responses

### Service Communication Validation
- Internal service calls must include proper authentication context
- Cross-service requests must validate the caller's authorization
- Database operations must validate user permissions before execution
- Tool calls must validate user ownership of resources being modified