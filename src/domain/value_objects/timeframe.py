from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class TimeFrame:
    """
    時間範圍值物件
    """
    start: datetime
    end: datetime

    def duration_days(self) -> int:
        """計算天數"""
        return (self.end - self.start).days

    def is_valid(self) -> bool:
        """檢查時間範圍是否有效"""
        return self.start < self.end