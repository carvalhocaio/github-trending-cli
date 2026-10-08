# GitHub Trending CLI (`trending-repos`) - Design Specification

**Date:** 2026-10-08  
**Project:** `github-trending-cli` (`trending-repos`)  
**Challenge:** [roadmap.sh - GitHub Trending CLI](https://roadmap.sh/projects/github-trending-cli)

---

## 1. Overview & Requirements

The **GitHub Trending CLI** is a command-line tool that retrieves and displays trending GitHub repositories across specified time intervals (`day`, `week`, `month`, `year`), sorted by star count.

### Key Requirements
- **CLI Command:** `trending-repos`
- **CLI Arguments:**
  - `--duration`: Filter by time range (`day`, `week`, `month`, `year`). Default: `week`.
  - `--limit`: Number of repositories to fetch and display. Default: `10`. Minimum: `1`.
  - `--language` / `-l`: (Bonus) Filter by programming language (e.g. `python`, `rust`).
- **Data Source:** GitHub REST Search API (`GET https://api.github.com/search/repositories`).
- **Authentication:** Public requests by default; supports optional `GITHUB_TOKEN` environment variable to raise API rate limits.
- **Output:** Formatted terminal table using `rich` displaying Rank, Repository name, Stars count, Primary language, Description, and URL.
- **Error Handling:** Robust handling of invalid input, rate limiting, network disconnects, and API errors with explicit exit codes.

---

## 2. Architecture & Directory Layout

Following clean architecture principles established in `githubactivity`:

```text
src/trending_repos/
├── __init__.py
├── __main__.py               # Composition root (CLI entry point)
├── errors.py                 # Custom exception hierarchy
├── domain/
│   ├── __init__.py
│   ├── models.py             # Repository dataclass, Duration Enum
│   └── dates.py              # Cutoff date calculations based on Duration
└── infrastructure/
    ├── __init__.py
    ├── github_client.py       # GitHub Search API client via httpx
    └── cli/
        ├── __init__.py
        ├── parser.py          # Command-line argument parsing (argparse)
        ├── display.py         # Table formatting and terminal rendering (rich)
        └── session.py         # Application lifecycle and exit code handling
```

---

## 3. Detailed Component Design

### 3.1 Domain Layer (`domain/`)
- **`Duration`**:
  ```python
  from enum import StrEnum

  class Duration(StrEnum):
      DAY = "day"
      WEEK = "week"
      MONTH = "month"
      YEAR = "year"
  ```
- **`dates.py`**:
  Calculates the cutoff date formatted as `YYYY-MM-DD` for GitHub search queries:
  - `day`: `now - 1 day`
  - `week`: `now - 7 days`
  - `month`: `now - 30 days`
  - `year`: `now - 365 days`
  Accepts a `now: datetime | None = None` parameter for pure, deterministic unit testing.
- **`Repository`**:
  Frozen dataclass representing a trending repository:
  ```python
  @dataclass(frozen=True, slots=True)
  class Repository:
      name: str              # full_name (e.g., owner/repo)
      description: str | None
      stars: int             # stargazers_count
      language: str | None
      url: str               # html_url
  ```

### 3.2 Infrastructure Layer (`infrastructure/`)

#### GitHub Client (`github_client.py`)
- Uses `httpx.Client` with timeout (default 10s).
- Query structure:
  - Base URL: `https://api.github.com/search/repositories`
  - Query string: `q=created:>{cutoff_date}` (appends ` language:{lang}` if language provided).
  - Params: `sort=stars`, `order=desc`, `per_page={limit}`.
  - Headers:
    - `Accept: application/vnd.github+json`
    - `User-Agent: trending-repos-cli`
    - `Authorization: Bearer <token>` (if `GITHUB_TOKEN` is present in env).
- Maps HTTP status codes to custom exceptions:
  - `403` / `429`: `RateLimitError`
  - `ConnectError` / `TimeoutException`: `NetworkError`
  - Other non-2xx: `APIError`

#### CLI Parser (`parser.py`)
- Standard library `argparse.ArgumentParser`.
- Flags:
  - `--duration`: choices `["day", "week", "month", "year"]`, default `"week"`.
  - `--limit`: integer, default `10`. Raises `UsageError` if `<= 0`.
  - `-l` / `--language`: string, optional.

#### Display (`display.py`)
- Uses `rich.table.Table` with styling:
  - Columns: `#` (cyan), `Repository` (bold), `Stars` (yellow), `Language` (magenta), `Description` (dim/truncated).
- If no repositories are found, displays a clean informational message.
- Uses `rich.console.Console` writing to `sys.stdout` (or injectible console for tests).

#### Session (`session.py`)
- Orchestrates:
  1. Parse args.
  2. Compute cutoff date from `--duration`.
  3. Fetch repositories via `GitHubClient`.
  4. Render table via `Display`.
  5. Catch exceptions, format error messages (to stderr), and return appropriate exit codes.

---

## 4. Exit Codes

| Code | Meaning |
|------|---------|
| `0`  | Success |
| `1`  | Invalid usage / arguments |
| `2`  | GitHub API rate limit exceeded |
| `3`  | Network / connectivity error |
| `4`  | Other GitHub API errors |
| `5`  | Unexpected error |

---

## 5. Dependencies

- **Runtime:**
  - `httpx>=0.28.0` (modern HTTP client)
  - `rich>=13.9.0` (terminal formatting)
- **Dev:**
  - `pytest>=8.4.0`
  - `ruff>=0.15.0`
  - `pip-audit>=2.10.0`
  - `pre-commit>=4.0.0`

---

## 6. Testing Strategy

1. **Unit Tests (`tests/unit/`):**
   - `test_dates.py`: Test date delta calculation for all 4 durations with fixed freeze-gun / deterministic UTC time.
   - `test_parser.py`: Verify valid defaults, custom arguments, short flag aliases, and invalid limit/duration validation.
   - `test_github_client.py`: Mock HTTP calls using `httpx.MockTransport` to verify URL parameters, header injection, rate limit handling, and network errors.
   - `test_display.py`: Verify table construction, row formatting, and empty state rendering with injected string/mock console.
   - `test_session.py`: Verify end-to-end exit codes with faked client for success and failure scenarios.
2. **Quality Gates:**
   - `make lint` (`ruff check .`)
   - `make format-check` (`ruff format --check .`)
   - `make test` (`pytest -v`)
   - `make check` (runs all checks)
