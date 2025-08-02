from abc import ABC, abstractmethod
from typing import Dict
from domain.entities.stock import Stock
from domain.value_objects.analysis_result import AnalysisResult

class LLMServiceInterface(ABC):
    @abstractmethod
    async def analyze(self,
                     technical_analysis: AnalysisResult,
                     stock_data: Stock) -> Dict:
        pass

    @abstractmethod
    async def generate_text(self, prompt: str) -> str:
        """
        Generates a text response based on a given prompt.
        """
        pass
