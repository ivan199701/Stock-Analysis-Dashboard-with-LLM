from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass(frozen=True)
class AnalysisResult:
    """
    Analysis Result Value Object
    """
    trend: str  # "bullish", "bearish", "neutral"
    strength: float  # 0.0 to 1.0
    signals: List[str]
    support_levels: List[float]
    resistance_levels: List[float]
    recommendation: str  # "BUY", "SELL", "HOLD"
    indicators: Dict = field(default_factory=dict, repr=False)

    def is_actionable(self) -> bool:
        """Determine if the analysis provides a clear action signal"""
        return self.recommendation in ["BUY", "SELL"] and self.strength > 0.7

    def get_risk_level(self) -> str:
        """Calculate risk level based on analysis"""
        if self.strength < 0.3:
            return "LOW"
        elif self.strength < 0.7:
            return "MEDIUM"
        else:
            return "HIGH"

    def get_nearest_support(self, current_price: float) -> Optional[float]:
        """Find the nearest support level below current price"""
        supports_below = [s for s in self.support_levels if s < current_price]
        return max(supports_below) if supports_below else None

    def get_nearest_resistance(self, current_price: float) -> Optional[float]:
        """Find the nearest resistance level above current price"""
        resistances_above = [
            r for r in self.resistance_levels if r > current_price]
        return min(resistances_above) if resistances_above else None