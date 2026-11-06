from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

from core.exceptions import ProcessExecutionError, ToolNotFoundError


@dataclass
class CommandResult:
    command: list[str]
    returncode: int
    stdout: str
    stderr: str
    executed: bool = True


class ProcessManager:
    """Safe, centralized process execution wrapper for external tools."""

    def __init__(self, logger: Any | None = None):
        self.logger = logger

    def is_available(self, executable: str) -> bool:
        return shutil.which(executable) is not None

    def require_tool(self, executable: str) -> str:
        resolved = shutil.which(executable)
        if not resolved:
            raise ToolNotFoundError(f"Required tool '{executable}' is not installed or not on PATH.")
        return resolved

    def execute(
        self,
        command: Sequence[str],
        *,
        timeout: int = 120,
        cwd: str | os.PathLike[str] | None = None,
        env: dict[str, str] | None = None,
        check: bool = True,
    ) -> CommandResult:
        if not command:
            raise ProcessExecutionError("No command provided for execution.")

        args = [str(part).strip() for part in command if str(part).strip()]
        if not args:
            raise ProcessExecutionError("Command arguments are empty after sanitization.")

        if self.logger:
            self.logger.info("Executing command: %s", args)

        try:
            completed = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(cwd) if cwd else None,
                env=env,
                shell=False,
                check=False,
            )
        except FileNotFoundError as exc:
            raise ToolNotFoundError(f"Command not found: {args[0]}") from exc
        except subprocess.TimeoutExpired as exc:
            raise ProcessExecutionError(f"Command timed out after {timeout} seconds: {' '.join(args)}") from exc

        result = CommandResult(command=args, returncode=completed.returncode, stdout=completed.stdout, stderr=completed.stderr)
        if check and completed.returncode != 0:
            raise ProcessExecutionError(f"Command failed with exit code {completed.returncode}: {' '.join(args)}")
        return result
