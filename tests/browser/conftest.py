"""Opt-in real Chromium tests against a fresh FastAPI process per test."""
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

import pytest

ROOT = Path(__file__).resolve().parents[2]


def pytest_addoption(parser):
    parser.addoption("--browser", action="store_true", help="Run isolated Chromium journeys")


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--browser"):
        for item in items:
            if Path(__file__).parent in Path(item.path).parents:
                item.add_marker(pytest.mark.skip(reason="Run with --browser"))


@pytest.fixture
def server(tmp_path, request):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    # Explicit allowlist: never pass deployment/provider credentials to the child.
    env = {k: os.environ[k] for k in (
        "PATH", "HOME", "PYTHONPATH", "PYTHONHOME", "LD_LIBRARY_PATH"
    ) if k in os.environ}
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT), *sys.path])
    mode = getattr(request, "param", "0")
    with (tmp_path / "server.log").open("w+") as log:
        process = subprocess.Popen(
            [sys.executable, str(Path(__file__).with_name("server.py")),
             str(tmp_path / "synthetic.sqlite3"), str(port), mode],
            cwd=ROOT, env=env, stdout=log, stderr=log,
        )
        url = f"http://127.0.0.1:{port}"
        try:
            for _ in range(100):
                if process.poll() is not None:
                    log.seek(0)
                    pytest.fail(log.read())
                try:
                    urlopen(url + "/start", timeout=.2).close()
                    break
                except HTTPError as exc:
                    if exc.code in (401, 503):
                        break
                    raise
                except (URLError, TimeoutError):
                    time.sleep(.1)
            else:
                pytest.fail("Disposable server did not become ready")
            yield url
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


@pytest.fixture
def browser():
    from playwright.sync_api import sync_playwright
    executable = os.getenv("PLAYWRIGHT_CHROMIUM_EXECUTABLE") or shutil.which("chromium")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            **({"executable_path": executable} if executable else {}),
            args=["--no-sandbox"],
        )
        yield browser
        browser.close()


@pytest.fixture
def page(browser, server):
    context = browser.new_context(base_url=server)
    # The unchanged release loads its pinned React/Babel runtime from unpkg.
    scripts = {
        "https://unpkg.com/react@18.3.1/umd/react.production.min.js",
        "https://unpkg.com/react-dom@18.3.1/umd/react-dom.production.min.js",
        "https://unpkg.com/@babel/standalone@7.29.0/babel.min.js",
    }
    context.route("**/*", lambda route: route.continue_()
                  if route.request.url.startswith(server + "/") or route.request.url in scripts
                  else route.abort())
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    yield page
    context.close()
    assert not errors, f"Uncaught browser errors: {errors}"
