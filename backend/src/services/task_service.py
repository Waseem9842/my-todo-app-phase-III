from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime, timezone
from ..models.task_model import Task, TaskCreate, TaskUpdate, TaskRead


class TaskService:
    """
    Service class for handling CRUD operations on tasks with user isolation validation.
    Designed for MCP server integration with string user_id validation.
    """

    @staticmethod
    def create_task(task_data: TaskCreate, db_session: Session) -> Task:
        """
        Create a new task with the given data.

        Args:
            task_data: TaskCreate object containing task information
            db_session: Database session

        Returns:
            Created Task object
        """
        task = Task(
            title=task_data.title,
            description=task_data.description,
            user_id=task_data.user_id,
            completed=False
        )
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task

    @staticmethod
    def get_tasks_by_user(user_id: str, db_session: Session) -> List[Task]:
        """
        Get all tasks for a specific user.

        Args:
            user_id: ID of the user whose tasks to retrieve (string format)
            db_session: Database session

        Returns:
            List of Task objects belonging to the user
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = db_session.exec(statement).all()
        return tasks

    @staticmethod
    def get_task_by_id_and_user(task_id: int, user_id: str, db_session: Session) -> Optional[Task]:
        """
        Get a specific task by ID and user ID for validation.

        Args:
            task_id: ID of the task to retrieve
            user_id: ID of the user who should own the task (string format)
            db_session: Database session

        Returns:
            Task object if found and owned by user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = db_session.exec(statement).first()
        return task

    @staticmethod
    def update_task(task_id: int, user_id: str, task_update: TaskUpdate, db_session: Session) -> Optional[Task]:
        """
        Update a task if it belongs to the specified user.

        Args:
            task_id: ID of the task to update
            user_id: ID of the user who owns the task (string format)
            task_update: TaskUpdate object with new values
            db_session: Database session

        Returns:
            Updated Task object if successful, None if not found or not owned by user
        """
        task = TaskService.get_task_by_id_and_user(task_id, user_id, db_session)
        if not task:
            return None

        # Update only the fields that are provided
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description

        task.updated_at = datetime.utcnow()
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task

    @staticmethod
    def toggle_task_completion(task_id: int, user_id: str, completed: bool, db_session: Session) -> Optional[Task]:
        """
        Toggle the completion status of a task for the specified user.

        Args:
            task_id: ID of the task to update
            user_id: ID of the user who owns the task (string format)
            completed: Boolean indicating whether the task should be marked as completed
            db_session: Database session

        Returns:
            Updated Task object if successful, None if not found or not owned by user
        """
        task = TaskService.get_task_by_id_and_user(task_id, user_id, db_session)
        if not task:
            return None

        task.completed = completed
        task.updated_at = datetime.utcnow()
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)
        return task

    @staticmethod
    def delete_task(task_id: int, user_id: str, db_session: Session) -> bool:
        """
        Delete a task if it belongs to the specified user.

        Args:
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task (string format)
            db_session: Database session

        Returns:
            True if deletion was successful, False if task not found or not owned by user
        """
        task = TaskService.get_task_by_id_and_user(task_id, user_id, db_session)
        if not task:
            return False

        db_session.delete(task)
        db_session.commit()
        return True