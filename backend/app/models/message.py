# Task: T-301 - Create Message Model
# Spec: specs/ai-chatbot/spec.md §4
# Plan: specs/ai-chatbot/plan.md
"""
Message model for chat message persistence.

Stores individual messages within conversations, supporting
both user and assistant roles for conversation history.
"""

from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class MessageRole(str, Enum):
    """Message sender role."""

    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageBase(SQLModel):
    """Base message fields."""

    user_id: str = Field(index=True, description="User who owns this message")
    conversation_id: int = Field(
        foreign_key="conversations.id",
        index=True,
        description="Conversation this message belongs to",
    )
    role: str = Field(description="Message role: user, assistant, or system")
    content: str = Field(description="Message content")


class Message(MessageBase, table=True):
    """
    Message model for storing chat messages.

    Attributes:
        id: Unique message identifier
        user_id: User who owns this message
        conversation_id: Foreign key to conversation
        role: Message sender role (user/assistant/system)
        content: The message text content
        created_at: When the message was created
        conversation: Parent conversation relationship
    """

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Optional["Conversation"] = Relationship(back_populates="messages")


class MessageCreate(SQLModel):
    """Schema for creating a new message."""

    conversation_id: int
    role: str
    content: str


class MessageResponse(MessageBase):
    """Schema for message API responses."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
