from __future__ import annotations

from core.application import LiosharlApplication
from core.process_manager import ProcessManager


class SystemIntelligence:
    def __init__(self, application: LiosharlApplication | None = None, process_manager: ProcessManager | None = None):
        self.application = application or LiosharlApplication()
        self.process_manager = process_manager or ProcessManager()

    def get_status(self) -> dict[str, object]:
        snapshot = self.application.get_environment_snapshot()
        tools = {
            "nmap": self.process_manager.is_available("nmap"),
            "whatweb": self.process_manager.is_available("whatweb"),
            "nikto": self.process_manager.is_available("nikto"),
            "sqlmap": self.process_manager.is_available("sqlmap"),
            "gobuster": self.process_manager.is_available("gobuster"),
            "ollama": self.process_manager.is_available("ollama"),
        }
        return {
            "environment": snapshot,
            "tools": tools,
        }
