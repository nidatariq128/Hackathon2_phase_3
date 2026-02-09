# Implementation Plan: AI-Powered Todo Chatbot

## Phase III - Hackathon II

**Spec Reference:** [spec.md](./spec.md)

---

## 1. Implementation Phases

### Phase 3.1: Database Models (Backend)
**Priority:** P0 - Critical Path
**Estimated Tasks:** 2

Create new SQLModel models for conversation persistence:
- `Conversation` model with user_id, timestamps
- `Message` model with conversation_id, role, content

**Dependencies:** None (existing database infrastructure)

---

### Phase 3.2: MCP Tools Implementation (Backend)
**Priority:** P0 - Critical Path
**Estimated Tasks:** 5

Implement MCP tools that wrap existing task operations:
- `add_task` - wraps task creation
- `list_tasks` - wraps task listing with filters
- `complete_task` - wraps task completion toggle
- `delete_task` - wraps task deletion
- `update_task` - wraps task update

**Dependencies:** Phase 3.1 (models)

---

### Phase 3.3: OpenAI Agent Setup (Backend)
**Priority:** P0 - Critical Path
**Estimated Tasks:** 2

Configure OpenAI Agents SDK:
- Create todo agent with system prompt
- Register MCP tools with agent
- Configure agent runner

**Dependencies:** Phase 3.2 (MCP tools)

---

### Phase 3.4: Chat API Endpoint (Backend)
**Priority:** P0 - Critical Path
**Estimated Tasks:** 3

Implement chat endpoint:
- POST `/api/{user_id}/chat` endpoint
- Conversation state management (create/load)
- Message persistence (user + assistant)

**Dependencies:** Phase 3.3 (agent setup)

---

### Phase 3.5: Frontend Chat UI (Frontend)
**Priority:** P1 - Important
**Estimated Tasks:** 3

Build ChatKit-based interface:
- Chat page component
- API client for chat endpoint
- Integration with existing auth

**Dependencies:** Phase 3.4 (chat endpoint)

---

## 2. Technical Decisions

### 2.1 Agent Architecture

**Decision:** Use OpenAI Agents SDK with function calling
**Rationale:**
- Native function calling support
- Built-in conversation management
- Easy tool registration

**Alternative Considered:** LangChain
**Why Rejected:** More complexity, hackathon specifies OpenAI Agents SDK

---

### 2.2 MCP Integration

**Decision:** Implement MCP tools as Python functions with decorators
**Rationale:**
- Simple integration with OpenAI function calling
- Tools can directly access database session
- Follows official MCP SDK patterns

---

### 2.3 Conversation Storage

**Decision:** Store full message history in PostgreSQL
**Rationale:**
- Stateless server architecture
- Persistence across restarts
- Easy to query and filter

**Alternative Considered:** Redis for session state
**Why Rejected:** Adds infrastructure complexity, PostgreSQL sufficient

---

### 2.4 Frontend Approach

**Decision:** Use OpenAI ChatKit with custom API backend
**Rationale:**
- Hackathon requirement
- Pre-built UI components
- Focus effort on backend logic

---

## 3. Component Diagram

```
┌────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (Next.js)                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    ChatKit Component                         │   │
│  │  - Message input                                             │   │
│  │  - Message history display                                   │   │
│  │  - Loading states                                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    API Client (chat.ts)                      │   │
│  │  - sendMessage(conversationId, message)                      │   │
│  │  - JWT token attachment                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
                              │
                              │ POST /api/{user_id}/chat
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                         BACKEND (FastAPI)                           │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Chat Router (chat.py)                     │   │
│  │  - JWT verification                                          │   │
│  │  - Request validation                                        │   │
│  │  - Response formatting                                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                 Conversation Service                         │   │
│  │  - Load/create conversation                                  │   │
│  │  - Store messages                                            │   │
│  │  - Build message history                                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Todo Agent (OpenAI)                       │   │
│  │  - System prompt                                             │   │
│  │  - Function calling                                          │   │
│  │  - Response generation                                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    MCP Tools                                 │   │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐                  │   │
│  │  │ add_task  │ │list_tasks │ │complete_  │                  │   │
│  │  │           │ │           │ │   task    │                  │   │
│  │  └───────────┘ └───────────┘ └───────────┘                  │   │
│  │  ┌───────────┐ ┌───────────┐                                │   │
│  │  │delete_task│ │update_task│                                │   │
│  │  │           │ │           │                                │   │
│  │  └───────────┘ └───────────┘                                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Database (Neon)                           │   │
│  │  - tasks table (existing)                                    │   │
│  │  - conversations table (new)                                 │   │
│  │  - messages table (new)                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────┘
```

---

## 4. API Flow Sequence

```
User                Frontend            Backend              OpenAI              Database
  │                    │                   │                   │                   │
  │──"Add buy milk"───▶│                   │                   │                   │
  │                    │──POST /chat──────▶│                   │                   │
  │                    │                   │──verify JWT──────▶│                   │
  │                    │                   │◀─────────────────│                   │
  │                    │                   │──load history────────────────────────▶│
  │                    │                   │◀───────────────────────────────────────│
  │                    │                   │──save user msg───────────────────────▶│
  │                    │                   │──run agent───────▶│                   │
  │                    │                   │                   │──function call───▶│
  │                    │                   │                   │   (add_task)      │
  │                    │                   │◀──────────────────│◀──────────────────│
  │                    │                   │──save asst msg───────────────────────▶│
  │                    │◀─────response─────│                   │                   │
  │◀────"Added!"───────│                   │                   │                   │
```

---

## 5. Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| OpenAI API rate limits | High | Implement retry logic, consider caching |
| Token usage costs | Medium | Limit conversation history length |
| Slow response times | Medium | Add loading states, optimize prompts |
| Tool execution errors | Medium | Comprehensive error handling |

---

## 6. Testing Strategy

### Unit Tests
- MCP tool functions
- Conversation service methods
- Message formatting

### Integration Tests
- Chat endpoint with mocked OpenAI
- Database operations
- JWT authentication flow

### E2E Tests
- Full chat flow
- Error scenarios
- Conversation persistence

---

## 7. Deployment Considerations

### Environment Variables
- `OPENAI_API_KEY` - Required for agent
- Existing vars unchanged

### Database Migrations
- Create conversations table
- Create messages table
- Add indexes for user_id, conversation_id

### CORS
- Existing CORS config sufficient
- ChatKit uses same origin

---

## 8. Success Metrics

| Metric | Target |
|--------|--------|
| Chat response time | < 5 seconds |
| Tool execution accuracy | > 95% |
| Error rate | < 5% |
| Conversation persistence | 100% |
