from __future__ import annotations

from typing import Any

import requests


class OllamaClient:
    def __init__(self, endpoint: str = "http://127.0.0.1:11434", model: str = "llama3.1"):
        self.endpoint = endpoint.rstrip("/")
        self.model = model

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=10)
            response.raise_for_status()
        except requests.RequestException:
            return []

        payload = response.json()
        models = payload.get("models", [])
        return [model.get("name", "") for model in models if model.get("name")]

    def generate(self, prompt: str, *, timeout: int = 30) -> str:
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        response = requests.post(f"{self.endpoint}/api/generate", json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "No response received.")
