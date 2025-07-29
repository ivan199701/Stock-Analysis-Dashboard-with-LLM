from abc import ABC, abstractmethod
from domain.entities.stock import Stock
from domain.value_objects.price import Price

class MarketDataInterface(ABC):
    @abstractmethod
    async def get_stock_data(self, symbol: str) -> Stock:
        pass

    @abstractmethod
    async def get_real_time_price(self, symbol: str) -> Price:
        pass