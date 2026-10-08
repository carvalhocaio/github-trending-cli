import io

from rich.console import Console

from trending_repos.domain.models import Repository
from trending_repos.infrastructure.cli.display import (
    render_error,
    render_repositories,
)


def test_render_repositories_with_data():
    output = io.StringIO()
    console = Console(file=output, color_system=None, width=120)

    repos = [
        Repository(
            name="pallets/flask",
            description="The Python micro framework for building web applications.",
            stars=68000,
            language="Python",
            url="https://github.com/pallets/flask",
        ),
        Repository(
            name="torvalds/linux",
            description=None,
            stars=175000,
            language="C",
            url="https://github.com/torvalds/linux",
        ),
    ]

    render_repositories(repos, console=console)
    text = output.getvalue()

    assert "pallets/flask" in text
    assert "The Python micro framework" in text
    assert "68,000" in text
    assert "Python" in text
    assert "torvalds/linux" in text
    assert "175,000" in text
    assert "C" in text


def test_render_repositories_empty():
    output = io.StringIO()
    console = Console(file=output, color_system=None, width=120)

    render_repositories([], console=console)
    text = output.getvalue()

    assert "No trending repositories found" in text


def test_render_error():
    output = io.StringIO()
    console = Console(file=output, color_system=None, width=120)

    render_error("API rate limit exceeded", console=console)
    text = output.getvalue()

    assert "API rate limit exceeded" in text
