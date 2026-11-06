from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from core.exceptions import ConfigurationError


@dataclass
class AppConfig:
    default_scan_profile: str = "basic"
    scan_timeout: int = 300
    report_dir: str = "./reports"
    log_level: str = "INFO"
    ai_provider: str = "ollama"
    ollama_endpoint: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.1"
    assessment_retention_days: int = 90
    tool_locations: dict[str, str] = field(default_factory=dict)
    interface_preferences: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "default_scan_profile": self.default_scan_profile,
            "scan_timeout": self.scan_timeout,
            "report_dir": self.report_dir,
            "log_level": self.log_level,
            "ai_provider": self.ai_provider,
            "ollama_endpoint": self.ollama_endpoint,
            "ollama_model": self.ollama_model,
            "assessment_retention_days": self.assessment_retention_days,
            "tool_locations": self.tool_locations,
            "interface_preferences": self.interface_preferences,
        }


def load_config(path: str | os.PathLike[str] = "./config/app_config.json") -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        return AppConfig()

    import json

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigurationError(f"Configuration file is not valid JSON: {config_path}") from exc

    defaults = AppConfig()
    merged = defaults.as_dict()
    merged.update(data)
    return AppConfig(**merged)


def save_config(config: AppConfig, path: str | os.PathLike[str] = "./config/app_config.json") -> None:
    config_path = Path(path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    import json

    config_path.write_text(json.dumps(config.as_dict(), indent=2), encoding="utf-8")
