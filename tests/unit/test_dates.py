import re
from datetime import UTC, datetime

from trending_repos.domain.dates import calculate_cutoff_date
from trending_repos.domain.models import Duration


def test_calculate_cutoff_date_fixed_times():
    fixed_now = datetime(2026, 10, 8, 12, 0, 0, tzinfo=UTC)

    assert calculate_cutoff_date(Duration.DAY, now=fixed_now) == "2026-10-07"
    assert calculate_cutoff_date(Duration.WEEK, now=fixed_now) == "2026-10-01"
    assert calculate_cutoff_date(Duration.MONTH, now=fixed_now) == "2026-09-08"
    assert calculate_cutoff_date(Duration.YEAR, now=fixed_now) == "2025-10-08"


def test_calculate_cutoff_date_default_now():
    cutoff = calculate_cutoff_date(Duration.WEEK)
    assert re.match(r"^\d{4}-\d{2}-\d{2}$", cutoff)
