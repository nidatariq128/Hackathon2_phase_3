# Feature: AI-Powered Todo Chatbot

## Phase III - Hackathon II

---

## 1. Overview

Transform the Phase II Todo application into an AI-powered chatbot that allows users to manage their tasks through natural language conversation.

### 1.1 Objective

Create a conversational interface using:
- **OpenAI ChatKit** for the frontend UI
- **OpenAI Agents SDK** for AI logic
- **Official MCP SDK** for task operations as tools
- **Stateless architecture** with conversation persistence in database

### 1.2 Success Criteria

- [ ] Users can manage tasks via natural language
- [ ] Conversation history persists across sessions
- [ ] MCP tools handle all task operations
- [ ] Server remains stateless (scalable)
- [ ] Graceful error handling

---

## 2. Architecture

```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│  ChatKit UI     │────▶│  │         Chat Endpoint                  │  │     │    Neon DB      │
│  (Frontend)     │     │  │  POST /api/{user_id}/chat              │  │     │  (PostgreSQL)   │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │  - tasks        │
│                 │     │                  ▼                           │     │  - conversations│
│                 │     │  ┌────────────────────────────────────────┐  │     │  - messages     │
│                 │◀────│  │      OpenAI Agents SDK                 │  │     │                 │
│                 │     │  │      (Agent + Runner)                  │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │────▶│                 │
│                 │     │  │         MCP Tools                      │  │     │                 │
│                 │     │  │  (Task CRUD Operations)                │  │◀────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

---

## 3. Technology Stack

| Component | Technology | Version |
|-----------|------------|---------|
| Frontend Chat UI | OpenAI ChatKit | Latest |
| Backend API | FastAPI | 0.124.4 |
| AI Framework | OpenAI Agents SDK | Latest |
| MCP Tools | Official MCP Python SDK | Latest |
| ORM | SQLModel | 0.0.31 |
| Database | Neon PostgreSQL | - |
| Authentication | Better Auth (JWT) | Existing |

---

## 4. Database Schema

### 4.1 New Models

#### Conversation Model
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

#### Message Model
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str  # "user" | "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 4.2 Existing Models (No Changes)
- `Task` model from Phase II remains unchanged

---

## 5. API Specification

### 5.1 Chat Endpoint

**POST** `/api/{user_id}/chat`

#### Request Body
```json
{
  "conversation_id": 123,       // Optional: existing conversation ID
  "message": "Add a task to buy groceries"  // Required: user message
}
```

#### Response
```json
{
  "conversation_id": 123,
  "response": "I've added 'Buy groceries' to your task list!",
  "tool_calls": [
    {
      "tool": "add_task",
      "input": {"title": "Buy groceries"},
      "result": {"task_id": 5, "status": "created"}
    }
  ]
}
```

#### Error Responses
| Status | Description |
|--------|-------------|
| 400 | Invalid request body |
| 401 | Not authenticated |
| 403 | Access denied (user_id mismatch) |
| 500 | Server error |

---

## 6. MCP Tools Specification

### 6.1 add_task

| Field | Value |
|-------|-------|
| **Purpose** | Create a new task |
| **Parameters** | `user_id` (str, required), `title` (str, required), `description` (str, optional) |
| **Returns** | `task_id`, `status`, `title` |

**Example:**
```json
// Input
{"user_id": "user_john", "title": "Buy groceries", "description": "Milk, eggs, bread"}

// Output
{"task_id": 5, "status": "created", "title": "Buy groceries"}
```

### 6.2 list_tasks

| Field | Value |
|-------|-------|
| **Purpose** | Retrieve tasks with optional filter |
| **Parameters** | `user_id` (str, required), `status` (str, optional: "all", "pending", "completed") |
| **Returns** | Array of task objects |

**Example:**
```json
// Input
{"user_id": "user_john", "status": "pending"}

// Output
[
  {"id": 1, "title": "Buy groceries", "completed": false},
  {"id": 2, "title": "Call mom", "completed": false}
]
```

### 6.3 complete_task

| Field | Value |
|-------|-------|
| **Purpose** | Mark a task as complete |
| **Parameters** | `user_id` (str, required), `task_id` (int, required) |
| **Returns** | `task_id`, `status`, `title` |

**Example:**
```json
// Input
{"user_id": "user_john", "task_id": 3}

// Output
{"task_id": 3, "status": "completed", "title": "Call mom"}
```

### 6.4 delete_task

| Field | Value |
|-------|-------|
| **Purpose** | Remove a task |
| **Parameters** | `user_id` (str, required), `task_id` (int, required) |
| **Returns** | `task_id`, `status`, `title` |

**Example:**
```json
// Input
{"user_id": "user_john", "task_id": 2}

// Output
{"task_id": 2, "status": "deleted", "title": "Old task"}
```

### 6.5 update_task

| Field | Value |
|-------|-------|
| **Purpose** | Modify task title or description |
| **Parameters** | `user_id` (str, required), `task_id` (int, required), `title` (str, optional), `description` (str, optional) |
| **Returns** | `task_id`, `status`, `title` |

**Example:**
```json
// Input
{"user_id": "user_john", "task_id": 1, "title": "Buy groceries and fruits"}

// Output
{"task_id": 1, "status": "updated", "title": "Buy groceries and fruits"}
```

---

## 7. Agent Behavior Specification

### 7.1 Natural Language Mapping

| User Says | Agent Action |
|-----------|--------------|
| "Add a task to buy groceries" | Call `add_task` with title "Buy groceries" |
| "Show me all my tasks" | Call `list_tasks` with status "all" |
| "What's pending?" | Call `list_tasks` with status "pending" |
| "Mark task 3 as complete" | Call `complete_task` with task_id 3 |
| "Delete the meeting task" | Call `list_tasks` first, then `delete_task` |
| "Change task 1 to 'Call mom tonight'" | Call `update_task` with new title |
| "I need to remember to pay bills" | Call `add_task` with title "Pay bills" |
| "What have I completed?" | Call `list_tasks` with status "completed" |

### 7.2 Agent System Prompt

```
You are a helpful todo assistant. You help users manage their tasks through conversation.

Available tools:
- add_task: Create new tasks
- list_tasks: View tasks (filter by status)
- complete_task: Mark tasks done
- delete_task: Remove tasks
- update_task: Modify tasks

Guidelines:
- Always confirm actions with friendly responses
- If user mentions a task by name but you need the ID, list tasks first
- Handle errors gracefully with helpful messages
- Be concise but friendly
```

---

## 8. Conversation Flow (Stateless)

1. **Receive** user message via POST `/api/{user_id}/chat`
2. **Fetch** conversation history from database (if conversation_id provided)
3. **Build** message array for agent (history + new message)
4. **Store** user message in database
5. **Run** agent with MCP tools
6. **Agent** invokes appropriate MCP tool(s)
7. **Store** assistant response in database
8. **Return** response to client
9. **Server** holds NO state (ready for next request)

---

## 9. Frontend Integration

### 9.1 OpenAI ChatKit Setup

```typescript
// chatConfig.ts
export const chatConfig = {
  apiEndpoint: '/api/{user_id}/chat',
  theme: 'light',
  placeholder: 'Ask me to manage your tasks...',
  welcomeMessage: 'Hi! I can help you manage your tasks. Try saying "Show my tasks" or "Add a task to..."'
};
```

### 9.2 Domain Allowlist (Production)

For deployed ChatKit:
1. Deploy frontend to get production URL
2. Add domain to OpenAI allowlist: https://platform.openai.com/settings/organization/security/domain-allowlist
3. Get domain key and configure in environment

---

## 10. Environment Variables

### Backend (.env)
```env
# Existing
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...

# New for Phase III
OPENAI_API_KEY=sk-...
```

### Frontend (.env.local)
```env
# Existing
NEXT_PUBLIC_API_URL=http://localhost:8000

# New for Phase III (production only)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=...
```

---

## 11. Dependencies

### Backend (requirements.txt additions)
```
openai-agents>=0.1.0
mcp>=1.0.0
```

### Frontend (package.json additions)
```json
{
  "@openai/chatkit": "^latest"
}
```

---

## 12. File Structure

```
backend/
├── app/
│   ├── agents/              # NEW
│   │   ├── __init__.py
│   │   ├── todo_agent.py    # OpenAI Agent setup
│   │   └── tools.py         # MCP tool definitions
│   ├── models/
│   │   ├── task.py          # Existing
│   │   ├── conversation.py  # NEW
│   │   └── message.py       # NEW
│   ├── routes/
│   │   ├── tasks.py         # Existing
│   │   └── chat.py          # NEW
│   └── main.py              # Add chat router

frontend/
├── app/
│   ├── dashboard/
│   │   ├── tasks/           # Existing
│   │   └── chat/            # NEW
│   │       └── page.tsx     # ChatKit UI
│   └── ...
├── components/
│   └── chat/                # NEW
│       └── ChatInterface.tsx
└── lib/
    └── api/
        ├── tasks.ts         # Existing
        └── chat.ts          # NEW
```

---

## 13. Acceptance Criteria

### 13.1 Functional Requirements

- [ ] User can start a new conversation
- [ ] User can continue existing conversation
- [ ] User can add tasks via natural language
- [ ] User can list tasks via natural language
- [ ] User can mark tasks complete via natural language
- [ ] User can delete tasks via natural language
- [ ] User can update tasks via natural language
- [ ] Conversation history persists in database
- [ ] Server restarts don't lose conversation state

### 13.2 Non-Functional Requirements

- [ ] Response time < 5 seconds for AI responses
- [ ] JWT authentication required for all chat endpoints
- [ ] User isolation (users only see their conversations)
- [ ] Graceful error handling with user-friendly messages

---

## 14. Out of Scope

- Voice input (Phase V bonus)
- Multi-language support (Phase V bonus)
- Real-time streaming responses
- File attachments in chat

---

## 15. References

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [OpenAI ChatKit](https://platform.openai.com/docs/guides/chatkit)
- [Phase II Spec](../task-crud/spec.md)
