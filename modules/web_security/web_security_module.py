from __future__ import annotations

from urllib.parse import urlparse

import requests


class WebSecurityModule:
    @staticmethod
    def passive_headers_check(url: str) -> dict[str, object]:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("URL must include a scheme and a host.")

        response = requests.get(url, timeout=10, allow_redirects=True)
        headers = response.headers
        observation = {
            "url": url,
            "status_code": response.status_code,
            "http_security_headers": {
                "strict_transport_security": headers.get("Strict-Transport-Security"),
                "x_frame_options": headers.get("X-Frame-Options"),
                "content_security_policy": headers.get("Content-Security-Policy"),
                "x_content_type_options": headers.get("X-Content-Type-Options"),
            },
            "cookie_security": {
                "set_cookie": headers.get("Set-Cookie"),
            },
        }
        return observation
