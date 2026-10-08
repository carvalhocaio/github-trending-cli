"""Terminal display rendering using rich."""

from rich.console import Console
from rich.table import Table

from trending_repos.domain.models import Repository


def render_repositories(
    repos: list[Repository], console: Console | None = None
) -> None:
    """Render a table of trending repositories or empty state message."""
    active_console = console or Console()

    if not repos:
        active_console.print("[yellow]No trending repositories found.[/yellow]")
        return

    table = Table(title="Trending Repositories", show_lines=True)
    table.add_column("#", style="cyan", justify="right", no_wrap=True)
    table.add_column("Repository", style="bold green", no_wrap=True)
    table.add_column("Stars", style="yellow", justify="right")
    table.add_column("Language", style="magenta")
    table.add_column("Description", style="white")

    for rank, repo in enumerate(repos, start=1):
        stars_formatted = f"{repo.stars:,}"
        language_formatted = repo.language or "-"
        description_formatted = repo.description or "-"
        table.add_row(
            str(rank),
            repo.name,
            stars_formatted,
            language_formatted,
            description_formatted,
        )

    active_console.print(table)


def render_error(message: str, console: Console | None = None) -> None:
    """Render an error message to terminal."""
    active_console = console or Console(stderr=True)
    active_console.print(f"[bold red]Error:[/bold red] {message}")
