# Backend Architecture – Nexora University UniSphere AI

## Overview

The backend is a **FastAPI** application that serves as the central API layer between the Next.js frontend and external services (Supabase, Pinecone, Groq). It follows a **layered architecture** where each layer has a single responsibility.

```
Frontend (Next.js)
        │
        ▼
   API Layer          ← HTTP routes, request validation
        │
        ▼
  Service Layer       ← Business logic (next phase)
        │
   ┌────┴────┐
   ▼         ▼
Database    RAG Layer
(Supabase)  (Pinecone + Groq + Embeddings)
```

---

## Folder Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry, CORS, router registration
│   ├── config.py            # Environment-based settings (Pydantic)
│   │
│   ├── api/                 # HTTP route handlers (thin controllers)
│   │   ├── router.py        # Aggregates all route modules
│   │   ├── auth.py          # Admin login, logout, password reset
│   │   ├── documents.py     # Document CRUD + upload
│   │   ├── chat.py          # UniSphere AI chatbot
│   │   ├── notices.py         # Notice management
│   │   ├── events.py        # Event management
│   │   ├── analytics.py     # Usage analytics
│   │   └── settings.py      # University settings
│   │
│   ├── services/            # Business logic (empty – next phase)
│   ├── models/              # Domain / DB models (empty – next phase)
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── common.py
│   │   ├── auth.py
│   │   └── api.py
│   │
│   ├── database/            # Supabase client configuration
│   │   └── supabase.py
│   │
│   ├── rag/                 # AI / RAG client configuration
│   │   ├── pinecone_client.py
│   │   ├── groq_client.py
│   │   └── embeddings.py
│   │
│   ├── auth/                # Auth dependencies and middleware
│   │   └── dependencies.py
│   │
│   └── utils/               # Shared helper functions
│       └── helpers.py
│
├── requirements.txt
├── .env.example
├── run.py
└── ARCHITECTURE.md
```

---

## Layer Responsibilities

### 1. API Layer (`app/api/`)

- Receives HTTP requests from the frontend
- Validates input using Pydantic schemas
- Delegates to the service layer (next phase)
- Returns structured JSON responses
- **Current state:** All routes return placeholder responses

### 2. Schemas Layer (`app/schemas/`)

- Defines request bodies and response shapes
- Provides automatic validation and OpenAPI documentation
- Keeps API contracts separate from business logic

### 3. Service Layer (`app/services/`) — Next Phase

- Contains all business logic
- Orchestrates calls to database and RAG layers
- Examples: `document_service.upload_and_index()`, `chat_service.generate_response()`

### 4. Database Layer (`app/database/`)

- **Supabase client** configured with two keys:
  - `service_key` → admin operations (bypasses RLS)
  - `anon_key` → public operations (respects RLS)
- Will handle PostgreSQL queries and Storage file operations

### 5. RAG Layer (`app/rag/`)

- **Pinecone** → vector storage and similarity search
- **Groq** → Llama 3.3 70B Instruct for response generation
- **Embeddings** → BAAI/bge-large-en-v1.5 for text-to-vector conversion
- Clients are configured but not yet wired to business logic

### 6. Auth Layer (`app/auth/`)

- Admin-only authentication via Supabase Auth
- `get_current_admin()` dependency will protect admin routes
- **Current state:** Returns 501 Not Implemented

---

## API Endpoints (Placeholder)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/auth/login` | Admin login |
| POST | `/api/v1/auth/logout` | Admin logout |
| GET | `/api/v1/documents/` | List documents |
| POST | `/api/v1/documents/upload` | Upload PDF |
| POST | `/api/v1/chat/` | Send chat message |
| GET | `/api/v1/notices/` | List notices |
| GET | `/api/v1/events/` | List events |
| GET | `/api/v1/analytics/overview` | Dashboard stats |
| GET | `/api/v1/settings/` | Get university settings |

Full interactive docs available at `/docs` when the server is running.

---

## Configuration

All settings are loaded from environment variables via `app/config.py` using Pydantic Settings. Placeholder values are used until real API keys are provided.

Copy `.env.example` to `.env` when ready:

```bash
cd backend
cp .env.example .env
```

---

## Running the Server

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python run.py
```

Server starts at http://localhost:8000  
API docs at http://localhost:8000/docs

---

## Next Phase (Awaiting Approval)

1. **Authentication** – Supabase Auth login/logout, JWT validation, protected routes
2. **Database operations** – CRUD for documents, notices, events, settings
3. **RAG pipeline** – Document ingestion, vector indexing, chat response generation
4. **Analytics** – Track AI queries, document downloads, page views
