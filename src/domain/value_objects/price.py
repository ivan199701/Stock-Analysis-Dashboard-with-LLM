from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Price:
    """
    價格值物件
    """
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    def calculate_change(self) -> float:
        """計算漲跌幅"""
        return (self.close - self.open) / self.open * 100