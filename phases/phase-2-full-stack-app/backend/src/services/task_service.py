from sqlmodel import Session, select
from schema.models import Task, TaskCreate, TaskUpdate, TaskRead
from typing import List, Optional
from datetime import datetime

class TaskService:
    @staticmethod
    def create_task(session: Session, task_data: TaskCreate, user_id: str) -> TaskRead:
        """Create a new task for a specific user"""
        # Create a dictionary with all the data
        task_dict = task_data.model_dump()
        task_dict['user_id'] = user_id
        # Create Task object using the dictionary
        task = Task(**task_dict)
        session.add(task)
        session.commit()
        session.refresh(task)
        return TaskRead.model_validate(task)

    @staticmethod
    def get_tasks_by_user_id(session: Session, user_id: str, search: Optional[str] = None, priority: Optional[str] = None, completed: Optional[bool] = None) -> List[TaskRead]:
        """Get all tasks for a specific user with optional search and filter parameters"""
        # Start with the base condition to ensure user data isolation
        statement = select(Task).where(Task.user_id == user_id)

        # Apply search filter if provided
        if search:
            search_lower = search.lower()
            statement = statement.where(
                (Task.title.icontains(search_lower)) |
                (Task.description.icontains(search_lower))
            )

        # Apply priority filter if provided
        if priority:
            statement = statement.where(Task.priority == priority)

        # Apply completed filter if provided
        if completed is not None:
            statement = statement.where(Task.completed == completed)

        tasks = session.exec(statement).all()
        return [TaskRead.model_validate(task) for task in tasks]

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: str) -> Optional[TaskRead]:
        """Get a specific task by ID for a specific user"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if task:
            return TaskRead.model_validate(task)
        return None

    @staticmethod
    def update_task(session: Session, task_id: int, user_id: str, task_data: TaskUpdate) -> Optional[TaskRead]:
        """Update a specific task by ID for a specific user"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            return None

        # Update task with provided data
        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return TaskRead.model_validate(task)

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        """Delete a specific task by ID for a specific user"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Optional[TaskRead]:
        """Toggle the completion status of a specific task for a specific user"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            return None

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return TaskRead.model_validate(task)