from __future__ import annotations

from typing import Any

import requests


class NVDIntegration:
    def __init__(self, base_url: str = "https://services.nvd.nist.gov/rest/json/cves/2.0"):
        self.base_url = base_url

    def get_cves(self, product: str, version: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
        query = product.strip()
        if version:
            query = f"{product} {version}"

        try:
            response = requests.get(
                self.base_url,
                params={"keywordSearch": query, "resultsPerPage": limit},
                timeout=12,
            )
            response.raise_for_status()
        except requests.RequestException:
            return []

        payload = response.json()
        results = payload.get("vulnerabilities", [])
        output = []
        for item in results[:limit]:
            cve = item.get("cve", {})
            output.append(
                {
                    "id": cve.get("id", "unknown"),
                    "description": (cve.get("descriptions") or [{}])[0].get("value", "No description supplied."),
                    "severity": cve.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseSeverity", "Informational"),
                    "score": cve.get("metrics", {}).get("cvssMetricV31", [{}])[0].get("cvssData", {}).get("baseScore", 0),
                    "references": [ref.get("url", "") for ref in cve.get("references", [])],
                }
            )
        return output
