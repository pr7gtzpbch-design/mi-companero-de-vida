from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    openai_model: str
    database_path: Path

    @property
    def has_openai_key(self) -> bool:
        return bool(self.openai_api_key.strip())


def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-6-astra"),
        database_path=Path(os.getenv("COMPANION_DB_PATH", "data/companion.db")),
    )

