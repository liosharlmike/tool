from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from core.exceptions import DatabaseError


class DatabaseManager:
    def __init__(self, db_path: str = "./database/liosharl.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id TEXT UNIQUE,
                    target TEXT NOT NULL,
                    scope TEXT,
                    purpose TEXT,
                    authorized INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    report_path TEXT,
                    status TEXT DEFAULT 'draft'
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS hosts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id TEXT,
                    host TEXT,
                    state TEXT,
                    vendor TEXT,
                    os TEXT,
                    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS services (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id TEXT,
                    host TEXT,
                    port INTEGER,
                    protocol TEXT,
                    service TEXT,
                    version TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS findings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id TEXT,
                    title TEXT,
                    severity TEXT,
                    evidence TEXT,
                    source TEXT,
                    confidence TEXT
                )
                """
            )

    def add_assessment(self, assessment_id: str, target: str, scope: str, purpose: str, authorized: bool) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO assessments (assessment_id, target, scope, purpose, authorized) VALUES (?, ?, ?, ?, ?)",
                (assessment_id, target, scope, purpose, int(authorized)),
            )

    def add_host(self, assessment_id: str, host: str, state: str = "up", vendor: str | None = None, os_name: str | None = None) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO hosts (assessment_id, host, state, vendor, os) VALUES (?, ?, ?, ?, ?)",
                (assessment_id, host, state, vendor, os_name),
            )

    def add_service(self, assessment_id: str, host: str, port: int, protocol: str, service: str, version: str | None = None) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO services (assessment_id, host, port, protocol, service, version) VALUES (?, ?, ?, ?, ?, ?)",
                (assessment_id, host, port, protocol, service, version),
            )

    def add_finding(self, assessment_id: str, title: str, severity: str, evidence: str, source: str, confidence: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO findings (assessment_id, title, severity, evidence, source, confidence) VALUES (?, ?, ?, ?, ?, ?)",
                (assessment_id, title, severity, evidence, source, confidence),
            )

    def list_assessments(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT assessment_id, target, scope, purpose, authorized, created_at, report_path, status FROM assessments ORDER BY created_at DESC"
            ).fetchall()
            return [dict(row) for row in rows]

    def backup(self, destination: str | Path) -> Path:
        dest = Path(destination)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            raise DatabaseError(f"Database not found at {self.db_path}")
        backup_path = dest / f"liosharl_backup_{self.db_path.name}"
        with self._connect() as conn:
            data = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            backup_path.write_bytes(self.db_path.read_bytes())
        return backup_path

    def update_report_path(self, assessment_id: str, report_path: str) -> None:
        with self._connect() as conn:
            conn.execute("UPDATE assessments SET report_path = ? WHERE assessment_id = ?", (report_path, assessment_id))

    def delete_assessment(self, assessment_id: str) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM findings WHERE assessment_id = ?", (assessment_id,))
            conn.execute("DELETE FROM services WHERE assessment_id = ?", (assessment_id,))
            conn.execute("DELETE FROM hosts WHERE assessment_id = ?", (assessment_id,))
            conn.execute("DELETE FROM assessments WHERE assessment_id = ?", (assessment_id,))
