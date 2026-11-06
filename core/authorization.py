from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from core.exceptions import AuthorizationError


@dataclass
class AuthorizationContext:
    target: str
    purpose: str
    authorized: bool = False
    scope: str = "internal"
    notes: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


def require_authorization(context: AuthorizationContext) -> AuthorizationContext:
    if not context.authorized:
        raise AuthorizationError("Authorization is required before scanning or testing a target.")
    if not context.target or not context.purpose.strip():
        raise AuthorizationError("A target and assessment purpose are required.")
    if context.scope.strip() == "":
        raise AuthorizationError("Assessment scope cannot be empty.")
    return context
