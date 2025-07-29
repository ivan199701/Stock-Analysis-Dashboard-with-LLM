from dataclasses import dataclass
from typing import List, Dict
from domain.value_objects.analysis_result import AnalysisResult
from domain.entities.stock import Stock

@dataclass
class AnalysisDTO:
    stock: Stock
    technical_analysis: AnalysisResult
    ai_analysis: Dict