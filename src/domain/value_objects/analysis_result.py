from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class AnalysisResult:
    """
    Analyze Result
    """
    trend: str
    strength: float
    signals: List[str]
    support_levels: List[float]
    resistance_levels: List[float]
    recommendation: str