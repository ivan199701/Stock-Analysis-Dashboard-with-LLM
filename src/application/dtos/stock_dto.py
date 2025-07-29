from dataclasses import dataclass
from typing import List, Dict

@dataclass
class StockDTO:
    symbol: str
    name: str
    current_price: float
    change_percent: float
    volume: int
    indicators: Dict[str, List[float]]
