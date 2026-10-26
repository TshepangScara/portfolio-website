"""
Shared fixtures for the portfolio site test suite.

- Serves the repo root over a local HTTP server for the whole session,
  so tests run against the real files with no build step.
- Stubs all third-party requests (Google Fonts, LinkedIn, etc.) so the
  suite is fast, deterministic and works offline.
"""
import functools
import http.server
import re
import socketserver
import threading
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    "index.html",
    "experience.html",
    "skills.html",
    "certifications.html",
    "projects.html",
    "cv.html",
]

THIRD_PARTY = re.compile(r"^https?://(?!127\.0\.0\.1|localhost)")


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):  # keep pytest output clean
        pass


@pytest.fixture(scope="session")
def base_url():
    """Start a static server on a free port and return its URL."""
    handler = functools.partial(_QuietHandler, directory=str(ROOT))
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as httpd:
        port = httpd.server_address[1]
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        yield f"http://127.0.0.1:{port}/"
        httpd.shutdown()


@pytest.fixture
def context(context):
    """Stub third-party requests with empty 200 responses."""
    context.route(THIRD_PARTY, lambda route: route.fulfill(status=200, body=""))
    return context


@pytest.fixture
def console_errors(page):
    """Collect console errors and uncaught exceptions for the current page."""
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    return errors
