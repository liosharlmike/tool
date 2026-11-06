from __future__ import annotations

from core.exceptions import ToolNotFoundError
from core.process_manager import ProcessManager


class WhatWebIntegration:
    def __init__(self, process_manager: ProcessManager | None = None):
        self.process_manager = process_manager or ProcessManager()

    def is_available(self) -> bool:
        return self.process_manager.is_available("whatweb")

    def inspect(self, target: str, timeout: int = 90) -> dict[str, object]:
        if not self.is_available():
            raise ToolNotFoundError("whatweb is not installed or not on PATH.")
        result = self.process_manager.execute(["whatweb", "--log-verbose=/dev/null", target], timeout=timeout, check=False)
        return {"target": target, "stdout": result.stdout.strip(), "stderr": result.stderr.strip(), "returncode": result.returncode}
