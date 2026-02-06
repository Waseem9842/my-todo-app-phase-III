from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from src.database.database import get_session
from src.models.task_model import Task, TaskCreate, TaskRead, TaskUpdate
from src.services.task_service import TaskService
from src.auth.auth_dependencies import get_current_user
from src.auth.error_handlers import create_forbidden_exception

# Create the API router
task_router = APIRouter()


@task_router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: int,
    task_create: TaskCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the specified user.
    """
    # Verify that the user_id in the path matches the user_id in the token
    token_user_id = int(current_user["user_id"])
    if token_user_id != user_id:
        raise create_forbidden_exception("You can only create tasks for yourself")

    try:
        # Update task_create to include the user_id from the path
        task_create.user_id = str(user_id)
        task = TaskService.create_task(task_create, session)
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating task: {str(e)}"
        )


@task_router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the specified user.
    """
    # Verify that the user_id in the path matches the user_id in the token
    token_user_id = int(current_user["user_id"])
    if token_user_id != user_id:
        raise create_forbidden_exception("You can only access your own tasks")

    try:
        tasks = TaskService.get_tasks_by_user(str(user_id), session)
        return tasks
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving tasks: {str(e)}"
        )


@task_router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    user_id: int,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the specified user.
    """
    # Verify that the user_id in the path matches the user_id in the token
    token_user_id = int(current_user["user_id"])
    if token_user_id != user_id:
        raise create_forbidden_exception("You can only access your own tasks")

    try:
        task = TaskService.get_task_by_id_and_user(task_id, str(user_id), session)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the specified user"
            )
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving task: {str(e)}"
        )


@task_router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    user_id: int,
    task_id: int,
    task_update: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task by ID for the specified user.
    """
    # Verify that the user_id in the path matches the user_id in the token
    token_user_id = int(current_user["user_id"])
    if token_user_id != user_id:
        raise create_forbidden_exception("You can only update your own tasks")

    try:
        updated_task = TaskService.update_task(task_id, str(user_id), task_update, session)
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the specified user"
            )
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task: {str(e)}"
        )


@task_router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def toggle_task_completion(
    user_id: int,
    task_id: int,
    completed: bool,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the specified user.
    """
    # Verify that the user_id in the path matches the user_id in the token
    token_user_id = int(current_user["user_id"])
    if token_user_id != user_id:
        raise create_forbidden_exception("You can only update your own tasks")

    try:
        updated_task = TaskService.toggle_task_completion(task_id, str(user_id), completed, session)
        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the specified user"
            )
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating task completion: {str(e)}"
        )


@task_router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: int,
    task_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task by ID for the specified user.
    """
    # Verify that the user_id in the path matches the user_id in the token
    token_user_id = int(current_user["user_id"])
    if token_user_id != user_id:
        raise create_forbidden_exception("You can only delete your own tasks")

    try:
        deleted = TaskService.delete_task(task_id, str(user_id), session)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found or does not belong to the specified user"
            )
        return
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting task: {str(e)}"
        )