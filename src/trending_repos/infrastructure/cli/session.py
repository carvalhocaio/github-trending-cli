"""CLI session orchestration and exit code mapping."""

from rich.console import Console

from trending_repos.domain.dates import calculate_cutoff_date
from trending_repos.errors import (
    APIError,
    NetworkError,
    RateLimitError,
    UsageError,
)
from trending_repos.infrastructure.cli.display import (
    render_error,
    render_repositories,
)
from trending_repos.infrastructure.cli.parser import parse_args
from trending_repos.infrastructure.github_client import GitHubClient


class Session:
    """Coordinates CLI execution lifecycle and handles errors."""

    def __init__(
        self,
        client: GitHubClient | None = None,
        stdout_console: Console | None = None,
        stderr_console: Console | None = None,
    ) -> None:
        self._client = client or GitHubClient()
        self._stdout = stdout_console or Console()
        self._stderr = stderr_console or Console(stderr=True)

    def run(self, args: list[str] | None = None) -> int:
        """Run the CLI session and return an integer exit code."""
        try:
            parsed = parse_args(args)
            cutoff_date = calculate_cutoff_date(parsed.duration)
            repos = self._client.search_trending(
                cutoff_date=cutoff_date,
                limit=parsed.limit,
                language=parsed.language,
            )
            render_repositories(repos, console=self._stdout)
            return 0
        except UsageError as err:
            render_error(str(err), console=self._stderr)
            return 1
        except RateLimitError as err:
            render_error(
                f"{err}\nTip: Export GITHUB_TOKEN=your_token to increase rate limits.",
                console=self._stderr,
            )
            return 2
        except NetworkError as err:
            render_error(str(err), console=self._stderr)
            return 3
        except APIError as err:
            render_error(str(err), console=self._stderr)
            return 4
        except Exception as err:
            render_error(f"Unexpected error: {err}", console=self._stderr)
            return 5
