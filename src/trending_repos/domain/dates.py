"""Date calculation utilities for trending repository searches."""

from datetime import UTC, datetime, timedelta

from trending_repos.domain.models import Duration

_DURATION_DELTAS: dict[Duration, timedelta] = {
    Duration.DAY: timedelta(days=1),
    Duration.WEEK: timedelta(days=7),
    Duration.MONTH: timedelta(days=30),
    Duration.YEAR: timedelta(days=365),
}


def calculate_cutoff_date(duration: Duration, now: datetime | None = None) -> str:
    """Calculate the YYYY-MM-DD cutoff date for a given Duration."""
    current_time = now if now is not None else datetime.now(UTC)
    delta = _DURATION_DELTAS[duration]
    cutoff = current_time - delta
    return cutoff.strftime("%Y-%m-%d")
