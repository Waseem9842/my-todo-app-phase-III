# API Contracts: Final Integration, Security & Readiness for AI Todo Platform

## Overview
This document defines the contracts for the integrated system including health checks, authentication validation, and cross-service communication patterns.

## Health and Readiness Endpoints

### GET /health
Return the overall health status of the system.

**Query Parameters**: None

**Success Response** (200 OK):
```json
{
  "status": {
    "type": "string",
    "values": ["healthy", "degraded", "unavailable"],
    "description": "Overall system health status"
  },
  "timestamp": {
    "type": "string",
    "format": "ISO 8601 datetime",
    "description": "Time when the health check was performed"
  },
  "services": {
    "type": "object",
    "properties": {
      "database": {
        "type": "object",
        "properties": {
          "status": {"type": "string", "values": ["connected", "disconnected", "error"]},
          "response_time_ms": {"type": "number"},
          "message": {"type": "string"}
        }
      },
      "mcp_server": {
        "type": "object",
        "properties": {
          "status": {"type": "string", "values": ["available", "unavailable", "error"]},
          "response_time_ms": {"type": "number"},
          "message": {"type": "string"}
        }
      },
      "auth_service": {
        "type": "object",
        "properties": {
          "status": {"type": "string", "values": ["available", "unavailable", "error"]},
          "response_time_ms": {"type": "number"},
          "message": {"type": "string"}
        }
      }
    },
    "description": "Status of individual system services"
  },
  "overall_response_time_ms": {
    "type": "number",
    "description": "Total time to perform health check"
  }
}
```

**Error Response** (503 Service Unavailable):
```json
{
  "status": "unavailable",
  "error": {
    "type": "string",
    "description": "Reason for unavailability"
  },
  "timestamp": {
    "type": "string",
    "format": "ISO 8601 datetime"
  }
}
```

### GET /ready
Return the readiness status of the system for accepting requests.

**Query Parameters**: None

**Success Response** (200 OK):
```json
{
  "ready": {
    "type": "boolean",
    "description": "True if system is ready to accept requests"
  },
  "reason": {
    "type": "string",
    "description": "Explanation of readiness status if not ready"
  },
  "checks": {
    "type": "object",
    "properties": {
      "database_connected": {"type": "boolean"},
      "mcp_tools_available": {"type": "boolean"},
      "auth_service_healthy": {"type": "boolean"},
      "environment_validated": {"type": "boolean"}
    },
    "description": "Individual readiness checks"
  },
  "timestamp": {
    "type": "string",
    "format": "ISO 8601 datetime"
  }
}
```

## Authentication Validation Endpoints

### POST /auth/validate-jwt
Validate a JWT token and return user information.

**Request Body**:
```json
{
  "token": {
    "type": "string",
    "required": true,
    "description": "JWT token to validate"
  }
}
```

**Success Response** (200 OK):
```json
{
  "valid": {
    "type": "boolean",
    "description": "True if token is valid"
  },
  "user_id": {
    "type": "string",
    "description": "User ID from the token"
  },
  "expires_at": {
    "type": "string",
    "format": "ISO 8601 datetime",
    "description": "Token expiration time"
  },
  "message": {
    "type": "string",
    "description": "Success message"
  }
}
```

**Error Response** (401 Unauthorized):
```json
{
  "valid": false,
  "error": {
    "type": "string",
    "values": ["invalid_token", "expired_token", "malformed_token"],
    "description": "Reason for validation failure"
  },
  "message": {
    "type": "string",
    "description": "Error description"
  }
}
```

## Logging Endpoints

### POST /logs/operation
Log an operation for observability and monitoring.

**Request Body**:
```json
{
  "user_id": {
    "type": "string",
    "required": true,
    "description": "ID of the user associated with the operation"
  },
  "operation_type": {
    "type": "string",
    "required": true,
    "values": ["chat_interaction", "tool_call", "auth_check", "database_operation"],
    "description": "Type of operation being logged"
  },
  "tool_name": {
    "type": "string",
    "required": false,
    "description": "Name of the tool called (if applicable)"
  },
  "request_payload": {
    "type": "object",
    "required": false,
    "description": "Original request data (may be omitted for security)"
  },
  "response_payload": {
    "type": "object",
    "required": false,
    "description": "Response data (may be omitted for security)"
  },
  "success": {
    "type": "boolean",
    "required": true,
    "description": "Whether the operation was successful"
  },
  "duration_ms": {
    "type": "number",
    "required": true,
    "description": "Time taken to complete the operation in milliseconds"
  },
  "error_message": {
    "type": "string",
    "required": false,
    "description": "Error message if operation failed"
  }
}
```

**Success Response** (200 OK):
```json
{
  "logged": {
    "type": "boolean",
    "description": "True if log entry was successfully recorded"
  },
  "entry_id": {
    "type": "string",
    "description": "ID of the log entry"
  },
  "message": {
    "type": "string",
    "description": "Success message"
  }
}
```

## Error Handling Contract

### Standard Error Response Format
All error responses across the system must follow this format:

```json
{
  "success": {
    "type": "boolean",
    "description": "Always false for error responses"
  },
  "error": {
    "type": "string",
    "description": "Error type identifier"
  },
  "message": {
    "type": "string",
    "description": "Human-readable error message"
  },
  "details": {
    "type": "object",
    "required": false,
    "description": "Additional error details (for debugging)"
  },
  "timestamp": {
    "type": "string",
    "format": "ISO 8601 datetime",
    "description": "Time when error occurred"
  }
}
```

### Common Error Types
- `validation_error`: Input validation failed
- `auth_error`: Authentication or authorization failed
- `database_error`: Database operation failed
- `tool_error`: MCP tool call failed
- `service_unavailable`: Dependent service unavailable
- `internal_error`: Unexpected internal error

## Integration Requirements

### Cross-Service Communication
- All service-to-service calls must include appropriate authentication context
- Requests between services must follow the same authentication validation rules
- Error propagation should maintain consistent error formats across services
- Response times between services should be monitored and logged

### JWT Consistency Requirements
- JWT secret must be identical between frontend and backend configurations
- Token validation algorithms must match between services
- User ID extraction from JWT must be consistent
- Token expiration handling must be synchronized

### Data Flow Validation
- All user data must flow through proper validation channels
- User isolation must be maintained at every service boundary
- Conversation continuity must be preserved across service restarts
- Tool call results must be properly propagated to the user interface