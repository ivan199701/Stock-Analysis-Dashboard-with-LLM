from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TimeFrame:

    start: datetime
    end: datetime

    def duration_days(self) -> int:
        return (self.end - self.start).days

    def is_valid(self) -> bool:
        return self.start < self.end