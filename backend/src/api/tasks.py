from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from src.database.db import get_session
from src.schema.models import TaskCreate, TaskRead, TaskUpdate
from src.services.task_service import TaskService
from src.middleware.auth_handler import get_current_user

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(user_id: str,
              search: Optional[str] = Query(None, description="Search term for title/description"),
              priority: Optional[str] = Query(None, description="Filter by priority (low, medium, high, urgent)"),
              completed: Optional[bool] = Query(None, description="Filter by completion status (true for completed, false for incomplete)"),
              current_user_id: str = Depends(get_current_user),
              session: Session = Depends(get_session)):
    """
    List all tasks for the specified user with optional search and filter parameters.
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )
    tasks = TaskService.get_tasks_by_user_id(session, user_id, search=search, priority=priority, completed=completed)
    return tasks

@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task(user_id: str, task_data: TaskCreate, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Create a new task for the specified user.
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )
    return TaskService.create_task(session, task_data, user_id)

@router.get("/{user_id}/tasks/{id}", response_model=TaskRead)
def get_task_by_id(user_id: str, id: int, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Get specific task (must belong to user).
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )
    task = TaskService.get_task_by_id(session, id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/{user_id}/tasks/{id}", response_model=TaskRead)
def update_task_by_id(user_id: str, id: int, task_data: TaskUpdate, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Update specific task (must belong to user).
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )
    task = TaskService.update_task(session, id, user_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.delete("/{user_id}/tasks/{id}")
def delete_task_by_id(user_id: str, id: int, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Delete specific task (must belong to user).
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )
    success = TaskService.delete_task(session, id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}

@router.patch("/{user_id}/tasks/{id}/complete", response_model=TaskRead)
def toggle_task_completion(user_id: str, id: int, current_user_id: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """
    Toggle task completion (must belong to user).
    """
    # Verify that the user_id in the path matches the current user from JWT
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )
    task = TaskService.toggle_task_completion(session, id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task