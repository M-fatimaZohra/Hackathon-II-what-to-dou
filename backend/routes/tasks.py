from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session
from typing import List
from database.db import get_session
from schema.models import TaskCreate, TaskRead, TaskUpdate
from services.task_service import TaskService

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(request: Request, user_id: str, session: Session = Depends(get_session)):
    """
    List all tasks for the specified user.
    """
    # Extract user_id from JWT which was set by middleware
    jwt_user_id = getattr(request.state, 'user_id', None)
    if not jwt_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Verify that the user_id in the path matches the user from JWT
    if jwt_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    tasks = TaskService.get_tasks_by_user_id(session, user_id)
    return tasks

@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task(request: Request, user_id: str, task_data: TaskCreate, session: Session = Depends(get_session)):
    """
    Create a new task for the specified user.
    """
    # Extract user_id from JWT which was set by middleware
    jwt_user_id = getattr(request.state, 'user_id', None)
    if not jwt_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Verify that the user_id in the path matches the user from JWT
    if jwt_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: User ID mismatch"
        )

    return TaskService.create_task(session, task_data, user_id)

@router.get("/{user_id}/tasks/{id}", response_model=TaskRead)
def get_task_by_id(request: Request, user_id: str, id: int, session: Session = Depends(get_session)):
    """
    Get specific task (must belong to user).
    """
    # Extract user_id from JWT which was set by middleware
    jwt_user_id = getattr(request.state, 'user_id', None)
    if not jwt_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Verify that the user_id in the path matches the user from JWT
    if jwt_user_id != user_id:
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
def update_task_by_id(request: Request, user_id: str, id: int, task_data: TaskUpdate, session: Session = Depends(get_session)):
    """
    Update specific task (must belong to user).
    """
    # Extract user_id from JWT which was set by middleware
    jwt_user_id = getattr(request.state, 'user_id', None)
    if not jwt_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Verify that the user_id in the path matches the user from JWT
    if jwt_user_id != user_id:
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
def delete_task_by_id(request: Request, user_id: str, id: int, session: Session = Depends(get_session)):
    """
    Delete specific task (must belong to user).
    """
    # Extract user_id from JWT which was set by middleware
    jwt_user_id = getattr(request.state, 'user_id', None)
    if not jwt_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Verify that the user_id in the path matches the user from JWT
    if jwt_user_id != user_id:
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
def toggle_task_completion(request: Request, user_id: str, id: int, session: Session = Depends(get_session)):
    """
    Toggle task completion (must belong to user).
    """
    # Extract user_id from JWT which was set by middleware
    jwt_user_id = getattr(request.state, 'user_id', None)
    if not jwt_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    # Verify that the user_id in the path matches the user from JWT
    if jwt_user_id != user_id:
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