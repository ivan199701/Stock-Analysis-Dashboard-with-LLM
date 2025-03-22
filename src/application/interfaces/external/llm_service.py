from abc import ABC, abstractmethod
from typing import Dict
from ....domain.entities.stock import Stock

class LLMServiceInterface(ABC):
    """
    LLM 服務介面定義
    """
    @abstractmethod
    async def analyze(self, 
                     technical_data: Dict, 
                     stock_data: Stock) -> str:
        """執行 AI 分析"""
        pass