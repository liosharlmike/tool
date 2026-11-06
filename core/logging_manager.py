from __future__ import annotations

import logging
import os
import re
from pathlib import Path

_REDACTION_PATTERNS = [
    r"(Authorization:\s*)?Bearer\s+[A-Za-z0-9._\-]+",
    r"(api[_-]?key\s*[:=]\s*)(?:['\"][^'\"]+['\"]|[^\s,;]+)",
    r"(password\s*[:=]\s*)(?:['\"][^'\"]+['\"]|[^\s,;]+)",
]


def redact_sensitive(value: str) -> str:
    redacted = value
    for pattern in _REDACTION_PATTERNS:
        redacted = re.sub(pattern, "[REDACTED]", redacted, flags=re.IGNORECASE)
    return redacted


def setup_logging(log_dir: str = "./logs", level: str = "INFO") -> logging.Logger:
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("liosharl")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    file_handler = logging.FileHandler(log_path / "liosharl.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.propagate = False
    return logger


def log_exception(logger: logging.Logger, exc: Exception, context: str = "error") -> None:
    logger.exception("%s: %s", context, redact_sensitive(str(exc)))
