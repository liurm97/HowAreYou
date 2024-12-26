from typing import Any
from django.core.management.base import BaseCommand, CommandError
from ...scripts.seed_db_script import (
    seed_resources_db,
    seed_students_and_responses_db,
)


class Command(BaseCommand):
    help = "seed resources, students and responses database"

    def handle(self, *args: Any, **options: Any) -> str | None:
        seed_students_and_responses_db()
        seed_resources_db()
