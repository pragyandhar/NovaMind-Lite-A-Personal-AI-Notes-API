from app.routers.notes import router as notes_router
from app.routers.ai import router as ai_router
from app.routers.auth import router as auth_router
from app.db.session import Base, engine
# ------------------------------------------------------
from fastapi import FastAPI
from contextlib import asynccontextmanager
# ------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Novamind is starting")
    Base.metadata.create_all(bind=engine)
    yield
    print("Novamind is shutting down")


app = FastAPI(title="NovaMind Lite", version="0.1.0", lifespan=lifespan)

app.include_router(notes_router)
app.include_router(ai_router)
app.include_router(auth_router)

