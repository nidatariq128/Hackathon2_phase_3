# Task: T-309 - Implement Conversation Service
# Spec: specs/ai-chatbot/spec.md §8
# Plan: specs/ai-chatbot/plan.md
"""
Conversation Service for managing chat state.

Handles creation, loading, and message persistence for
conversations in the stateless server architecture.
"""

from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models import Conversation, Message


class ConversationService:
    """
    Service for managing conversations and messages.

    Provides methods for creating conversations, loading history,
    and persisting messages to enable stateless server operation.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the conversation service.

        Args:
            session: Database session for operations
        """
        self.session = session

    async def create_conversation(self, user_id: str) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: User who owns the conversation

        Returns:
            The newly created conversation
        """
        conversation = Conversation(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def get_conversation(
        self, conversation_id: int, user_id: str
    ) -> Optional[Conversation]:
        """
        Get a conversation by ID, verifying ownership.

        Args:
            conversation_id: ID of the conversation
            user_id: User who should own the conversation

        Returns:
            The conversation if found and owned by user, None otherwise
        """
        query = select(Conversation).where(
            Conversation.id == conversation_id, Conversation.user_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_or_create_conversation(
        self, conversation_id: Optional[int], user_id: str
    ) -> Conversation:
        """
        Get an existing conversation or create a new one.

        Args:
            conversation_id: Optional ID of existing conversation
            user_id: User who owns the conversation

        Returns:
            The existing or newly created conversation
        """
        if conversation_id:
            conversation = await self.get_conversation(conversation_id, user_id)
            if conversation:
                return conversation

        # Create new conversation if not found or not provided
        return await self.create_conversation(user_id)

    async def get_messages(
        self, conversation_id: int, limit: int = 50
    ) -> List[Message]:
        """
        Get messages for a conversation.

        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages to return

        Returns:
            List of messages ordered by creation time
        """
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_message_history(
        self, conversation_id: int, limit: int = 20
    ) -> List[Dict[str, str]]:
        """
        Get message history formatted for OpenAI API.

        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages to return

        Returns:
            List of message dicts with role and content
        """
        messages = await self.get_messages(conversation_id, limit)
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
            if msg.role in ("user", "assistant")
        ]

    async def add_message(
        self,
        conversation_id: int,
        user_id: str,
        role: str,
        content: str,
    ) -> Message:
        """
        Add a message to a conversation.

        Args:
            conversation_id: ID of the conversation
            user_id: User who owns the message
            role: Message role (user/assistant/system)
            content: Message content

        Returns:
            The created message
        """
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            created_at=datetime.utcnow(),
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def add_user_message(
        self, conversation_id: int, user_id: str, content: str
    ) -> Message:
        """
        Add a user message to a conversation.

        Args:
            conversation_id: ID of the conversation
            user_id: User who sent the message
            content: Message content

        Returns:
            The created message
        """
        return await self.add_message(conversation_id, user_id, "user", content)

    async def add_assistant_message(
        self, conversation_id: int, user_id: str, content: str
    ) -> Message:
        """
        Add an assistant message to a conversation.

        Args:
            conversation_id: ID of the conversation
            user_id: User who owns the conversation
            content: Assistant's response

        Returns:
            The created message
        """
        return await self.add_message(conversation_id, user_id, "assistant", content)

    async def update_conversation_timestamp(self, conversation: Conversation) -> None:
        """
        Update the conversation's updated_at timestamp.

        Args:
            conversation: The conversation to update
        """
        conversation.updated_at = datetime.utcnow()
        await self.session.commit()
