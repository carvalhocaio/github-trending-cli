from trending_repos.domain.models import Duration, Repository
from trending_repos.errors import (
    APIError,
    NetworkError,
    RateLimitError,
    TrendingReposError,
    UsageError,
)


def test_duration_enum_values():
    assert Duration.DAY.value == "day"
    assert Duration.WEEK.value == "week"
    assert Duration.MONTH.value == "month"
    assert Duration.YEAR.value == "year"
    assert list(Duration) == ["day", "week", "month", "year"]


def test_repository_creation():
    repo = Repository(
        name="facebook/react",
        description="The library for web and native user interfaces",
        stars=230000,
        language="JavaScript",
        url="https://github.com/facebook/react",
    )
    assert repo.name == "facebook/react"
    assert repo.description == "The library for web and native user interfaces"
    assert repo.stars == 230000
    assert repo.language == "JavaScript"
    assert repo.url == "https://github.com/facebook/react"


def test_repository_optional_fields():
    repo = Repository(
        name="owner/repo",
        description=None,
        stars=10,
        language=None,
        url="https://github.com/owner/repo",
    )
    assert repo.description is None
    assert repo.language is None


def test_errors_hierarchy():
    assert issubclass(UsageError, TrendingReposError)
    assert issubclass(RateLimitError, TrendingReposError)
    assert issubclass(NetworkError, TrendingReposError)
    assert issubclass(APIError, TrendingReposError)

    err = RateLimitError("rate limit exceeded")
    assert str(err) == "rate limit exceeded"
