#!/usr/bin/env python3
"""
OAuth proxy for Sveltia CMS / Decap CMS GitHub backend.

Runs alongside zensical serve to handle the GitHub OAuth
redirect during CMS authentication.  Overrides the entire
OAuth flow using a local server that exchanges an authorization
code for an access token via the GitHub API.
"""
from __future__ import annotations

import http.server
import json
import logging
import os
import socketserver
import sys
import urllib.error
import urllib.parse
import urllib.request

PORT = 4567
CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.environ.get("GITHUB_CLIENT_SECRET")

logger = logging.getLogger("oauth-proxy")


class Handler(http.server.BaseHTTPRequestHandler):
    """Handle GitHub OAuth redirects for Sveltia CMS."""

    # Silence the default per-request access log line.
    def log_message(self, _format: str, *args: object) -> None:  # type: ignore[override]
        pass

    def do_GET(self) -> None:
        """Handle GET requests -- only /auth is recognised."""
        if not self.path.startswith("/auth"):
            self._respond(404, b"Not found")
            return

        self._exchange_code()

    def _exchange_code(self) -> None:
        """Exchange authorisation code for a token via the GitHub API."""
        query = urllib.parse.parse_qs(
            self.path.split("?")[1],
        ) if "?" in self.path else {}

        code: str = query.get("code", [""])[0]
        if not code:
            logger.warning("No authorisation code in request: %s", self.path)
            self._respond(400, b"Missing code parameter")
            return

        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
        }

        req = urllib.request.Request(
            "https://github.com/login/oauth/access_token",
            data=urllib.parse.urlencode(data).encode(),
            headers={
                "Accept": "application/json",
                "User-Agent": "codesigils-oauth-proxy/1.0",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read()
        except urllib.error.HTTPError as exc:
            logger.error("GitHub OAuth API HTTP error: %s %s", exc.code, exc.reason)
            self._respond(exc.code, b"GitHub API error")
            return
        except urllib.error.URLError as exc:
            logger.error("GitHub OAuth API connection error: %s", exc.reason)
            self._respond(502, b"Upstream connection error")
            return

        try:
            token_data = json.loads(body)
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON from GitHub: %s", exc)
            self._respond(502, b"Invalid response from GitHub")
            return

        token: str = token_data.get("access_token", "")
        if not token:
            logger.error("No access_token in GitHub response: %s", token_data)
            self._respond(502, b"No access token returned")
            return

        # Redirect back to the CMS admin with the token in the URL fragment.
        # The fragment (#) is consumed by the browser's JavaScript and never
        # sent to the server, so this is safe for the local-proxy use case.
        self.send_response(302)
        self.send_header(
            "Location",
            f"http://localhost:8000/admin/#access_token={token}",
        )
        self.end_headers()

    def _respond(self, status: int, body: bytes) -> None:
        """Send a plain-text response."""
        self.send_response(status)
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(name)s: %(message)s",
    )

    missing = []
    if not CLIENT_ID:
        missing.append("GITHUB_CLIENT_ID")
    if not CLIENT_SECRET:
        missing.append("GITHUB_CLIENT_SECRET")
    if missing:
        logger.error(
            "Set the following environment variable(s): %s",
            ", ".join(missing),
        )
        sys.exit(1)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        logger.info("OAuth proxy running on http://localhost:%d", PORT)
        logger.info("Callback URL:  http://localhost:%d/auth", PORT)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down")
            httpd.shutdown()


if __name__ == "__main__":
    main()
