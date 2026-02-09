# Task: T-001, T-310 - API Routes
# Spec: specs/task-crud/spec.md, specs/ai-chatbot/spec.md
"""
API routes package.

Contains FastAPI routers for API endpoints.
"""

from app.routes.tasks import router as tasks_router
from app.routes.health import router as health_router
from app.routes.chat import router as chat_router

__all__ = [
    "tasks_router",
    "health_router",
    "chat_router",
]
