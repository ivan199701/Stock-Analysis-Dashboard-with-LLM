from dataclasses import dataclass
from typing import Dict, List

@dataclass
class AnalysisDTO:
    """
    分析結果傳輸物件
    """
    technical_analysis: Dict
    ai_analysis: str
    signals: List[str]
    recommendation: str