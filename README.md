# trending-repos (GitHub Trending CLI)

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![uv](https://img.shields.io/badge/package%20manager-uv-blueviolet)
![pytest](https://img.shields.io/badge/tested%20with-pytest-0A9EDC)
![Ruff](https://img.shields.io/badge/lint%2Fformat-ruff-red)

A command-line tool that talks to the GitHub API and displays trending repositories filtered by duration and language in a rich terminal table.

Implementation of the [roadmap.sh - GitHub Trending CLI](https://roadmap.sh/projects/github-trending-cli) project.

---

## Features

- **Time Range Filtering:** Retrieve trending repositories by `day`, `week`, `month`, or `year` (defaults to `week`).
- **Configurable Limit:** Specify the number of repositories to display with `--limit` (defaults to `10`).
- **Language Filter:** Filter repositories by programming language via `--language` / `-l` (e.g. `python`, `rust`, `go`).
- **Polished Terminal Output:** Displays formatted tables (Rank, Repository, Stars, Language, Description) powered by `rich`.
- **Optional Authentication:** Supports `GITHUB_TOKEN` environment variable to increase GitHub API rate limits.
- **Robust Error Handling:** Distinguishes between usage errors, rate limits, connectivity failures, and API errors with explicit exit codes for scripting.

---

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

---

## Installation & Setup

```bash
git clone https://github.com/carvalhocaio/github-trending-cli.git
cd github-trending-cli
make sync
```

---

## Usage

Run via `uv run` or `make run`:

```bash
# Default: trending in the last week (10 repositories)
uv run trending-repos

# Trending today with a custom limit of 5
uv run trending-repos --duration day --limit 5

# Trending this month filtered by Python
uv run trending-repos --duration month --limit 20 --language python

# Using make run
make run ARGS="--duration month --limit 15 -l rust"
```

### Options

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--duration` | | `week` | Time range: `day`, `week`, `month`, `year` |
| `--limit` | | `10` | Number of repositories to fetch (> 0) |
| `--language` | `-l` | `None` | Filter by programming language |
| `--help` | `-h` | | Show help and options |

### Authenticated Requests (Optional)

Set `GITHUB_TOKEN` in your environment to avoid unauthenticated GitHub Search API rate limits:

```bash
export GITHUB_TOKEN=ghp_your_personal_access_token
uv run trending-repos --duration week
```

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Invalid usage or arguments |
| `2` | GitHub API rate limit exceeded |
| `3` | Network / connectivity error |
| `4` | Other non-2xx GitHub API response |
| `5` | Unexpected error |

---

## Development

```bash
make sync          # Install runtime and dev dependencies
make test          # Run tests with pytest
make lint          # Check code with ruff
make lint-fix      # Automatically fix linting issues
make format        # Format code with ruff
make format-check  # Verify code formatting
make check         # Run full check (lint, format-check, test)
```

---

## Project Structure

```text
src/trending_repos/
├── __init__.py
├── __main__.py             # Composition root
├── errors.py               # Custom exception hierarchy
├── domain/
│   ├── models.py           # Domain models: Duration, Repository
│   └── dates.py            # Cutoff date calculation for query filtering
└── infrastructure/
    ├── github_client.py    # GitHub REST Search API client via httpx
    └── cli/
        ├── parser.py       # Argument parsing and validation
        ├── display.py      # Rich terminal table formatting
        └── session.py      # Orchestration and exit code handling
tests/
└── unit/
    ├── test_dates.py
    ├── test_display.py
    ├── test_github_client.py
    ├── test_models.py
    ├── test_parser.py
    └── test_session.py
```
