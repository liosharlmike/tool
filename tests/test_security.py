from __future__ import annotations

import pytest

from core.process_manager import ProcessManager
from core.validation import validate_target


def test_invalid_target_rejected() -> None:
    with pytest.raises(Exception):
        validate_target("../../etc/passwd")


def test_process_manager_executes_argument_list_without_shell() -> None:
    manager = ProcessManager()
    result = manager.execute(["python", "-c", "print('hello')"], timeout=30)
    assert result.returncode == 0
    assert "hello" in result.stdout
