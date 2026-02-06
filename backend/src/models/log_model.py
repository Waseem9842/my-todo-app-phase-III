from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class LogEntryBase(SQLModel):
    """
    Base model for operation log entries with common fields.
    """
    user_id: str = Field(description="ID of the user associated with the operation")
    operation_type: str = Field(description="Type of operation: chat_interaction, tool_call, auth_check, database_operation")
    success: bool = Field(description="Whether the operation was successful")


class LogEntry(LogEntryBase, table=True):
    """
    Model representing a log entry for operations in the system.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    tool_name: Optional[str] = Field(default=None, description="Name of the tool called (if applicable)")
    request_payload: Optional[Dict[str, Any]] = Field(default=None, description="Original request data (may be omitted for security)")
    response_payload: Optional[Dict[str, Any]] = Field(default=None, description="Response data (may be omitted for security)")
    duration_ms: Optional[int] = Field(default=None, description="Time taken to complete the operation in milliseconds")
    error_message: Optional[str] = Field(default=None, description="Error message if operation failed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class LogEntryRead(LogEntryBase):
    """
    Response model for reading log entries.
    """
    id: int
    tool_name: Optional[str]
    request_payload: Optional[Dict[str, Any]]
    response_payload: Optional[Dict[str, Any]]
    duration_ms: Optional[int]
    error_message: Optional[str]
    timestamp: datetime


class LogEntryCreate(LogEntryBase):
    """
    Request model for creating log entries.
    """
    tool_name: Optional[str] = None
    request_payload: Optional[Dict[str, Any]] = None
    response_payload: Optional[Dict[str, Any]] = None
    duration_ms: Optional[int] = None
    error_message: Optional[str] = None