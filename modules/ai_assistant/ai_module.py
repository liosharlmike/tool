from __future__ import annotations

from integrations.ollama import OllamaClient


class AIAssistant:
    def __init__(self, client: OllamaClient | None = None):
        self.client = client or OllamaClient()

    def available(self) -> bool:
        return self.client.is_available()

    def explain(self, content: str) -> str:
        if not self.available():
            return "AI explanation is unavailable because Ollama is not reachable on the configured endpoint."
        return self.client.generate(f"Explain the following cybersecurity information succinctly and clearly.\n\n{content}")
