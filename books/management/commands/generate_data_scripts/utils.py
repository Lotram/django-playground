import math
from dataclasses import dataclass, field
from datetime import date, datetime, time, timezone
from random import randint


@dataclass
class DateTimeGenerator:
    start_date: date
    end_date: date
    start_timestamp: int = field(init=False)
    end_timestamp: int = field(init=False)

    def __post_init__(self):
        self.start_timestamp = int(
            datetime.combine(self.start_date, time.min).timestamp()
        )
        self.end_timestamp = int(datetime.combine(self.end_date, time.max).timestamp())

    def date_time_between(self):
        """
        like faker's date_time_between, but much faster
        """
        return datetime.fromtimestamp(
            randint(self.start_timestamp, self.end_timestamp), tz=timezone.utc
        )

    def date_between(self):
        return self.date_time_between().date()


def binomial_distribution(expected_value: int, n: int) -> list[float]:
    p = expected_value / n
    return [math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)]
