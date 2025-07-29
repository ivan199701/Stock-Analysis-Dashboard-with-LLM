from domain.aggregates.stock_analysis import StockAnalysis
from domain.entities.stock import Stock
from application.dtos.analysis_dto import AnalysisDTO
from application.interfaces.external.llm_service import LLMServiceInterface

class AnalysisService:
    def __init__(self, llm_service: LLMServiceInterface):
        self.llm_service = llm_service

    async def analyze_stock(self, stock_data: Stock, timeframe: str = 'medium', indicators: list = None) -> AnalysisDTO:
        stock_analysis = StockAnalysis(stock_data)
        technical_analysis = stock_analysis.analyze(timeframe, indicators)
        
        ai_analysis = await self.llm_service.analyze(
            technical_analysis,
            stock_data
        )
        
        return self._create_analysis_dto(stock_data, technical_analysis, ai_analysis)

    def _create_analysis_dto(self, stock_data: Stock, technical_analysis, ai_analysis) -> AnalysisDTO:
        return AnalysisDTO(
            stock=stock_data,
            technical_analysis=technical_analysis,
            ai_analysis=ai_analysis
        )