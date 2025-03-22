class AnalysisService:
    """
    分析服務：協調整個分析流程
    """
    def __init__(self):
        self.market_data = YahooFinance()
        self.llm_service = OpenAIService()

    async def analyze_stock(self, symbol: str) -> AnalysisDTO:
        """
        執行完整股票分析
        1. 獲取市場數據
        2. 執行技術分析
        3. 獲取 AI 分析
        4. 整合結果
        """
        stock_data = await self.market_data.get_stock_data(symbol)
        analysis = StockAnalysis(stock_data)
        technical_results = analysis.analyze()
        
        ai_analysis = await self.llm_service.analyze(
            technical_results,
            stock_data
        )
        
        return self._create_analysis_dto(technical_results, ai_analysis)
        
    def _create_analysis_dto(self, technical_results, ai_analysis):
        """建立分析 DTO"""
        return AnalysisDTO(
            technical_analysis=technical_results,
            ai_analysis=ai_analysis,
            signals=technical_results.get('signals', []),
            recommendation=technical_results.get('recommendation', '')
        )