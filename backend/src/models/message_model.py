from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from sqlalchemy import JSON


class MessageBase(SQLModel):
    conversation_id: int = Field(description="ID of the conversation this message belongs to")
    role: str = Field(description="Role of the message sender: user, assistant, or system")
    content: str = Field(max_length=10000, description="Content of the message")


class Message(MessageBase, table=True):
    """
    Represents an individual message in a conversation with content, sender, timestamp, and role (user/assistant).
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    tool_calls: Optional[dict] = Field(default=None, sa_type=JSON, description="Stores MCP tool calls made during this interaction")
    tool_results: Optional[dict] = Field(default=None, sa_type=JSON, description="Stores results from MCP tool calls")


class MessageRead(MessageBase):
    """Response model for reading messages"""
    id: int
    timestamp: datetime
    tool_calls: Optional[dict]
    tool_results: Optional[dict]


class MessageCreate(MessageBase):
    """Request model for creating messages"""
    pass  # Inherits all fields from MessageBase