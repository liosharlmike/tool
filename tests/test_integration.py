from __future__ import annotations

from pathlib import Path

import pytest

from integrations.nmap import NmapIntegration
from modules.ai_assistant.ai_module import AIAssistant
from modules.web_security.web_security_module import WebSecurityModule


def test_nmap_parser_handles_fixture() -> None:
    xml_path = Path(__file__).parent / "fixtures" / "nmap_sample.xml"
    xml_text = xml_path.read_text(encoding="utf-8")
    parsed = NmapIntegration().parse_xml(xml_text)
    assert parsed["summary"]["count"] == 2
    assert parsed["hosts"][0]["ports"][0]["service"] == "ssh"


def test_ai_assistant_reports_unavailable_when_client_missing(monkeypatch) -> None:
    class FakeClient:
        def is_available(self):
            return False

        def generate(self, prompt: str):
            return "Should not be called"

    assistant = AIAssistant(FakeClient())
    message = assistant.explain("This is a sample explanation request.")
    assert "unavailable" in message.lower()


def test_web_security_module_handles_mocked_headers(monkeypatch) -> None:
    class FakeResponse:
        status_code = 200
        headers = {"Strict-Transport-Security": "max-age=31536000", "Set-Cookie": "session=abc123"}

    def fake_get(url, timeout, allow_redirects=True):
        assert url == "https://example.com"
        return FakeResponse()

    monkeypatch.setattr("modules.web_security.web_security_module.requests.get", fake_get)
    result = WebSecurityModule.passive_headers_check("https://example.com")
    assert result["status_code"] == 200
    assert result["http_security_headers"]["strict_transport_security"] == "max-age=31536000"
