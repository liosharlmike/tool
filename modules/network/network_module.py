from __future__ import annotations

from integrations.nmap import NmapIntegration


class NetworkModule:
    def __init__(self, nmap_integration: NmapIntegration | None = None):
        self.nmap_integration = nmap_integration or NmapIntegration()

    def scan(self, target: str, profile: str = "basic", timeout: int = 300) -> dict[str, object]:
        return self.nmap_integration.scan(target, profile=profile, timeout=timeout)
