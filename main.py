from app.exceptions import NoteNotFoundException, UserAlreadyExistsException
from app.routers.notes import router as notes_router
from app.routers.ai import router as ai_router
from app.routers.auth import router as auth_router
from app.db.session import Base, engine
# ------------------------------------------------------
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware
# ------------------------------------------------------
import time
# ------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Novamind is starting")
    Base.metadata.create_all(bind=engine)
    yield
    print("Novamind is shutting down")


app = FastAPI(title="NovaMind Lite", version="0.1.0", lifespan=lifespan)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        print(f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s")
        return response
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000', 'http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
app.add_middleware(RequestLoggingMiddleware)


app.include_router(notes_router)
app.include_router(ai_router)
app.include_router(auth_router)

@app.exception_handler(NoteNotFoundException)
async def note_not_found_handler(req: Request, exc: NoteNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"error": "Note was not found", "Note ID": exc.note_id}
    )

@app.exception_handler(UserAlreadyExistsException)
async def user_already_exists_handler(req: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content={"error": "User Already Exists", "Email": exc.email}
    )

@app.exception_handler(RequestValidationError)
async def pydantic_validation_handler(req: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Validation Failed", "details": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(req: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

@app.exception_handler(HTTPException)
async def global_exception_handler(req: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
