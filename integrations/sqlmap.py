from __future__ import annotations

from core.authorization import AuthorizationContext, require_authorization


class SQLMapIntegration:
    def __init__(self):
        self.enabled = False

    def authorize_and_check_scope(self, auth: AuthorizationContext, url: str, approved_scope: str) -> None:
        require_authorization(auth)
        if not url.startswith("http"):
            raise ValueError("SQLMap requires a full URL beginning with http:// or https://")
        if approved_scope not in {"internal", "lab", "authorized"}:
            raise ValueError("SQLMap requires an approved assessment scope.")
