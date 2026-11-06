from __future__ import annotations

from core.process_manager import ProcessManager


class GobusterIntegration:
    def __init__(self, process_manager: ProcessManager | None = None):
        self.process_manager = process_manager or ProcessManager()

    def is_available(self) -> bool:
        return self.process_manager.is_available("gobuster")

    def run(self, target: str, wordlist: str, timeout: int = 60) -> dict[str, object]:
        if not self.is_available():
            return {"status": "unavailable", "target": target, "message": "Gobuster is not installed."}
        result = self.process_manager.execute(["gobuster", "dir", "-u", target, "-w", wordlist], timeout=timeout, check=False)
        return {"status": "completed" if result.returncode in (0, 1) else "error", "stdout": result.stdout, "stderr": result.stderr}
