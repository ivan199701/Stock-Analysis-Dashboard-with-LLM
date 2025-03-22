from dataclasses import dataclass
from typing import List, Dict
from ..value_objects.price import Price

@dataclass
class Stock:
    """
    Stock Entity Class
    """
    symbol: str
    name: str
    prices: List[Price]
    
    def calculate_sma(self, period: int = 20) -> List[float]:
        """Calculate Simple Moving Average"""
        pass

    def calculate_rsi(self, period: int = 14) -> List[float]:
        """Calculate RSI"""
        pass

    def calculate_macd(self) -> Dict[str, List[float]]:
        """Calculate MACD"""
        pass
