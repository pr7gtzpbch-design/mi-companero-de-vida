from __future__ import annotations

import json
from typing import Dict, List

from openai import OpenAI

from ..config import Settings


SYSTEM_INSTRUCTIONS = """
Eres el cerebro de un compañero personal de escritorio. Responde en español claro,
directo y cálido. Ayuda a priorizar trabajo, explica tus criterios y distingue entre
lo urgente, lo importante y lo que puede esperar. No afirmes que ejecutaste una acción
externa si la aplicación no te entregó el resultado de esa herramienta. Antes de enviar
mensajes, modificar calendarios, borrar datos o realizar acciones sensibles, pide aprobación.
""".strip()


class OpenAIService:
    def __init__(self, settings: Settings):
        if not settings.has_openai_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)

    def respond(self, message: str, tasks: List[Dict[str, object]]) -> str:
        task_context = json.dumps(tasks, ensure_ascii=False, indent=2)
        response = self.client.responses.create(
            model=self.settings.openai_model,
            reasoning={"effort": "medium"},
            instructions=SYSTEM_INSTRUCTIONS,
            input=(
                "Estas son las tareas activas del usuario:\n"
                f"{task_context}\n\n"
                f"Solicitud del usuario: {message}"
            ),
        )
        return response.output_text.strip()

