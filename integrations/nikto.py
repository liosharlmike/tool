from __future__ import annotations

from core.process_manager import ProcessManager


class NiktoIntegration:
    def __init__(self, process_manager: ProcessManager | None = None):
        self.process_manager = process_manager or ProcessManager()

    def is_available(self) -> bool:
        return self.process_manager.is_available("nikto")

    def assess(self, target: str, timeout: int = 90) -> dict[str, object]:
        if not self.is_available():
            return {"status": "unavailable", "target": target, "message": "Nikto is not installed."}
        result = self.process_manager.execute(["nikto", "-h", target], timeout=timeout, check=False)
        return {"status": "completed" if result.returncode in (0, 1) else "error", "target": target, "stdout": result.stdout, "stderr": result.stderr}
