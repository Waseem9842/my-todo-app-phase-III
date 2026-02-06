from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class ConversationBase(SQLModel):
    user_id: str = Field(description="ID of the user who owns this conversation")


class Conversation(ConversationBase, table=True):
    """
    Represents a user's chat session with metadata like start time, status, and user_id.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    started_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="active", description="Conversation status: active, closed, archived")


class ConversationRead(ConversationBase):
    """Response model for reading conversations"""
    id: int
    started_at: datetime
    updated_at: datetime
    status: str


class ConversationCreate(ConversationBase):
    """Request model for creating conversations"""
    pass  # Inherits all fields from ConversationBase