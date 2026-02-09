# Task: T-303 to T-307 - MCP Tools Implementation
# Spec: specs/ai-chatbot/spec.md §6
# Plan: specs/ai-chatbot/plan.md
"""
MCP Tools for Todo AI Agent.

These tools allow the AI agent to perform CRUD operations
on tasks through natural language conversation.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Task


async def add_task(
    session: AsyncSession,
    user_id: str,
    title: str,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a new task for the user.

    Args:
        session: Database session
        user_id: User who owns the task
        title: Task title (required)
        description: Task description (optional)

    Returns:
        Dict with task_id, status, and title
    """
    try:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
        }
    except Exception as e:
        return {"error": str(e)}


async def list_tasks(
    session: AsyncSession,
    user_id: str,
    status: Optional[str] = "all",
) -> Dict[str, Any]:
    """
    Get tasks for the user with optional status filter.

    Args:
        session: Database session
        user_id: User who owns the tasks
        status: Filter by status - "all", "pending", or "completed"

    Returns:
        Dict with tasks list
    """
    try:
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)  # noqa: E712
        elif status == "completed":
            query = query.where(Task.completed == True)  # noqa: E712
        # "all" or None means no filter

        query = query.order_by(Task.created_at.desc())

        result = await session.execute(query)
        tasks = result.scalars().all()

        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat() if task.created_at else None,
            }
            for task in tasks
        ]

        return {
            "tasks": task_list,
            "count": len(task_list),
            "status_filter": status or "all",
        }
    except Exception as e:
        return {"error": str(e), "tasks": []}


async def complete_task(
    session: AsyncSession,
    user_id: str,
    task_id: int,
) -> Dict[str, Any]:
    """
    Mark a task as complete.

    Args:
        session: Database session
        user_id: User who owns the task
        task_id: ID of the task to complete

    Returns:
        Dict with task_id, status, and title
    """
    try:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return {"error": "Task not found", "task_id": task_id}

        task.completed = True
        task.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(task)

        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title,
        }
    except Exception as e:
        return {"error": str(e)}


async def delete_task(
    session: AsyncSession,
    user_id: str,
    task_id: int,
) -> Dict[str, Any]:
    """
    Delete a task.

    Args:
        session: Database session
        user_id: User who owns the task
        task_id: ID of the task to delete

    Returns:
        Dict with task_id, status, and title
    """
    try:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return {"error": "Task not found", "task_id": task_id}

        title = task.title
        await session.delete(task)
        await session.commit()

        return {
            "task_id": task_id,
            "status": "deleted",
            "title": title,
        }
    except Exception as e:
        return {"error": str(e)}


async def update_task(
    session: AsyncSession,
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Update a task's title or description.

    Args:
        session: Database session
        user_id: User who owns the task
        task_id: ID of the task to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        Dict with task_id, status, and title
    """
    try:
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return {"error": "Task not found", "task_id": task_id}

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        task.updated_at = datetime.utcnow()
        await session.commit()
        await session.refresh(task)

        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title,
        }
    except Exception as e:
        return {"error": str(e)}


def get_all_tools() -> List[Dict[str, Any]]:
    """
    Get OpenAI function definitions for all MCP tools.

    Returns:
        List of tool definitions for OpenAI function calling
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Create a new task for the user. Use this when the user wants to add, create, or remember something.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The title of the task to create",
                        },
                        "description": {
                            "type": "string",
                            "description": "Optional description or details for the task",
                        },
                    },
                    "required": ["title"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "Get the user's tasks. Use this when the user wants to see, show, or list their tasks.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter tasks by status. Use 'pending' for incomplete tasks, 'completed' for done tasks, 'all' for everything.",
                        },
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as complete. Use this when the user says they finished, completed, or done with a task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to mark as complete",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task from the list. Use this when the user wants to remove, delete, or cancel a task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to delete",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update a task's title or description. Use this when the user wants to change, rename, or modify a task.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to update",
                        },
                        "title": {
                            "type": "string",
                            "description": "New title for the task",
                        },
                        "description": {
                            "type": "string",
                            "description": "New description for the task",
                        },
                    },
                    "required": ["task_id"],
                },
            },
        },
    ]
