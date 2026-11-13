from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    openai_configured: bool


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    description: str = Field(default="", max_length=4000)
    priority: int = Field(default=3, ge=1, le=5)
    due_at: Optional[str] = None


class Task(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    status: str
    due_at: Optional[str]
    created_at: str
    updated_at: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=12000)


class ChatResponse(BaseModel):
    reply: str
    model: str

