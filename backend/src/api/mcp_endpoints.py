"""
MCP (Model Context Protocol) Endpoints for Todo Task Operations
Implements the stateless tools for AI agents to interact with todo tasks.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from fastapi import Depends, HTTPException
from sqlmodel import Session

from backend.src.models.task_model import TaskCreate, TaskUpdate, TaskRead
from backend.src.services.task_service import TaskService
from backend.src.database.database import get_session


# Set up logging
logger = logging.getLogger(__name__)

# This is a placeholder implementation that demonstrates the structure
# Actual MCP tools would be implemented using the python-mcp-sdk

class MCPTaskEndpoints:
    """
    Container class for MCP task endpoints that will be registered with the MCP server.
    """

    def __init__(self):
        # Initialize any required components
        self.validation_errors = []
        self.logger = logging.getLogger(__name__)

    def add_task(self, title: str, description: Optional[str], user_id: str) -> Dict[str, Any]:
        """
        Create a new task for a user.

        Args:
            title: Title of the task (1-255 characters)
            description: Optional description of the task (max 1000 characters)
            user_id: ID of the user creating the task

        Returns:
            Dictionary with success status, task ID, and message
        """
        try:
            # Validate input
            if not title or len(title) < 1 or len(title) > 255:
                return {
                    "success": False,
                    "error": "validation_error",
                    "message": "Title must be between 1 and 255 characters"
                }

            if user_id is None or user_id.strip() == "":
                return {
                    "success": False,
                    "error": "validation_error",
                    "message": "user_id is required"
                }

            # Create task data object
            task_create = TaskCreate(
                title=title,
                description=description,
                user_id=user_id
            )

            # Get database session
            # In a real MCP implementation, this would be handled differently
            # This is a simplified version for demonstration
            from backend.src.database.database import engine
            from sqlmodel import Session

            with Session(engine) as session:
                task = TaskService.create_task(task_data=task_create, db_session=session)

                return {
                    "success": True,
                    "task_id": task.id,
                    "message": f"Task '{task.title}' created successfully"
                }

        except Exception as e:
            return {
                "success": False,
                "error": "database_error",
                "message": f"Failed to create task: {str(e)}"
            }

    def list_tasks(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve all tasks for a specific user.

        Args:
            user_id: ID of the user whose tasks to retrieve

        Returns:
            Dictionary with success status, tasks array, and message
        """
        try:
            if user_id is None or user_id.strip() == "":
                return {
                    "success": False,
                    "error": "validation_error",
                    "message": "user_id is required"
                }

            # Get database session
            from backend.src.database.database import engine
            from sqlmodel import Session

            with Session(engine) as session:
                tasks = TaskService.get_tasks_by_user(user_id, session)

                # Convert tasks to dictionary format
                tasks_data = []
                for task in tasks:
                    tasks_data.append({
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    })

                return {
                    "success": True,
                    "tasks": tasks_data,
                    "message": f"Retrieved {len(tasks)} tasks for user"
                }

        except Exception as e:
            return {
                "success": False,
                "error": "database_error",
                "message": f"Failed to retrieve tasks: {str(e)}"
            }

    def update_task(self, task_id: int, user_id: str, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Update an existing task for a specific user.

        Args:
            task_id: ID of the task to update
            user_id: ID of the user who owns the task
            title: New title for the task (optional)
            description: New description for the task (optional)

        Returns:
            Dictionary with success status, updated task data, and message
        """
        try:
            if user_id is None or user_id.strip() == "":
                return {
                    "success": False,
                    "error": "validation_error",
                    "message": "user_id is required"
                }

            if task_id is None or task_id <= 0:
                return {
                    "success": False,
                    "error": "validation_error",
                    "message": "task_id must be a positive integer"
                }

            # Validate title if provided
            if title is not None and (len(title) < 1 or len(title) > 255):
                return {
                    "success": False,
                    "error": "validation_error",
                    "message": "Title must be between 1 and 255 characters if provided"
                }

            # Prepare update data
            task_update = TaskUpdate(
                title=title,
                description=description
            )

            # Get database session
            from backend.src.database.database import engine
            from sqlmodel import Session

            with Session(engine) as session:
                updated_task = TaskService.update_task(task_id, user_id, task_update, session)

                if updated_task is None:
                    return {
                        "success": False,
                        "error": "authorization_error",
                        "message": "Task not found or user not authorized to modify this task"
                    }

                # Convert task to dictionary format
                task_data = {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "completed": updated_task.completed,
                    "created_at": updated_task.created_at.isoformat(),
                    "updated_at": updated_task.updated_at.isoformat()
                }

                return {
                    "success": True,
                    "task": task_data,
                    "message": f"Task {task_id} updated successfully"
                }

        except Exception as e:
            return {
                "success": False,
                "error": "database_error",
                "message": f"Failed to update task: {str(e)}"
            }

    def complete_task(self, task_id: int, user_id: str) -> Dict[str, Any]:
        """
        Mark a task as completed for a specific user.

        Args:
            task_id: ID of the task to mark as completed
            user_id: ID of the user who owns the task

        Returns:
            Dictionary with success status, updated task data, and message
        """
        try:
            if user_id is None or user_id.strip() == "":
                return {
                    "success": False,
                    "error": "validation_error",
                    "message": "user_id is required"
                }

            if task_id is None or task_id <= 0:
                return {
                    "success": False,
                    "error": "validation_error",
                    "message": "task_id must be a positive integer"
                }

            # Get database session
            from backend.src.database.database import engine
            from sqlmodel import Session

            with Session(engine) as session:
                completed_task = TaskService.complete_task(task_id, user_id, session)

                if completed_task is None:
                    return {
                        "success": False,
                        "error": "authorization_error",
                        "message": "Task not found or user not authorized to modify this task"
                    }

                # Convert task to dictionary format
                task_data = {
                    "id": completed_task.id,
                    "title": completed_task.title,
                    "description": completed_task.description,
                    "completed": completed_task.completed,
                    "created_at": completed_task.created_at.isoformat(),
                    "updated_at": completed_task.updated_at.isoformat()
                }

                return {
                    "success": True,
                    "task": task_data,
                    "message": f"Task {task_id} marked as completed"
                }

        except Exception as e:
            return {
                "success": False,
                "error": "database_error",
                "message": f"Failed to complete task: {str(e)}"
            }

    def delete_task(self, task_id: int, user_id: str) -> Dict[str, Any]:
        """
        Delete a task for a specific user.

        Args:
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            Dictionary with success status and message
        """
        try:
            if user_id is None or user_id.strip() == "":
                return {
                    "success": False,
                    "error": "validation_error",
                    "message": "user_id is required"
                }

            if task_id is None or task_id <= 0:
                return {
                    "success": False,
                    "error": "validation_error",
                    "message": "task_id must be a positive integer"
                }

            # Get database session
            from backend.src.database.database import engine
            from sqlmodel import Session

            with Session(engine) as session:
                success = TaskService.delete_task(task_id, user_id, session)

                if not success:
                    return {
                        "success": False,
                        "error": "authorization_error",
                        "message": "Task not found or user not authorized to delete this task"
                    }

                return {
                    "success": True,
                    "message": f"Task {task_id} deleted successfully"
                }

        except Exception as e:
            return {
                "success": False,
                "error": "database_error",
                "message": f"Failed to delete task: {str(e)}"
            }


# Create an instance of the endpoints to be used by the MCP server
mcp_task_endpoints = MCPTaskEndpoints()