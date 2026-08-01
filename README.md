# Nexora University – UniSphere AI

An AI-powered university information portal using Retrieval-Augmented Generation (RAG) to provide instant access to official university information.

## Project Structure

```
nexora/
├── frontend/          # Next.js public website + admin portal + chat UI
├── backend/           # FastAPI REST API
├── ai/                # RAG pipeline (LangChain, Groq, Pinecone)
├── knowledge_base/    # University PDF documents for AI indexing
├── shared/            # Shared utilities
├── types/             # Shared TypeScript types
├── lib/               # Shared libraries
├── components/        # Shared components
├── hooks/             # Shared React hooks
└── utils/             # Shared utilities
```

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Backend | FastAPI (Python) |
| Database | Supabase PostgreSQL |
| Auth | Supabase Auth (admin only) |
| Storage | Supabase Storage |
| LLM | Groq – Llama 3.3 70B |
| RAG | LangChain |
| Embeddings | BAAI/bge-large-en-v1.5 |
| Vector DB | Pinecone |

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- Supabase account
- Groq API key
- Pinecone account

### 1. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Frontend runs at http://localhost:3000

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env          # Fill in API keys
python run.py
```

Backend runs at http://localhost:8000

### 3. Database

1. Create a Supabase project
2. Run `backend/supabase/schema.sql` in the SQL Editor
3. Add Supabase URL and keys to `.env` files

### 4. Knowledge Base

1. Add university PDFs to `knowledge_base/`
2. Index them:

```bash
python -m ai.ingest_batch
```

## Features

- **Public Website** – University info, departments, faculty, admissions, placements, etc.
- **UniSphere AI** – RAG chatbot with document-based answers and source citations
- **Document Library** – Search, view, and download official documents
- **Admin Portal** – Manage documents, notices, events, and analytics
- **Notices & Events** – Official announcements and campus activities

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/chat` | Send message to UniSphere AI |
| GET | `/api/documents` | List documents |
| POST | `/api/documents/upload` | Upload and index a PDF |

## License

Private – Nexora University Project
