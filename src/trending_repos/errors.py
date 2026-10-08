"""Custom exception hierarchy for trending-repos CLI."""


class TrendingReposError(Exception):
    """Base exception for all domain and infrastructure errors."""


class UsageError(TrendingReposError):
    """Raised when command-line arguments are invalid."""


class RateLimitError(TrendingReposError):
    """Raised when the GitHub API rate limit is exceeded."""


class NetworkError(TrendingReposError):
    """Rose on network timeout or connection failure."""


class APIError(TrendingReposError):
    """Raised when GitHub API returns an unexpected non-2xx status."""
