from openai import AsyncOpenAI
from typing import Dict
from ...application.interfaces.external.llm_service import LLMServiceInterface
from ...domain.entities.stock import Stock
from ...infrastructure.config.settings import Settings

class OpenAIService(LLMServiceInterface):
    """
    OpenAI API 實現
    """
    def __init__(self):
        settings = Settings()
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.system_prompt = self._load_system_prompt()

    async def analyze(self, 
                     technical_data: Dict, 
                     stock_data: Stock) -> str:
        """
        執行 AI 分析
        1. 整理輸入數據
        2. 調用 OpenAI API
        3. 處理回應
        """
        prompt = self._prepare_prompt(technical_data, stock_data)
        
        response = await self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        
        return response.choices[0].message.content

    def _load_system_prompt(self) -> str:
        """載入系統提示詞"""
        return """您是一位專業的股票市場分析師，專長於技術分析和基本面分析。
您將收到一支股票的技術指標數據和價格歷史，請提供以下分析：
1. 趨勢分析：短期、中期、長期趨勢判斷
2. 支撐與阻力位判斷
3. 技術指標解讀
4. 交易訊號判讀
5. 綜合建議

請以專業但易懂的方式回答，避免過度技術性語言，並清楚標示各分析部分。"""

    def _prepare_prompt(self, technical_data: Dict, stock_data: Stock) -> str:
        """準備提示詞"""
        # 取最近的價格數據以減少 token 用量
        recent_prices = stock_data.prices[-30:]
        price_data = "\n".join([
            f"{p.timestamp.date()}: 開:{p.open:.2f} 高:{p.high:.2f} 低:{p.low:.2f} 收:{p.close:.2f} 量:{p.volume}"
            for p in recent_prices
        ])
        
        prompt = f"""請分析以下股票數據:
股票代號: {stock_data.symbol}
股票名稱: {stock_data.name}

最近價格數據:
{price_data}

技術指標:
SMA: {technical_data.get('sma', [])[-10:]}
RSI: {technical_data.get('rsi', [])[-10:]}
MACD: {technical_data.get('macd', {}).get('macd', [])[-10:]}
MACD Signal: {technical_data.get('macd', {}).get('signal', [])[-10:]}

請提供完整分析報告。"""

        return prompt