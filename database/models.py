from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AssessmentRecord:
    assessment_id: str
    target: str
    scope: str
    purpose: str
    authorized: bool = False
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    report_path: str | None = None
    status: str = "draft"
