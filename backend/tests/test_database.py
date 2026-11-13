from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase

from backend.app.database import CompanionDatabase


class CompanionDatabaseTests(TestCase):
    def test_create_and_list_tasks(self) -> None:
        with TemporaryDirectory() as directory:
            database = CompanionDatabase(Path(directory) / "companion.db")
            database.initialize()

            created = database.create_task(
                title="Preparar propuesta",
                description="Revisar alcance y presupuesto",
                priority=1,
            )

            tasks = database.list_tasks()

            self.assertEqual(created["title"], "Preparar propuesta")
            self.assertEqual(tasks[0]["id"], created["id"])
            self.assertEqual(tasks[0]["priority"], 1)

