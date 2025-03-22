from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class AnalysisResult:
    """
    分析結果值物件
    """
    trend: str
    strength: float
    signals: List[str]
    support_levels: List[float]
    resistance_levels: List[float]
    recommendation: str