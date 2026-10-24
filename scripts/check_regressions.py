"""Run non-browser tests with disposable storage and no live network access."""
import os
from pathlib import Path
import socket
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]


def forbid_network(*args, **kwargs):
    raise RuntimeError("Repository regression checks forbid network connections")


def main():
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    # Do not read local .env credentials, even when invoked in a developer workspace.
    os.environ["PYTHON_DOTENV_DISABLED"] = "1"
    for name in (
        "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "RUNPOD_API_KEY",
        "RUNPOD_ENDPOINT_ID", "RUNPOD_ENDPOINT_URL", "ADMIN_TOKEN",
        "FUTUREPATH_DEMO_PASSWORD", "SESSION_SECRET",
    ):
        os.environ[name] = ""
    os.environ["SIGNALS_REFRESH_HOURS"] = "0"
    os.environ["FUTUREPATH_PUBLIC_DEMO"] = "0"
    # Tests use in-process clients and provider mocks. Synthetic test keys must
    # never turn an accidentally unstubbed request into a real provider call.
    socket.socket.connect = forbid_network
    socket.socket.connect_ex = forbid_network
    with TemporaryDirectory(prefix="futurepath-regressions-") as directory:
        os.environ["FUTUREPATH_DB"] = str(Path(directory) / "synthetic.sqlite3")
        # Freeze storage before collection: legacy tests assign fixed /tmp DB
        # paths at module scope. They must not redirect this run's actual storage.
        from backend import storage

        assert storage.DB == Path(os.environ["FUTUREPATH_DB"])
        import pytest

        return pytest.main(["tests", "--ignore=tests/browser", "-q", "--tb=short"])


if __name__ == "__main__":
    sys.exit(main())
