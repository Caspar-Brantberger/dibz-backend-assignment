from __future__ import annotations

import html
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

BASE_DIR = Path(__file__).resolve().parent
LOGIN_HTML = (BASE_DIR / "login.html").read_text(encoding="utf-8")
ACCOUNT_HTML = (BASE_DIR / "account.html").read_text(encoding="utf-8")
VALID_USERNAME = "maxim@example.com"
VALID_PASSWORD = "test123"
SESSION_VALUE = "ok"


class MockHandler(BaseHTTPRequestHandler):
    def _send_html(self, content: str, status: int = 200, extra_headers: list[tuple[str, str]] | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        if extra_headers:
            for key, value in extra_headers:
                self.send_header(key, value)
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _is_logged_in(self) -> bool:
        cookie_header = self.headers.get("Cookie", "")
        cookie = SimpleCookie()
        cookie.load(cookie_header)
        return cookie.get("session") is not None and cookie["session"].value == SESSION_VALUE

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/login"):
            self._send_html(LOGIN_HTML)
            return

        if self.path == "/account":
            if not self._is_logged_in():
                self.send_response(HTTPStatus.FOUND)
                self.send_header("Location", "/login")
                self.end_headers()
                return
            self._send_html(ACCOUNT_HTML)
            return

        if self.path == "/api/ping":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
            return

        self._send_html("<h1>Not Found</h1>", status=404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/login":
            self._send_html("<h1>Not Found</h1>", status=404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)
        username = data.get("username", [""])[0]
        password = data.get("password", [""])[0]

        if username == VALID_USERNAME and password == VALID_PASSWORD:
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Set-Cookie", f"session={SESSION_VALUE}; Path=/")
            self.send_header("Location", "/account")
            self.end_headers()
            return

        escaped = html.escape(username)
        error_html = LOGIN_HTML.replace(
            "</form>",
            f"<p style='color:#b91c1c;'>Login failed for {escaped or 'unknown user'}.</p></form>",
        )
        self._send_html(error_html, status=401)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), MockHandler)
    print("Mock platform running at http://127.0.0.1:8000")
    server.serve_forever()
