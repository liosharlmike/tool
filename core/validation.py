from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass
from typing import Literal

from core.exceptions import TargetValidationError

HOSTNAME_RE = re.compile(r"^(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)*[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")


@dataclass
class ValidatedTarget:
    raw: str
    normalized: str
    kind: Literal["ipv4", "ipv6", "cidr", "hostname", "localhost"]
    is_private: bool


def _is_localhost(value: str) -> bool:
    return value.lower() in {"localhost", "127.0.0.1", "::1"}


def validate_target(target: str) -> ValidatedTarget:
    if not isinstance(target, str):
        raise TargetValidationError("Target must be a non-empty string.")

    candidate = target.strip()
    if not candidate:
        raise TargetValidationError("Target cannot be empty.")

    if _is_localhost(candidate):
        return ValidatedTarget(candidate, "localhost", "localhost", True)

    try:
        ip = ipaddress.ip_address(candidate)
        kind = "ipv4" if ip.version == 4 else "ipv6"
        return ValidatedTarget(candidate, str(ip), kind, ip.is_private or ip.is_loopback)
    except ValueError:
        pass

    try:
        network = ipaddress.ip_network(candidate, strict=False)
        if network.version not in (4, 6):
            raise TargetValidationError("Unsupported IP network type.")
        return ValidatedTarget(candidate, str(network), "cidr", network.is_private)
    except ValueError:
        pass

    if HOSTNAME_RE.match(candidate):
        return ValidatedTarget(candidate, candidate.lower(), "hostname", not candidate.endswith("."))

    raise TargetValidationError(f"Unsupported target '{target}'. Use IPv4, IPv6, CIDR, or an authorized hostname.")
