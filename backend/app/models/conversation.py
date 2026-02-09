# Task: T-301 - Create Conversation Model
# Spec: specs/ai-chatbot/spec.md §4
# Plan: specs/ai-chatbot/plan.md
"""
Conversation model for chat history persistence.

Stores conversation sessions for each user, enabling
stateless server architecture with persistent chat history.
"""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.message import Message


class ConversationBase(SQLModel):
    """Base conversation fields."""

    user_id: str = Field(index=True, description="Owner of the conversation")


class Conversation(ConversationBase, table=True):
    """
    Conversation model for storing chat sessions.

    Attributes:
        id: Unique conversation identifier
        user_id: User who owns this conversation
        created_at: When the conversation was started
        updated_at: When the conversation was last updated
        messages: List of messages in this conversation
    """

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation")


class ConversationCreate(SQLModel):
    """Schema for creating a new conversation."""

    user_id: str


class ConversationResponse(ConversationBase):
    """Schema for conversation API responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
