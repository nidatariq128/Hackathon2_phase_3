# Task: T-001, T-301 - Database Models
# Spec: specs/task-crud/spec.md, specs/ai-chatbot/spec.md
"""
Database models package.

Contains SQLModel models for database tables.
"""

from app.models.task import (
    Task,
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
)
from app.models.conversation import (
    Conversation,
    ConversationCreate,
    ConversationResponse,
)
from app.models.message import (
    Message,
    MessageCreate,
    MessageResponse,
    MessageRole,
)

__all__ = [
    # Task models
    "Task",
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskListResponse",
    # Conversation models
    "Conversation",
    "ConversationCreate",
    "ConversationResponse",
    # Message models
    "Message",
    "MessageCreate",
    "MessageResponse",
    "MessageRole",
]
