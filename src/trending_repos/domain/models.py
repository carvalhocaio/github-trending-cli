"""Domain models for trending repositories."""

from dataclasses import dataclass
from enum import StrEnum


class Duration(StrEnum):
    """Supported time ranges for trending calculation."""

    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


@dataclass(frozen=True, slots=True)
class Repository:
    """Representation of a trending GitHub repository."""

    name: str
    description: str | None
    stars: int
    language: str | None
    url: str
