from __future__ import annotations

from core.application import LiosharlApplication


class DashboardModule:
    def __init__(self, application: LiosharlApplication):
        self.application = application

    def get_overview(self) -> dict[str, object]:
        snapshot = self.application.get_environment_snapshot()
        return {
            "product": "LIOSHARL CYBERSECURITY SUITE",
            "version": "2.0.0",
            "distro": snapshot.distro,
            "kernel": snapshot.kernel,
            "python_version": snapshot.python_version,
            "privilege_level": snapshot.privilege_level,
            "memory_gb": snapshot.memory_gb,
            "storage_gb": snapshot.storage_gb,
            "network_interfaces": snapshot.network_interfaces,
            "connectivity": snapshot.connectivity,
        }
