# NovaMind Lite

A production-grade REST API for storing, tagging, searching, and querying notes using a large language model. Built with FastAPI, SQLAlchemy, and Groq.

---

## Overview

NovaMind Lite is a fully authenticated notes API with an integrated AI layer. Users can register, log in, manage their notes, and request AI-generated summaries of any note using the Groq LLM backend. The project is containerized, tested, and CI-ready.

---

## Architecture

```
novamind_lite/
├── app/
│   ├── main.py               # FastAPI application entry point, middleware, exception handlers
│   ├── config.py             # Centralized Pydantic Settings configuration
│   ├── dependencies.py       # Reusable FastAPI dependencies (get_db, get_current_user)
│   ├── exceptions.py         # Custom domain exception classes
│   ├── db/
│   │   └── session.py        # SQLAlchemy engine, session, and base setup
│   ├── models/
│   │   └── database.py       # ORM models: Note, User
│   ├── routers/
│   │   ├── notes.py          # CRUD endpoints for notes
│   │   ├── auth.py           # Register and login endpoints
│   │   └── ai.py             # AI summarization endpoint
│   ├── schemas/
│   │   ├── note.py           # Pydantic schemas: NoteCreate, NoteResponse
│   │   └── user.py           # Pydantic schemas: UserCreate, UserResponse, Token
│   └── services/
│       ├── auth_service.py   # Password hashing, JWT creation and decoding
│       └── ai_service.py     # Groq async LLM client and summarization logic
├── tests/
│   ├── conftest.py           # In-memory DB override, fake user fixture
│   └── test_notes.py         # Route-level tests using TestClient
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/ci.yml
└── requirements.txt
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | SQLite via SQLAlchemy ORM |
| Authentication | JWT (PyJWT) + bcrypt password hashing |
| AI Layer | Groq API (llama3-8b-8192) |
| Validation | Pydantic v2 |
| Testing | Pytest + Starlette TestClient |
| Containerization | Docker + Docker Compose |
| CI | GitHub Actions |
| Config | Pydantic Settings |

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and receive JWT token | No |

### Notes

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/notes/` | List all notes | Yes |
| GET | `/notes/{note_id}` | Get a single note by ID | Yes |
| POST | `/notes/create_note` | Create a new note | Yes |
| DELETE | `/notes/{note_id}` | Delete a note by ID | Yes |

### AI

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| GET | `/ai/summarize/{note_id}` | Summarize a note using Groq LLM | Yes |

---

## Getting Started

### Prerequisites

- Python 3.12+
- A Groq API key (free tier available at [console.groq.com](https://console.groq.com))

### Local Setup

```bash
# Clone the repository
git clone https://github.com/your-username/novamind-lite.git
cd novamind-lite

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
JWT_SECRET_KEY=your_jwt_secret_key_here
GROQ_API_KEY=your_groq_api_key_here
DATABASE_URL=sqlite:///./novamind.db
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Run the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive docs are at `http://localhost:8000/docs`.

---

## Running with Docker

```bash
# Build and start the container
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

---

## Testing

```bash
pytest tests/ -v
```

Tests use an in-memory SQLite database and a fake user dependency override — no real database or authentication tokens are required.

```
tests/test_notes.py::test_get_notes_returns_empty_list   PASSED
tests/test_notes.py::test_create_note_returns_201        PASSED
tests/test_notes.py::test_get_nonexistent_note_returns_404  PASSED
```

---

## Key Design Decisions

**Dependency Injection for DB and Auth**
Both the database session and the current user are provided via FastAPI's `Depends()` system. This makes every route testable in isolation — tests simply override these dependencies with in-memory fakes.

**Centralized Error Handling**
All errors are handled through global exception handlers registered in `main.py`. Custom domain exceptions (`NoteNotFoundException`, `UserAlreadyExistsException`) keep route logic clean and decouple error formatting from business logic.

**Async AI Layer**
The Groq LLM client uses `AsyncGroq` with `await`, making the AI summarization endpoint genuinely non-blocking. The rest of the application uses synchronous SQLAlchemy, which FastAPI runs in a threadpool — the correct approach for sync I/O.

**JWT Authentication Flow**
Passwords are hashed with bcrypt and never stored in plaintext. On login, a signed JWT is issued containing the user ID as the `sub` claim. Protected routes validate this token via `get_current_user`, which is injected as a dependency — a single line locks any route.

**Background Tasks**
The registration endpoint uses FastAPI's `BackgroundTasks` to send a welcome notification after the response is returned, without blocking the client.

---

## CI Pipeline

Every push and pull request to `main` triggers the GitHub Actions workflow:

1. Checkout code
2. Set up Python 3.12
3. Install dependencies
4. Run the full test suite with injected test environment variables

---

## Environment Variable Reference

| Variable | Required | Default | Description |
|---|---|---|---|
| `JWT_SECRET_KEY` | Yes | None | Secret key for signing JWTs |
| `GROQ_API_KEY` | Yes | None | Groq API key for LLM access |
| `DATABASE_URL` | No | `sqlite:///./novamind.db` | SQLAlchemy database URL |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `30` | JWT expiry duration in minutes |

---

## License

MIT
