import io

from rich.console import Console

from trending_repos.domain.models import Repository
from trending_repos.errors import APIError, NetworkError, RateLimitError
from trending_repos.infrastructure.cli.session import Session


class FakeGitHubClient:
    def __init__(self, repos=None, error=None):
        self.repos = repos if repos is not None else []
        self.error = error
        self.last_query = None

    def search_trending(
        self, cutoff_date: str, limit: int, language: str | None = None
    ):
        self.last_query = (cutoff_date, limit, language)
        if self.error:
            raise self.error
        return self.repos


def test_session_success():
    stdout_io = io.StringIO()
    stderr_io = io.StringIO()
    stdout_console = Console(file=stdout_io, color_system=None, width=120)
    stderr_console = Console(file=stderr_io, color_system=None, width=120)

    client = FakeGitHubClient(
        repos=[
            Repository(
                name="sample/repo",
                description="Sample desc",
                stars=123,
                language="Python",
                url="https://github.com/sample/repo",
            )
        ]
    )

    session = Session(
        client=client,
        stdout_console=stdout_console,
        stderr_console=stderr_console,
    )
    code = session.run(["--duration", "month", "--limit", "5", "--language", "python"])

    assert code == 0
    assert "sample/repo" in stdout_io.getvalue()
    assert stderr_io.getvalue() == ""
    assert client.last_query[1] == 5
    assert client.last_query[2] == "python"


def test_session_usage_error():
    stderr_io = io.StringIO()
    stderr_console = Console(file=stderr_io, color_system=None, width=120)

    session = Session(stderr_console=stderr_console)
    code = session.run(["--limit", "-1"])

    assert code == 1
    assert "Error:" in stderr_io.getvalue()


def test_session_rate_limit_error():
    stderr_io = io.StringIO()
    stderr_console = Console(file=stderr_io, color_system=None, width=120)
    client = FakeGitHubClient(error=RateLimitError("API rate limit exceeded"))

    session = Session(client=client, stderr_console=stderr_console)
    code = session.run([])

    assert code == 2
    assert "rate limit exceeded" in stderr_io.getvalue()
    assert "GITHUB_TOKEN" in stderr_io.getvalue()


def test_session_network_error():
    stderr_io = io.StringIO()
    stderr_console = Console(file=stderr_io, color_system=None, width=120)
    client = FakeGitHubClient(error=NetworkError("Connection timed out"))

    session = Session(client=client, stderr_console=stderr_console)
    code = session.run([])

    assert code == 3
    assert "Connection timed out" in stderr_io.getvalue()


def test_session_api_error():
    stderr_io = io.StringIO()
    stderr_console = Console(file=stderr_io, color_system=None, width=120)
    client = FakeGitHubClient(error=APIError("Internal server error 500"))

    session = Session(client=client, stderr_console=stderr_console)
    code = session.run([])

    assert code == 4
    assert "Internal server error 500" in stderr_io.getvalue()


def test_session_unexpected_error():
    stderr_io = io.StringIO()
    stderr_console = Console(file=stderr_io, color_system=None, width=120)
    client = FakeGitHubClient(error=RuntimeError("Fatal boom"))

    session = Session(client=client, stderr_console=stderr_console)
    code = session.run([])

    assert code == 5
    assert "Unexpected error" in stderr_io.getvalue()


def test_main_entrypoint(monkeypatch):
    import pytest

    import trending_repos.__main__ as main_module

    monkeypatch.setattr("sys.argv", ["trending-repos", "--limit", "1"])
    monkeypatch.setattr(
        "trending_repos.infrastructure.cli.session.Session.run",
        lambda self, args: 0,
    )
    with pytest.raises(SystemExit) as exc:
        main_module.main()
    assert exc.value.code == 0
