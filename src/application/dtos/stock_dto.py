from dataclasses import dataclass
from typing import Dict, List

@dataclass
class StockDTO:
    """
    股票資料傳輸物件
    """
    symbol: str
    name: str
    current_price: float
    change_percent: float
    volume: int
    indicators: Dict[str, List[float]]