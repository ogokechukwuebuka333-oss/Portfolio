"""Shared fixtures for the end-to-end suite.

Run against the local copy (starts tests/serve.py on :8080 if nothing is listening):
    .venv/bin/pytest
Run against the live site:
    .venv/bin/pytest --base-url https://chukwuebukasportfolio.vercel.app
"""
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import pytest

SERVE = Path(__file__).with_name("serve.py")


def _port_open(host, port):
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex((host, port)) == 0


@pytest.fixture(scope="session", autouse=True)
def local_server(base_url):
    """Start the local preview server when testing localhost and nothing is running yet."""
    u = urlparse(base_url)
    if u.hostname not in ("localhost", "127.0.0.1") or _port_open("127.0.0.1", u.port or 80):
        yield
        return
    proc = subprocess.Popen([sys.executable, str(SERVE), str(u.port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        if _port_open("127.0.0.1", u.port):
            break
        time.sleep(0.1)
    yield
    proc.terminate()


@pytest.fixture
def browser_context_args(browser_context_args):
    # Clipboard tests need permission; reduced motion keeps map animations deterministic.
    return {**browser_context_args, "permissions": ["clipboard-read", "clipboard-write"], "reduced_motion": "reduce"}


@pytest.fixture
def problems(page):
    """Collect console errors, uncaught exceptions and failed same-site requests; fail the test if any appear."""
    found = []
    page.on("console", lambda m: m.type == "error" and found.append(f"console: {m.text}"))
    page.on("pageerror", lambda e: found.append(f"pageerror: {e}"))

    def on_response(r):
        if r.status >= 400 and urlparse(r.url).hostname == urlparse(page.url or r.url).hostname:
            found.append(f"{r.status} {r.url}")

    page.on("response", on_response)
    # requests cancelled by navigating to another page are expected, not failures
    page.on("requestfailed", lambda r: "ERR_ABORTED" not in (r.failure or "") and found.append(f"failed {r.url} ({r.failure})"))
    yield found
    assert not found, "\n".join(found)


@pytest.fixture
def home(page, problems, base_url):
    page.goto(base_url + "/")
    page.wait_for_function("document.querySelectorAll('#scene [data-id]').length > 0")
    page.evaluate("document.fonts.ready.then(() => true)")  # web fonts swapping in reflow the page
    return page


@pytest.fixture
def case(page, problems, base_url):
    page.goto(base_url + "/betalmighty")
    page.wait_for_selector("#case:not([hidden])")
    page.evaluate("document.fonts.ready.then(() => true)")
    return page


def view_box(page):
    return [float(x) for x in page.get_attribute("#scene", "viewBox").split()]
