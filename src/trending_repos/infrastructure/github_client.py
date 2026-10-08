"""GitHub REST API client for searching repositories."""

import json
import os

import httpx

from trending_repos.domain.models import Repository
from trending_repos.errors import APIError, NetworkError, RateLimitError

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"


class GitHubClient:
    """Client for querying the GitHub Search Repositories API."""

    def __init__(
        self,
        token: str | None = None,
        client: httpx.Client | None = None,
        timeout: float = 10.0,
    ) -> None:
        self._token = token or os.environ.get("GITHUB_TOKEN")
        self._client = client or httpx.Client(timeout=timeout)

    def search_trending(
        self,
        cutoff_date: str,
        limit: int,
        language: str | None = None,
    ) -> list[Repository]:
        """Search for repositories created after cutoff_date, sorted by stars."""
        query = f"created:>{cutoff_date}"
        if language:
            query = f"{query} language:{language}"

        params = {
            "q": query,
            "sort": "stars",
            "order": "desc",
            "per_page": limit,
        }

        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "trending-repos-cli",
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"

        try:
            response = self._client.get(
                GITHUB_SEARCH_URL,
                params=params,
                headers=headers,
            )
        except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError) as err:
            raise NetworkError(f"Network error: {err}") from err

        if response.status_code in (403, 429):
            msg = "API rate limit exceeded"
            try:
                body = response.json()
                if isinstance(body, dict) and "message" in body:
                    msg = str(body["message"])
            except (ValueError, json.JSONDecodeError):
                pass
            raise RateLimitError(msg)

        if response.is_error:
            raise APIError(
                f"GitHub API error (status {response.status_code}): {response.text}"
            )

        data = response.json()
        items = data.get("items", [])
        return [
            Repository(
                name=item["full_name"],
                description=item.get("description"),
                stars=item["stargazers_count"],
                language=item.get("language"),
                url=item["html_url"],
            )
            for item in items
        ]
