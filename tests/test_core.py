from __future__ import annotations

import json

import pytest

from core.authorization import AuthorizationContext, require_authorization
from core.configuration import AppConfig, load_config
from core.database import DatabaseManager
from core.logging_manager import redact_sensitive
from core.validation import validate_target


def test_validate_target_accepts_ipv4() -> None:
    target = validate_target("192.168.1.10")
    assert target.kind == "ipv4"
    assert target.normalized == "192.168.1.10"


def test_validate_target_accepts_cidr() -> None:
    target = validate_target("192.168.1.0/24")
    assert target.kind == "cidr"
    assert target.normalized == "192.168.1.0/24"


def test_validate_target_rejects_invalid_input() -> None:
    with pytest.raises(ValueError):
        validate_target("not a valid target")


def test_authorization_blocks_missing_approval() -> None:
    auth = AuthorizationContext(target="192.168.1.10", purpose="assessment", authorized=False, scope="internal")
    with pytest.raises(Exception):
        require_authorization(auth)


def test_load_config_reads_defaults(tmp_path) -> None:
    config_path = tmp_path / "app_config.json"
    config_path.write_text(json.dumps({"default_scan_profile": "advanced"}), encoding="utf-8")
    config = load_config(config_path)
    assert config.default_scan_profile == "advanced"
    assert config.log_level == "INFO"


def test_database_manager_round_trip(tmp_path) -> None:
    db = DatabaseManager(str(tmp_path / "test.db"))
    db.add_assessment("A-001", "192.168.1.10", "lab", "test", True)
    db.add_host("A-001", "192.168.1.10", "up", "None", "Linux")
    db.add_service("A-001", "192.168.1.10", 80, "tcp", "http", "nginx")
    entries = db.list_assessments()
    assert len(entries) == 1
    assert entries[0]["target"] == "192.168.1.10"


def test_redact_sensitive_patterns() -> None:
    message = "Authorization: Bearer abc123 and password=secret123"
    redacted = redact_sensitive(message)
    assert "abc123" not in redacted
    assert "secret123" not in redacted
    assert "[REDACTED]" in redacted
