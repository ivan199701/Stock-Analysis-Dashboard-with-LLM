from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Price:
    
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    def calculate_change(self) -> float:
        """calculate change"""
        return (self.close - self.open) / self.open * 100