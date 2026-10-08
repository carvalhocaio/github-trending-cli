import httpx
import pytest

from trending_repos.domain.models import Repository
from trending_repos.errors import APIError, NetworkError, RateLimitError
from trending_repos.infrastructure.github_client import GitHubClient


def test_search_trending_success():
    items = [
        {
            "full_name": "astral-sh/uv",
            "description": "An extremely fast Python package manager",
            "stargazers_count": 45000,
            "language": "Rust",
            "html_url": "https://github.com/astral-sh/uv",
        },
        {
            "full_name": "textualize/rich",
            "description": "Rich is a Python library for rich text",
            "stargazers_count": 50000,
            "language": "Python",
            "html_url": "https://github.com/textualize/rich",
        },
    ]

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.host == "api.github.com"
        assert request.url.path == "/search/repositories"
        assert request.url.params["q"] == "created:>2026-10-01"
        assert request.url.params["per_page"] == "2"
        assert request.headers["Accept"] == "application/vnd.github+json"
        assert request.headers["User-Agent"] == "trending-repos-cli"
        return httpx.Response(200, json={"items": items})

    client = GitHubClient(client=httpx.Client(transport=httpx.MockTransport(handler)))
    repos = client.search_trending(cutoff_date="2026-10-01", limit=2)

    assert repos == [
        Repository(
            name="astral-sh/uv",
            description="An extremely fast Python package manager",
            stars=45000,
            language="Rust",
            url="https://github.com/astral-sh/uv",
        ),
        Repository(
            name="textualize/rich",
            description="Rich is a Python library for rich text",
            stars=50000,
            language="Python",
            url="https://github.com/textualize/rich",
        ),
    ]


def test_search_trending_with_language_and_token():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.params["q"] == "created:>2026-10-01 language:python"
        assert request.headers["Authorization"] == "Bearer test_secret_token"
        return httpx.Response(200, json={"items": []})

    client = GitHubClient(
        token="test_secret_token",
        client=httpx.Client(transport=httpx.MockTransport(handler)),
    )
    repos = client.search_trending(cutoff_date="2026-10-01", limit=5, language="python")
    assert repos == []


def test_search_trending_rate_limit_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, json={"message": "API rate limit exceeded for user"})

    client = GitHubClient(client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(RateLimitError, match="API rate limit exceeded"):
        client.search_trending(cutoff_date="2026-10-01", limit=10)


def test_search_trending_api_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, text="Internal Server Error")

    client = GitHubClient(client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(APIError, match="GitHub API error \\(status 500\\)"):
        client.search_trending(cutoff_date="2026-10-01", limit=10)


def test_search_trending_network_error():
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Failed to connect")

    client = GitHubClient(client=httpx.Client(transport=httpx.MockTransport(handler)))
    with pytest.raises(NetworkError, match="Network error"):
        client.search_trending(cutoff_date="2026-10-01", limit=10)
