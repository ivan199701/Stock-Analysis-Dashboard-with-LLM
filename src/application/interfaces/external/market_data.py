from abc import ABC, abstractmethod
from ....domain.entities.stock import Stock

class MarketDataInterface(ABC):
    """
    市場數據介面定義
    """
    @abstractmethod
    async def get_stock_data(self, symbol: str) -> Stock:
        """獲取股票數據"""
        pass

    @abstractmethod
    async def get_real_time_price(self, symbol: str) -> Price:
        """獲取即時價格"""
        pass