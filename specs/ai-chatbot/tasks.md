# Tasks: AI-Powered Todo Chatbot

## Phase III - Hackathon II

**Spec:** [spec.md](./spec.md)
**Plan:** [plan.md](./plan.md)

---

## Task Summary

| ID | Task | Status | Priority |
|----|------|--------|----------|
| T-301 | Create Conversation and Message models | pending | P0 |
| T-302 | Add database migrations for new tables | pending | P0 |
| T-303 | Implement add_task MCP tool | pending | P0 |
| T-304 | Implement list_tasks MCP tool | pending | P0 |
| T-305 | Implement complete_task MCP tool | pending | P0 |
| T-306 | Implement delete_task MCP tool | pending | P0 |
| T-307 | Implement update_task MCP tool | pending | P0 |
| T-308 | Create OpenAI Agent with tools | pending | P0 |
| T-309 | Implement conversation service | pending | P0 |
| T-310 | Create POST /api/{user_id}/chat endpoint | pending | P0 |
| T-311 | Add chat API client to frontend | pending | P1 |
| T-312 | Create ChatKit UI component | pending | P1 |
| T-313 | Add chat page to dashboard | pending | P1 |
| T-314 | Write integration tests | pending | P2 |
| T-315 | Update documentation | pending | P2 |

---

## Detailed Tasks

### T-301: Create Conversation and Message Models

**Priority:** P0
**Spec Reference:** spec.md §4 Database Schema

**Description:**
Create SQLModel models for conversation and message persistence.

**Acceptance Criteria:**
- [ ] Conversation model with id, user_id, created_at, updated_at
- [ ] Message model with id, user_id, conversation_id, role, content, created_at
- [ ] Foreign key relationship between Message and Conversation
- [ ] Indexes on user_id and conversation_id

**Files to Create:**
- `backend/app/models/conversation.py`
- `backend/app/models/message.py`

**Files to Modify:**
- `backend/app/models/__init__.py`

---

### T-302: Add Database Migrations

**Priority:** P0
**Depends On:** T-301

**Description:**
Ensure new tables are created in the database on startup.

**Acceptance Criteria:**
- [ ] conversations table created with proper schema
- [ ] messages table created with proper schema
- [ ] Tables created automatically on app startup

**Files to Modify:**
- `backend/app/database.py` (if needed)

---

### T-303: Implement add_task MCP Tool

**Priority:** P0
**Spec Reference:** spec.md §6.1

**Description:**
Create MCP tool function for adding tasks.

**Acceptance Criteria:**
- [ ] Function accepts user_id, title, description (optional)
- [ ] Creates task in database
- [ ] Returns task_id, status, title
- [ ] Handles validation errors

**Test Cases:**
```python
# Success case
add_task(user_id="user_john", title="Buy milk")
# Returns: {"task_id": 1, "status": "created", "title": "Buy milk"}

# With description
add_task(user_id="user_john", title="Shopping", description="Weekly groceries")
# Returns: {"task_id": 2, "status": "created", "title": "Shopping"}
```

**Files to Create:**
- `backend/app/agents/tools.py`

---

### T-304: Implement list_tasks MCP Tool

**Priority:** P0
**Spec Reference:** spec.md §6.2

**Description:**
Create MCP tool function for listing tasks.

**Acceptance Criteria:**
- [ ] Function accepts user_id, status (optional)
- [ ] Filters by status: all, pending, completed
- [ ] Returns array of task objects
- [ ] Only returns user's own tasks

**Test Cases:**
```python
# All tasks
list_tasks(user_id="user_john", status="all")
# Returns: [{"id": 1, "title": "Buy milk", "completed": false}, ...]

# Pending only
list_tasks(user_id="user_john", status="pending")
# Returns: [{"id": 1, "title": "Buy milk", "completed": false}]
```

**Files to Modify:**
- `backend/app/agents/tools.py`

---

### T-305: Implement complete_task MCP Tool

**Priority:** P0
**Spec Reference:** spec.md §6.3

**Description:**
Create MCP tool function for marking tasks complete.

**Acceptance Criteria:**
- [ ] Function accepts user_id, task_id
- [ ] Marks task as completed
- [ ] Returns task_id, status, title
- [ ] Validates task ownership

**Test Cases:**
```python
# Success case
complete_task(user_id="user_john", task_id=1)
# Returns: {"task_id": 1, "status": "completed", "title": "Buy milk"}

# Task not found
complete_task(user_id="user_john", task_id=999)
# Returns: {"error": "Task not found"}
```

**Files to Modify:**
- `backend/app/agents/tools.py`

---

### T-306: Implement delete_task MCP Tool

**Priority:** P0
**Spec Reference:** spec.md §6.4

**Description:**
Create MCP tool function for deleting tasks.

**Acceptance Criteria:**
- [ ] Function accepts user_id, task_id
- [ ] Deletes task from database
- [ ] Returns task_id, status, title
- [ ] Validates task ownership

**Test Cases:**
```python
# Success case
delete_task(user_id="user_john", task_id=1)
# Returns: {"task_id": 1, "status": "deleted", "title": "Buy milk"}
```

**Files to Modify:**
- `backend/app/agents/tools.py`

---

### T-307: Implement update_task MCP Tool

**Priority:** P0
**Spec Reference:** spec.md §6.5

**Description:**
Create MCP tool function for updating tasks.

**Acceptance Criteria:**
- [ ] Function accepts user_id, task_id, title (optional), description (optional)
- [ ] Updates specified fields
- [ ] Returns task_id, status, title
- [ ] Validates task ownership

**Test Cases:**
```python
# Update title
update_task(user_id="user_john", task_id=1, title="Buy groceries")
# Returns: {"task_id": 1, "status": "updated", "title": "Buy groceries"}
```

**Files to Modify:**
- `backend/app/agents/tools.py`

---

### T-308: Create OpenAI Agent with Tools

**Priority:** P0
**Depends On:** T-303, T-304, T-305, T-306, T-307

**Description:**
Set up OpenAI Agent with registered MCP tools.

**Acceptance Criteria:**
- [ ] Agent configured with system prompt
- [ ] All 5 MCP tools registered
- [ ] Agent can process natural language and call tools
- [ ] Returns formatted responses

**Files to Create:**
- `backend/app/agents/__init__.py`
- `backend/app/agents/todo_agent.py`

---

### T-309: Implement Conversation Service

**Priority:** P0
**Depends On:** T-301, T-302

**Description:**
Create service for managing conversation state.

**Acceptance Criteria:**
- [ ] Create new conversation
- [ ] Load existing conversation with messages
- [ ] Save user message
- [ ] Save assistant message
- [ ] Build message history for agent

**Files to Create:**
- `backend/app/services/__init__.py`
- `backend/app/services/conversation.py`

---

### T-310: Create POST /api/{user_id}/chat Endpoint

**Priority:** P0
**Depends On:** T-308, T-309

**Description:**
Implement the main chat API endpoint.

**Acceptance Criteria:**
- [ ] Accepts conversation_id (optional) and message (required)
- [ ] JWT authentication required
- [ ] Verifies user_id matches token
- [ ] Creates/loads conversation
- [ ] Runs agent and returns response
- [ ] Returns conversation_id, response, tool_calls

**Files to Create:**
- `backend/app/routes/chat.py`

**Files to Modify:**
- `backend/app/main.py` (register router)

---

### T-311: Add Chat API Client to Frontend

**Priority:** P1
**Depends On:** T-310

**Description:**
Create TypeScript API client for chat endpoint.

**Acceptance Criteria:**
- [ ] sendMessage function with conversation_id and message
- [ ] JWT token attached automatically
- [ ] Error handling for API errors
- [ ] TypeScript types for request/response

**Files to Create:**
- `frontend/lib/api/chat.ts`
- `frontend/lib/types/chat.ts`

---

### T-312: Create ChatKit UI Component

**Priority:** P1
**Depends On:** T-311

**Description:**
Build chat interface using OpenAI ChatKit.

**Acceptance Criteria:**
- [ ] Message input field
- [ ] Message history display
- [ ] Loading state while waiting for response
- [ ] Error display
- [ ] Auto-scroll to latest message

**Files to Create:**
- `frontend/components/chat/ChatInterface.tsx`

---

### T-313: Add Chat Page to Dashboard

**Priority:** P1
**Depends On:** T-312

**Description:**
Create chat page in dashboard.

**Acceptance Criteria:**
- [ ] Route: /dashboard/chat
- [ ] Protected by authentication
- [ ] Navigation link in dashboard layout
- [ ] Welcome message on load

**Files to Create:**
- `frontend/app/dashboard/chat/page.tsx`

**Files to Modify:**
- `frontend/app/dashboard/layout.tsx` (add nav link)

---

### T-314: Write Integration Tests

**Priority:** P2
**Depends On:** T-310

**Description:**
Create tests for chat functionality.

**Acceptance Criteria:**
- [ ] Test chat endpoint with mocked OpenAI
- [ ] Test conversation persistence
- [ ] Test MCP tools
- [ ] Test authentication

**Files to Create:**
- `backend/tests/test_chat.py`
- `backend/tests/test_conversation.py`
- `backend/tests/test_mcp_tools.py`

---

### T-315: Update Documentation

**Priority:** P2

**Description:**
Update README and add Phase III docs.

**Acceptance Criteria:**
- [ ] Update README with Phase III setup
- [ ] Document environment variables
- [ ] Add chat API documentation
- [ ] Include example conversations

**Files to Modify:**
- `README.md`
- `backend/README.md`
- `frontend/README.md`

---

## Implementation Order

```
T-301 (Models)
    │
    ▼
T-302 (Migrations)
    │
    ├──────────────────────────────────────┐
    ▼                                      ▼
T-303 ─► T-304 ─► T-305 ─► T-306 ─► T-307  T-309
(MCP Tools)                                (Conv Service)
    │                                      │
    └──────────────┬───────────────────────┘
                   ▼
               T-308 (Agent)
                   │
                   ▼
               T-310 (Endpoint)
                   │
                   ▼
               T-311 (API Client)
                   │
                   ▼
               T-312 (ChatKit UI)
                   │
                   ▼
               T-313 (Chat Page)
                   │
                   ▼
        T-314 (Tests) + T-315 (Docs)
```

---

## Notes

- OpenAI API key required before starting T-308
- Test each MCP tool individually before agent integration
- Use streaming for better UX (optional enhancement)
