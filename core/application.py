from __future__ import annotations

import os
import platform
import shutil
import socket
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class EnvironmentSnapshot:
    distro: str
    version: str
    kernel: str
    python_version: str
    cpu_architecture: str
    username: str
    privilege_level: str
    memory_gb: float
    storage_gb: float
    network_interfaces: list[str]
    connectivity: bool


class LiosharlApplication:
    def __init__(self, project_root: str | os.PathLike[str] | None = None):
        self.project_root = Path(project_root or Path(__file__).resolve().parents[1])

    def get_environment_snapshot(self) -> EnvironmentSnapshot:
        distro = platform.system() or "Linux"
        version = platform.release() or "unknown"
        kernel = platform.version() or "unknown"
        cpu = platform.machine() or "unknown"
        username = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"
        privilege = "root" if os.geteuid() == 0 else "standard-user"
        memory = self._memory_gb()
        storage = self._storage_gb()
        interfaces = self._network_interfaces()
        connectivity = self._has_network_connection()

        return EnvironmentSnapshot(
            distro=distro,
            version=version,
            kernel=kernel,
            python_version=sys.version.split()[0],
            cpu_architecture=cpu,
            username=username,
            privilege_level=privilege,
            memory_gb=memory,
            storage_gb=storage,
            network_interfaces=interfaces,
            connectivity=connectivity,
        )

    def _memory_gb(self) -> float:
        try:
            with open("/proc/meminfo", "r", encoding="utf-8") as handle:
                for line in handle:
                    if line.startswith("MemTotal:"):
                        total_kb = int(line.split()[1])
                        return round(total_kb / (1024 * 1024), 2)
        except OSError:
            return 0.0
        return 0.0

    def _storage_gb(self) -> float:
        try:
            stat = shutil.disk_usage("/")
            return round(stat.total / (1024 ** 3), 2)
        except OSError:
            return 0.0

    def _network_interfaces(self) -> list[str]:
        try:
            import psutil  # type: ignore

            return list(psutil.net_if_addrs().keys())
        except Exception:
            return ["lo"]

    def _has_network_connection(self) -> bool:
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False
