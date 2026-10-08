# GitHub Trending CLI Implementation Plan

> Implementation plan for building `trending-repos` CLI based on roadmap.sh specifications.

**Goal:** Build a robust, test-driven CLI tool that fetches trending GitHub repositories using the GitHub REST API and renders them with `rich`.

**Architecture:** Clean layered architecture with pure domain models (`models.py`, `dates.py`), standard `argparse` CLI parser, `httpx`-based GitHub search client with error mapping, and `rich` terminal table display orchestrated by `session.py`.

**Tech Stack:** Python 3.12+, `httpx`, `rich`, `pytest`, `ruff`, `uv`.

**Spec:** `docs/design.md`

## Global Constraints
- Target Python: `>=3.12`
- Runtime dependencies: `httpx>=0.28.0`, `rich>=13.9.0`
- CLI binary name: `trending-repos`
- Testing framework: `pytest`
- Linter / Formatter: `ruff`
- Exit codes:
  - `0`: Success
  - `1`: Invalid usage / arguments
  - `2`: GitHub API rate limit exceeded
  - `3`: Network / connectivity error
  - `4`: Other GitHub API errors
  - `5`: Unexpected error

---

### Task 1: Domain Models and Error Hierarchy

**Files:**
- Create: `src/trending_repos/domain/models.py`
- Create: `src/trending_repos/domain/__init__.py`
- Create: `src/trending_repos/errors.py`
- Test: `tests/unit/test_models.py`

**Interfaces:**
- Produces:
  - `Duration(StrEnum)`: `DAY = "day"`, `WEEK = "week"`, `MONTH = "month"`, `YEAR = "year"`
  - `Repository(dataclass)`: `name: str`, `description: str | None`, `stars: int`, `language: str | None`, `url: str`
  - Exceptions: `TrendingReposError`, `UsageError`, `RateLimitError`, `NetworkError`, `APIError`

- [ ] **Step 1: Write tests for domain models and errors**
- [ ] **Step 2: Run pytest to verify failure**
- [ ] **Step 3: Implement `models.py` and `errors.py`**
- [ ] **Step 4: Run pytest to verify pass**
- [ ] **Step 5: Commit**

---

### Task 2: Date Cutoff Calculation

**Files:**
- Create: `src/trending_repos/domain/dates.py`
- Test: `tests/unit/test_dates.py`

**Interfaces:**
- Consumes: `Duration` from `domain.models`
- Produces: `calculate_cutoff_date(duration: Duration, now: datetime | None = None) -> str` returning `"YYYY-MM-DD"`

- [ ] **Step 1: Write tests for `calculate_cutoff_date` for day (1d), week (7d), month (30d), year (365d)**
- [ ] **Step 2: Run pytest to verify failure**
- [ ] **Step 3: Implement `calculate_cutoff_date`**
- [ ] **Step 4: Run pytest to verify pass**
- [ ] **Step 5: Commit**

---

### Task 3: CLI Argument Parsing

**Files:**
- Create: `src/trending_repos/infrastructure/cli/parser.py`
- Create: `src/trending_repos/infrastructure/cli/__init__.py`
- Test: `tests/unit/test_parser.py`

**Interfaces:**
- Consumes: `Duration` from `domain.models`, `UsageError` from `errors`
- Produces: `parse_args(args: list[str] | None = None) -> CLIArgs` with fields: `duration: Duration`, `limit: int`, `language: str | None`

- [ ] **Step 1: Write tests for parser default arguments and flags (`--duration`, `--limit`, `--language`) and validation (`limit <= 0`)**
- [ ] **Step 2: Run pytest to verify failure**
- [ ] **Step 3: Implement `parser.py`**
- [ ] **Step 4: Run pytest to verify pass**
- [ ] **Step 5: Commit**

---

### Task 4: GitHub API Client

**Files:**
- Create: `src/trending_repos/infrastructure/github_client.py`
- Create: `src/trending_repos/infrastructure/__init__.py`
- Test: `tests/unit/test_github_client.py`

**Interfaces:**
- Consumes: `Repository` from `domain.models`, `RateLimitError`, `NetworkError`, `APIError` from `errors`
- Produces: `GitHubClient.search_trending(cutoff_date: str, limit: int, language: str | None = None) -> list[Repository]`

- [ ] **Step 1: Write tests using `httpx.MockTransport` for success, query parameters, auth header from `GITHUB_TOKEN`, 403/429 rate limit, 500 error, and network timeout**
- [ ] **Step 2: Run pytest to verify failure**
- [ ] **Step 3: Implement `GitHubClient`**
- [ ] **Step 4: Run pytest to verify pass**
- [ ] **Step 5: Commit**

---

### Task 5: Terminal Display Rendering

**Files:**
- Create: `src/trending_repos/infrastructure/cli/display.py`
- Test: `tests/unit/test_display.py`

**Interfaces:**
- Consumes: `Repository` from `domain.models`
- Produces: `render_repositories(repos: list[Repository], console: Console | None = None) -> None`, `render_error(message: str, console: Console | None = None) -> None`

- [ ] **Step 1: Write tests verifying `rich.table.Table` output columns, empty state message, and error rendering with in-memory `Console`**
- [ ] **Step 2: Run pytest to verify failure**
- [ ] **Step 3: Implement `display.py`**
- [ ] **Step 4: Run pytest to verify pass**
- [ ] **Step 5: Commit**

---

### Task 6: CLI Session Orchestration & Entry Point

**Files:**
- Create: `src/trending_repos/infrastructure/cli/session.py`
- Create: `src/trending_repos/__main__.py`
- Test: `tests/unit/test_session.py`

**Interfaces:**
- Consumes: `parse_args`, `GitHubClient`, `calculate_cutoff_date`, `render_repositories`, `render_error`
- Produces: `Session.run(args: list[str] | None = None) -> int`, `main() -> None`

- [ ] **Step 1: Write tests verifying end-to-end exit codes for success (0), usage errors (1), rate limit (2), network error (3), API error (4), unexpected error (5)**
- [ ] **Step 2: Run pytest to verify failure**
- [ ] **Step 3: Implement `session.py` and `__main__.py`**
- [ ] **Step 4: Run pytest to verify pass**
- [ ] **Step 5: Commit**

---

### Task 7: Full Verification & Documentation

**Files:**
- Modify: `README.md`
- Test: Run `make check` (lint, format-check, test)

- [ ] **Step 1: Write complete project README.md with usage instructions, options, and exit codes**
- [ ] **Step 2: Run `make check` to ensure all linters, formatting, and tests pass**
- [ ] **Step 3: Test CLI manually using `make run ARGS="--duration day --limit 5"`**
- [ ] **Step 4: Commit**
