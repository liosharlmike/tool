from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import Any

from core.exceptions import TargetValidationError, ToolNotFoundError
from core.process_manager import ProcessManager
from core.validation import validate_target


class NmapIntegration:
    def __init__(self, process_manager: ProcessManager | None = None):
        self.process_manager = process_manager or ProcessManager()

    def is_available(self) -> bool:
        return self.process_manager.is_available("nmap")

    def scan(self, target: str, profile: str = "basic", timeout: int = 300) -> dict[str, Any]:
        validated = validate_target(target)
        if not self.is_available():
            raise ToolNotFoundError("nmap is not installed or not on PATH.")

        profile_map = {
            "basic": ["-sn", "--top-ports", "50"],
            "service": ["-sV", "--top-ports", "200"],
            "advanced": ["-sV", "-O", "--top-ports", "400"],
        }
        args = ["nmap", "-oX", "-"] + profile_map.get(profile, profile_map["basic"]) + [validated.normalized]
        result = self.process_manager.execute(args, timeout=timeout)
        return self.parse_xml(result.stdout)

    def parse_xml(self, xml_text: str) -> dict[str, Any]:
        if not xml_text or "<nmaprun" not in xml_text:
            raise TargetValidationError("Nmap XML output was empty or malformed.")

        root = ET.fromstring(xml_text)
        hosts: list[dict[str, Any]] = []
        for host in root.findall("host"):
            address = host.find("address")
            status = host.find("status")
            host_ip = address.attrib.get("addr") if address is not None else "unknown"
            host_state = status.attrib.get("state", "unknown") if status is not None else "unknown"
            ports = []
            for port in host.findall("./ports/port"):
                port_id = int(port.attrib.get("portid", "0"))
                protocol = port.attrib.get("protocol", "tcp")
                port_state = port.find("state")
                port_service = port.find("service")
                ports.append(
                    {
                        "port": port_id,
                        "protocol": protocol,
                        "state": port_state.attrib.get("state") if port_state is not None else "unknown",
                        "service": port_service.attrib.get("name") if port_service is not None else "unknown",
                        "product": port_service.attrib.get("product") if port_service is not None else "",
                        "version": port_service.attrib.get("version") if port_service is not None else "",
                        "extradata": port_service.attrib.get("extrainfo") if port_service is not None else "",
                    }
                )
            hosts.append({"ip": host_ip, "state": host_state, "ports": ports})

        return {"hosts": hosts, "summary": {"count": len(hosts)}}
