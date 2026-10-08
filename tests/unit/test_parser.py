import pytest

from trending_repos.domain.models import Duration
from trending_repos.errors import UsageError
from trending_repos.infrastructure.cli.parser import CLIArgs, parse_args


def test_default_args():
    args = parse_args([])
    assert args == CLIArgs(
        duration=Duration.WEEK,
        limit=10,
        language=None,
    )


def test_custom_duration():
    args = parse_args(["--duration", "month"])
    assert args.duration == Duration.MONTH

    args_day = parse_args(["--duration", "day"])
    assert args_day.duration == Duration.DAY

    args_year = parse_args(["--duration", "year"])
    assert args_year.duration == Duration.YEAR


def test_custom_limit():
    args = parse_args(["--limit", "25"])
    assert args.limit == 25


def test_language_flag():
    args_short = parse_args(["-l", "rust"])
    assert args_short.language == "rust"

    args_long = parse_args(["--language", "python"])
    assert args_long.language == "python"


def test_invalid_duration():
    with pytest.raises(UsageError, match="invalid choice"):
        parse_args(["--duration", "decade"])


def test_invalid_limit_non_integer():
    with pytest.raises(UsageError, match="invalid int value"):
        parse_args(["--limit", "twenty"])


def test_invalid_limit_zero_or_negative():
    with pytest.raises(UsageError, match="--limit must be greater than 0"):
        parse_args(["--limit", "0"])

    with pytest.raises(UsageError, match="--limit must be greater than 0"):
        parse_args(["--limit", "-5"])
