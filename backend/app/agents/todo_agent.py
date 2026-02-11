# Task: T-308 - Create OpenAI Agent with Tools
# Spec: specs/ai-chatbot/spec.md §7
# Plan: specs/ai-chatbot/plan.md
"""
Todo AI Agent using Groq API (OpenAI-compatible).

Configures the AI agent with system prompt and MCP tools
for natural language task management.

Uses Groq's free API with Llama models for cost-effective
AI chatbot functionality.
"""

import json
from typing import Any, Dict, List, Optional

from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents import tools
from app.config import settings

# System prompt for the todo agent
SYSTEM_PROMPT = """You are a helpful todo assistant. You help users manage their tasks through conversation.

Available tools:
- add_task: Create new tasks
- list_tasks: View tasks (filter by status: all, pending, completed)
- complete_task: Mark tasks as done
- delete_task: Remove tasks
- update_task: Modify task title or description

Guidelines:
1. Always confirm actions with friendly, concise responses
2. If user mentions a task by name but you need the ID, list tasks first to find it
3. Handle errors gracefully with helpful messages
4. Be concise but friendly
5. When listing tasks, format them nicely for the user
6. If no tasks exist, let the user know and suggest adding one

Examples of what users might say:
- "Add a task to buy groceries" → use add_task
- "Show my tasks" or "What do I need to do?" → use list_tasks
- "Mark task 3 as done" or "I finished task 3" → use complete_task
- "Delete task 2" or "Remove the shopping task" → use delete_task
- "Change task 1 to 'Call mom tonight'" → use update_task
"""


class TodoAgent:
    """
    Todo AI Agent that processes natural language and manages tasks.

    Uses OpenRouter's API for function calling with MCP tools.
    OpenRouter provides access to various free and paid models.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Todo Agent with OpenRouter.

        Args:
            api_key: OpenRouter API key (defaults to settings)
        """
        # Use OpenRouter's OpenAI-compatible endpoint
        self.client = AsyncOpenAI(
            api_key=api_key or settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            default_headers={
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "Todo AI Assistant",
            },
        )
        # Use model from settings
        self.model = settings.AI_MODEL
        self.tools = tools.get_all_tools()

    async def process_message(
        self,
        session: AsyncSession,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        """
        Process a user message and return agent response.

        Args:
            session: Database session for tool execution
            user_id: User ID for tool context
            message: User's message
            conversation_history: Previous messages in conversation

        Returns:
            Dict with response text and tool_calls list
        """
        # Build messages array
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history,
            {"role": "user", "content": message},
        ]

        tool_calls_made = []

        try:
            # Initial API call
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto",
            )

            assistant_message = response.choices[0].message

            # Debug: print response structure
            print(f"DEBUG: assistant_message = {str(assistant_message).encode('utf-8', errors='replace').decode('utf-8')}")
            print(f"DEBUG: tool_calls = {assistant_message.tool_calls}")

            # Process tool calls if any
            while assistant_message.tool_calls:
                # Add assistant message to conversation (exclude unsupported fields)
                assistant_dict = {
                    "role": "assistant",
                    "content": assistant_message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in assistant_message.tool_calls
                    ],
                }
                messages.append(assistant_dict)

                # Execute each tool call
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    # Execute the tool
                    result = await self._execute_tool(
                        session, user_id, tool_name, tool_args
                    )

                    # Record the tool call
                    tool_calls_made.append(
                        {
                            "tool": tool_name,
                            "input": tool_args,
                            "result": result,
                        }
                    )

                    # Add tool result to messages
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": json.dumps(result),
                        }
                    )

                # Get next response
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=self.tools,
                    tool_choice="auto",
                )
                assistant_message = response.choices[0].message

            return {
                "response": assistant_message.content or "I processed your request.",
                "tool_calls": tool_calls_made,
            }

        except Exception as e:
            return {
                "response": f"I encountered an error: {str(e)}. Please try again.",
                "tool_calls": tool_calls_made,
                "error": str(e),
            }

    async def _execute_tool(
        self,
        session: AsyncSession,
        user_id: str,
        tool_name: str,
        tool_args: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Execute a tool with the given arguments.

        Args:
            session: Database session
            user_id: User ID for context
            tool_name: Name of the tool to execute
            tool_args: Arguments for the tool

        Returns:
            Tool execution result
        """
        if tool_name == "add_task":
            return await tools.add_task(
                session=session,
                user_id=user_id,
                title=tool_args.get("title", ""),
                description=tool_args.get("description"),
            )
        elif tool_name == "list_tasks":
            return await tools.list_tasks(
                session=session,
                user_id=user_id,
                status=tool_args.get("status", "all"),
            )
        elif tool_name == "complete_task":
            return await tools.complete_task(
                session=session,
                user_id=user_id,
                task_id=tool_args.get("task_id"),
            )
        elif tool_name == "delete_task":
            return await tools.delete_task(
                session=session,
                user_id=user_id,
                task_id=tool_args.get("task_id"),
            )
        elif tool_name == "update_task":
            return await tools.update_task(
                session=session,
                user_id=user_id,
                task_id=tool_args.get("task_id"),
                title=tool_args.get("title"),
                description=tool_args.get("description"),
            )
        else:
            return {"error": f"Unknown tool: {tool_name}"}


# Singleton agent instance
_agent: Optional[TodoAgent] = None


def get_agent() -> TodoAgent:
    """Get or create the singleton agent instance."""
    import os
    from dotenv import dotenv_values

    global _agent
    # Load directly from .env file to bypass system env vars
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    env_values = dotenv_values(env_path)
    api_key = env_values.get('OPENROUTER_API_KEY', settings.OPENROUTER_API_KEY)

    print(f"DEBUG: Using API key from .env: {api_key[:20]}...")
    print(f"DEBUG: Using model: {settings.AI_MODEL}")

    _agent = TodoAgent(api_key=api_key)
    return _agent


async def run_agent(
    session: AsyncSession,
    user_id: str,
    message: str,
    conversation_history: List[Dict[str, str]],
) -> Dict[str, Any]:
    """
    Convenience function to run the agent.

    Args:
        session: Database session
        user_id: User ID
        message: User message
        conversation_history: Previous messages

    Returns:
        Agent response with tool calls
    """
    agent = get_agent()
    return await agent.process_message(session, user_id, message, conversation_history)
