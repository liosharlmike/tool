from __future__ import annotations

from core.database import DatabaseManager


class AssessmentHistory:
    def __init__(self, db: DatabaseManager | None = None):
        self.db = db or DatabaseManager()

    def add(self, assessment_id: str, target: str, scope: str, purpose: str, authorized: bool) -> None:
        self.db.add_assessment(assessment_id, target, scope, purpose, authorized)

    def list(self) -> list[dict[str, object]]:
        return self.db.list_assessments()
