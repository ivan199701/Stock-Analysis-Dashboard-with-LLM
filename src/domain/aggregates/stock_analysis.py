from dataclasses import dataclass
from typing import List, Dict

class StockAnalysis:
    """
    股票分析的聚合根，整合所有分析結果
    Stock Analysis Aggregate Root, integrating all analysis results
    """
    def __init__(self, stock: Stock):
        self.stock = stock
        self.indicators = {}
        self.analysis_results = {}

    def analyze(self) -> Dict:
        """執行完整分析流程"""
        self._calculate_indicators()
        self._analyze_trend()
        self._generate_signals()
        return self.get_analysis_results()

    def _calculate_indicators(self):
        """計算所有技術指標"""
        self.indicators.update({
            'sma': self.stock.calculate_sma(),
            'rsi': self.stock.calculate_rsi(),
            'macd': self.stock.calculate_macd()
        })

    def _analyze_trend(self):
        """分析趨勢"""
        pass

    def _generate_signals(self):
        """生成交易訊號"""
        pass
        
    def get_analysis_results(self):
        """獲取分析結果"""
        return self.analysis_results