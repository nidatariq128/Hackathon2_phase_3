# TaskFlow AI - Full-Stack Task Manager with AI Assistant

A modern, full-stack Todo application built with Next.js 16, FastAPI, and PostgreSQL. Features AI-powered chat assistant, beautiful gradient UI with glassmorphism effects, and full CRUD task management.

## Live Demo

- **Frontend (Vercel):** [https://frontend-theta-five-67.vercel.app](https://frontend-theta-five-67.vercel.app)
- **Backend API (Hugging Face):** [https://nidatariq-hachathon2-phase3.hf.space](https://nidatariq-hachathon2-phase3.hf.space)
- **API Docs:** [https://nidatariq-hachathon2-phase3.hf.space/docs](https://nidatariq-hachathon2-phase3.hf.space/docs)

## Features

- **JWT Authentication** - Secure user authentication with HS256 signed tokens
- **Task Management** - Full CRUD operations (create, read, update, delete)
- **AI Chat Assistant** - AI-powered task management assistant via OpenRouter (Phase III)
- **Modern UI** - Beautiful gradient design with smooth animations
- **Glassmorphism** - Frosted glass effects throughout the interface
- **Task Filters** - Filter by All, Pending, or Completed status
- **Responsive Design** - Works on all devices
- **Real-time Updates** - Optimistic UI updates

## Tech Stack

### Frontend
- **Next.js 16** - React framework with App Router & Turbopack
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API communication
- **Jose** - JWT token handling
- **Lucide React** - Icon library

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL database ORM with Pydantic validation
- **PostgreSQL (Neon)** - Serverless PostgreSQL database
- **PyJWT / Python-Jose** - JWT token generation and verification
- **OpenAI SDK** - AI chat via OpenRouter API
- **Uvicorn** - ASGI server

### Deployment
- **Vercel** - Frontend hosting
- **Hugging Face Spaces** - Backend hosting (Docker)
- **Neon** - Serverless PostgreSQL database

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- PostgreSQL database (or [Neon](https://neon.tech) account)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nidatariq128/Hackathon2_phase_3.git
cd Hackathon2_phase_3
```

2. **Set up environment variables**
```bash
# Root-level backend env
cp .env.example .env
# Edit .env with your DATABASE_URL and BETTER_AUTH_SECRET

# Backend env
cp backend/.env.example backend/.env
# Edit with your credentials

# Frontend env
cp frontend/.env.local.example frontend/.env.local
# Set NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Install Frontend Dependencies**
```bash
cd frontend
npm install
```

4. **Install Backend Dependencies**
```bash
cd ../backend
pip install -r requirements.txt
```

### Running Locally

**Start Backend (Terminal 1):**
```bash
cd backend
python app.py
```

**Start Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

**Access the app:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs

## Project Structure

```
Hackathon2_phase_3/
├── frontend/                # Next.js 16 frontend
│   ├── app/                # App Router pages
│   │   ├── page.tsx        # Login page
│   │   ├── signup/         # Signup page
│   │   └── dashboard/      # Dashboard (tasks, chat)
│   ├── components/         # React components
│   │   ├── tasks/          # Task CRUD components
│   │   ├── chat/           # AI chat components
│   │   └── ui/             # Shared UI components
│   ├── lib/                # Utilities
│   │   ├── api/            # API client & endpoints
│   │   ├── auth/           # Auth context & JWT
│   │   └── types/          # TypeScript types
│   └── vercel.json         # Vercel deployment config
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI app entry point
│   │   ├── config.py       # Pydantic settings
│   │   ├── database.py     # Database connection
│   │   ├── models/         # SQLModel models
│   │   ├── routes/         # API route handlers
│   │   ├── auth/           # JWT auth & dependencies
│   │   ├── agents/         # AI chat agent (Phase III)
│   │   └── utils/          # Exception handlers
│   ├── Dockerfile          # HF Spaces Docker config
│   ├── requirements.txt    # Python dependencies
│   └── app.py              # Uvicorn entry point
├── specs/                   # Feature specifications
├── history/                 # Development history
└── README.md
```

## API Endpoints

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

### Tasks
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create a task |
| GET | `/api/{user_id}/tasks/{id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |

### AI Chat (Phase III)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/{user_id}/chat` | Send message to AI assistant |

All `/api/*` endpoints require a valid JWT token:
```
Authorization: Bearer <jwt_token>
```

## Authentication

The app uses JWT (JSON Web Tokens) for authentication:
- Tokens signed with HS256 algorithm
- Shared secret between frontend and backend
- Stored in browser localStorage
- Automatically injected in API requests via Axios interceptor
- 7-day expiration

## Deployment

### Frontend (Vercel)
1. Push to GitHub
2. Import project in Vercel (select `frontend/` directory)
3. Set environment variable: `NEXT_PUBLIC_API_URL=https://nidatariq-hachathon2-phase3.hf.space`
4. Deploy

### Backend (Hugging Face Spaces)
1. Create a new Docker Space on Hugging Face
2. Push backend code to the Space repo
3. Set Secrets: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `OPENROUTER_API_KEY`
4. Space auto-builds and deploys on port 7860

## Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend
cd frontend
npm test
```

## Environment Variables

### Backend
| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `BETTER_AUTH_SECRET` | JWT signing secret (min 32 chars) |
| `OPENROUTER_API_KEY` | OpenRouter API key for AI chat |
| `AI_MODEL` | AI model (default: `nvidia/nemotron-3-nano-30b-a3b:free`) |
| `CORS_ORIGINS` | Allowed CORS origins (JSON array) |
| `API_PORT` | Server port (default: 8000) |

### Frontend
| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend API URL |

## License

MIT License - feel free to use this project for learning or production.

---

Built with Next.js, FastAPI, and Neon PostgreSQL
