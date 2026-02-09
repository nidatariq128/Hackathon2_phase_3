# TaskFlow AI Backend - Hugging Face Space

This is the backend for the TaskFlow AI application, deployed on Hugging Face Spaces.

## About

TaskFlow AI is a full-stack todo application with AI-powered features. This backend provides:

- Task management API (CRUD operations)
- User authentication support
- AI chatbot integration
- Health monitoring

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: PostgreSQL (configured via environment variables)
- **Authentication**: JWT tokens

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get task by ID |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

## API Documentation

Visit `/docs` for interactive API documentation (Swagger UI) or `/redoc` for ReDoc documentation.

## Environment Variables

This application requires the following environment variables to be set:

- `DATABASE_URL`: PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret
- `OPENROUTER_API_KEY`: API key for AI chatbot (optional)