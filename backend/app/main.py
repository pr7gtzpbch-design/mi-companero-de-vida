from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from .config import get_settings
from .database import CompanionDatabase
from .models import ChatRequest, ChatResponse, HealthResponse, Task, TaskCreate
from .services.openai_service import OpenAIService


settings = get_settings()
database = CompanionDatabase(settings.database_path)


@asynccontextmanager
async def lifespan(_: FastAPI):
    database.initialize()
    yield


app = FastAPI(
    title="Mi compañero de vida",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", openai_configured=settings.has_openai_key)


@app.get("/tasks", response_model=list[Task])
def list_tasks(include_completed: bool = False) -> list[Task]:
    return [Task(**task) for task in database.list_tasks(include_completed)]


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    task = database.create_task(
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        due_at=payload.due_at,
    )
    return Task(**task)


@app.post("/assistant/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    if not settings.has_openai_key:
        raise HTTPException(
            status_code=503,
            detail="OPENAI_API_KEY is not configured. Copy .env.example to .env.",
        )

    service = OpenAIService(settings)
    try:
        reply = service.respond(payload.message, database.list_tasks())
    except Exception as error:
        raise HTTPException(status_code=502, detail="OpenAI request failed") from error
    return ChatResponse(reply=reply, model=settings.openai_model)

