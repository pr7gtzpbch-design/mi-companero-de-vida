from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterator, List, Optional


class CompanionDatabase:
    def __init__(self, path: Path):
        self.path = path

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(str(self.path))
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    priority INTEGER NOT NULL DEFAULT 3 CHECK(priority BETWEEN 1 AND 5),
                    status TEXT NOT NULL DEFAULT 'pending'
                        CHECK(status IN ('pending', 'in_progress', 'completed', 'cancelled')),
                    due_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_tasks_status_due_at
                    ON tasks(status, due_at);
                """
            )

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: int = 3,
        due_at: Optional[str] = None,
    ) -> Dict[str, object]:
        now = datetime.now(timezone.utc).isoformat()
        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tasks (title, description, priority, due_at, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (title.strip(), description.strip(), priority, due_at, now, now),
            )
            task_id = int(cursor.lastrowid)
        task = self.get_task(task_id)
        if task is None:
            raise RuntimeError("Task was created but could not be loaded")
        return task

    def get_task(self, task_id: int) -> Optional[Dict[str, object]]:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,)
            ).fetchone()
        return dict(row) if row else None

    def list_tasks(self, include_completed: bool = False) -> List[Dict[str, object]]:
        query = "SELECT * FROM tasks"
        parameters = ()
        if not include_completed:
            query += " WHERE status NOT IN (?, ?)"
            parameters = ("completed", "cancelled")
        query += " ORDER BY priority ASC, due_at IS NULL, due_at ASC, created_at ASC"
        with self.connect() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [dict(row) for row in rows]

