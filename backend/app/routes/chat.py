# Task: T-310 - Create POST /api/{user_id}/chat Endpoint
# Spec: specs/ai-chatbot/spec.md §5
# Plan: specs/ai-chatbot/plan.md
"""
Chat API endpoint for AI-powered todo assistant.

Provides conversational interface for task management
using OpenAI and MCP tools.
"""

from typing import Annotated, Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import JWTPayload, verify_user_access
from app.database import get_session
from app.agents import run_agent
from app.services import ConversationService


router = APIRouter()


class ChatRequest(BaseModel):
    """Request body for chat endpoint."""

    conversation_id: Optional[int] = Field(
        default=None,
        description="Existing conversation ID (creates new if not provided)",
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's message to the assistant",
    )


class ToolCall(BaseModel):
    """Information about a tool call made by the agent."""

    tool: str = Field(description="Name of the tool that was called")
    input: Dict[str, Any] = Field(description="Input parameters for the tool")
    result: Any = Field(description="Result returned by the tool")


class ChatResponse(BaseModel):
    """Response from the chat endpoint."""

    conversation_id: int = Field(description="The conversation ID")
    response: str = Field(description="Assistant's response message")
    tool_calls: List[ToolCall] = Field(
        default_factory=list,
        description="List of tools invoked during processing",
    )


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    summary="Send a message to the AI assistant",
    description="""
Send a natural language message to the AI assistant to manage your tasks.

The assistant can:
- Add new tasks ("Add a task to buy groceries")
- List your tasks ("Show my tasks", "What's pending?")
- Mark tasks complete ("Mark task 3 as done")
- Delete tasks ("Delete task 2")
- Update tasks ("Change task 1 to 'Call mom tonight'")

Conversation history is maintained, so you can have multi-turn conversations.
""",
    responses={
        200: {
            "description": "Assistant response",
            "content": {
                "application/json": {
                    "example": {
                        "conversation_id": 1,
                        "response": "I've added 'Buy groceries' to your task list!",
                        "tool_calls": [
                            {
                                "tool": "add_task",
                                "input": {"title": "Buy groceries"},
                                "result": {
                                    "task_id": 5,
                                    "status": "created",
                                    "title": "Buy groceries",
                                },
                            }
                        ],
                    }
                }
            },
        },
        400: {"description": "Invalid request"},
        401: {"description": "Not authenticated"},
        403: {"description": "Access denied"},
        500: {"description": "Server error"},
    },
)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: Annotated[JWTPayload, Depends(verify_user_access)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ChatResponse:
    """
    Process a chat message and return AI response.

    Flow:
    1. Get or create conversation
    2. Load conversation history
    3. Save user message
    4. Run AI agent with tools
    5. Save assistant response
    6. Return response

    Args:
        user_id: User ID from URL path
        request: Chat request with message
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        ChatResponse with assistant's message and tool calls
    """
    try:
        # Initialize conversation service
        conv_service = ConversationService(session)

        # Get or create conversation
        conversation = await conv_service.get_or_create_conversation(
            request.conversation_id, user_id
        )

        # Load conversation history
        history = await conv_service.get_message_history(conversation.id)

        # Save user message
        await conv_service.add_user_message(
            conversation.id, user_id, request.message
        )

        # Run the AI agent
        result = await run_agent(
            session=session,
            user_id=user_id,
            message=request.message,
            conversation_history=history,
        )

        # Save assistant response
        await conv_service.add_assistant_message(
            conversation.id, user_id, result["response"]
        )

        # Update conversation timestamp
        await conv_service.update_conversation_timestamp(conversation)

        return ChatResponse(
            conversation_id=conversation.id,
            response=result["response"],
            tool_calls=[
                ToolCall(
                    tool=tc["tool"],
                    input=tc["input"],
                    result=tc["result"],
                )
                for tc in result.get("tool_calls", [])
            ],
        )

    except Exception as e:
        # Log the error (in production, use proper logging)
        print(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred processing your message: {str(e)}",
        )


@router.get(
    "/{user_id}/conversations",
    summary="List user's conversations",
    description="Get a list of all conversations for the authenticated user.",
)
async def list_conversations(
    user_id: str,
    current_user: Annotated[JWTPayload, Depends(verify_user_access)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """
    List all conversations for a user.

    Args:
        user_id: User ID from URL path
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        List of conversation summaries
    """
    from sqlmodel import select
    from app.models import Conversation

    query = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
    )
    result = await session.execute(query)
    conversations = result.scalars().all()

    return [
        {
            "id": conv.id,
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
        }
        for conv in conversations
    ]


@router.get(
    "/{user_id}/conversations/{conversation_id}/messages",
    summary="Get conversation messages",
    description="Get all messages in a specific conversation.",
)
async def get_conversation_messages(
    user_id: str,
    conversation_id: int,
    current_user: Annotated[JWTPayload, Depends(verify_user_access)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """
    Get all messages in a conversation.

    Args:
        user_id: User ID from URL path
        conversation_id: Conversation ID
        current_user: Authenticated user from JWT
        session: Database session

    Returns:
        List of messages in the conversation
    """
    conv_service = ConversationService(session)

    # Verify conversation belongs to user
    conversation = await conv_service.get_conversation(conversation_id, user_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    messages = await conv_service.get_messages(conversation_id, limit=100)

    return [
        {
            "id": msg.id,
            "role": msg.role,
            "content": msg.content,
            "created_at": msg.created_at.isoformat(),
        }
        for msg in messages
    ]
