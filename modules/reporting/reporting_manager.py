from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from core.exceptions import ReportGenerationError


class ReportGenerator:
    def __init__(self, report_dir: str = "./reports"):
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def generate_html(self, assessment: dict[str, Any]) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        report_path = self.report_dir / f"report_{timestamp}.html"
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta charset=\"utf-8\"><title>Liosharl Assessment</title></head>
        <body>
        <h1>LIOSHARL CYBERSECURITY SUITE</h1>
        <h2>Assessment Report</h2>
        <p><strong>Target:</strong> {assessment.get('target','unknown')}</p>
        <p><strong>Scope:</strong> {assessment.get('scope','unknown')}</p>
        <p><strong>Purpose:</strong> {assessment.get('purpose','unknown')}</p>
        <p><strong>Generated:</strong> {datetime.now(timezone.utc).isoformat()}</p>
        <table>
            <tr><th>Finding</th><th>Severity</th></tr>
            {''.join(f'<tr><td>{item.get("title","unknown")}</td><td>{item.get("severity","unknown")}</td></tr>' for item in assessment.get('findings', []))}
        </table>
        </body>
        </html>
        """
        report_path.write_text(html, encoding="utf-8")
        return str(report_path)

    def generate_json(self, assessment: dict[str, Any]) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        report_path = self.report_dir / f"report_{timestamp}.json"
        report_path.write_text(json.dumps(assessment, indent=2), encoding="utf-8")
        return str(report_path)

    def generate_txt(self, assessment: dict[str, Any]) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        report_path = self.report_dir / f"report_{timestamp}.txt"
        lines = [
            "LIOSHARL CYBERSECURITY SUITE",
            "Assessment Report",
            f"Target: {assessment.get('target', 'unknown')}",
            f"Scope: {assessment.get('scope', 'unknown')}",
            f"Purpose: {assessment.get('purpose', 'unknown')}",
        ]
        for item in assessment.get("findings", []):
            lines.append(f"- {item.get('title','unknown')} [{item.get('severity','unknown')}]")
        report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(report_path)
