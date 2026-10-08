"""CLI argument parser for trending-repos."""

import argparse
from dataclasses import dataclass

from trending_repos.domain.models import Duration
from trending_repos.errors import UsageError

DEFAULT_DURATION = "week"
DEFAULT_LIMIT = 10


@dataclass(frozen=True, slots=True)
class CLIArgs:
    """Parsed and validated command-line arguments."""

    duration: Duration
    limit: int
    language: str | None


class _CLIArgumentParser(argparse.ArgumentParser):
    """Custom ArgumentParser that raises UsageError instead of exiting."""

    def error(self, message: str) -> None:
        raise UsageError(message)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for trending-repos."""
    parser = _CLIArgumentParser(
        prog="trending-repos",
        description="Display trending GitHub repositories.",
    )
    parser.add_argument(
        "--duration",
        choices=[d.value for d in Duration],
        default=DEFAULT_DURATION,
        help=(
            "Time range for trending repositories (day, week, month, year). "
            "Default: week."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=DEFAULT_LIMIT,
        help="Number of repositories to display. Default: 10.",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default=None,
        help="Filter repositories by programming language (e.g. python, rust).",
    )
    return parser


def parse_args(args: list[str] | None = None) -> CLIArgs:
    """Parse and validate CLI arguments."""
    parser = create_parser()
    parsed = parser.parse_args(args)

    if parsed.limit <= 0:
        raise UsageError(f"--limit must be greater than 0, got {parsed.limit}")

    return CLIArgs(
        duration=Duration(parsed.duration),
        limit=parsed.limit,
        language=parsed.language,
    )
