"""Main CLI composition root for trending-repos."""

import sys

from trending_repos.infrastructure.cli.session import Session


def main() -> None:
    """CLI entry point for trending-repos."""
    session = Session()
    sys.exit(session.run(sys.argv[1:]))


if __name__ == "__main__":
    main()
