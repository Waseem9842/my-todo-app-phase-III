from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskCreate(TaskBase):
    """Request model for creating tasks"""
    user_id: Optional[str] = Field(default=None, description="ID of the user who owns this task")


class Task(TaskBase, table=True):
    """
    Todo Task model representing a user's task with properties like title,
    description, completion status, and timestamps.
    """
    user_id: str = Field(default=None, description="ID of the user who owns this task")
    id: Optional[int] = Field(default=None, primary_key=True)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskRead(TaskBase):
    """Response model for reading tasks"""
    id: int
    user_id: str  # Include user_id in responses
    completed: bool
    created_at: datetime
    updated_at: datetime


class TaskUpdate(SQLModel):
    """Request model for updating tasks"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)