import google.generativeai as genai
import json
from typing import Dict

from application.interfaces.external.llm_service import LLMServiceInterface
from domain.entities.stock import Stock
from domain.value_objects.analysis_result import AnalysisResult
from infrastructure.utils.retry_decorator import async_retry
from infrastructure.config.settings import Settings


class GoogleGeminiService(LLMServiceInterface):
    def __init__(self):
        self.settings = Settings()
        genai.configure(api_key=self.settings.GEMINI_API_KEY)
        # This is a placeholder, the model name might be different
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    @async_retry()
    async def analyze(self,
                      technical_analysis: AnalysisResult,
                      stock_data: Stock) -> Dict:
        prompt = self._build_prompt(technical_analysis, stock_data)

        try:
            response = await self.model.generate_content_async(prompt)

            # Extracting the json string from the response
            json_string = response.text.strip().replace(
                '```json', '').replace('```', '').strip()

            return json.loads(json_string)
        except Exception as e:
            raise e

    def _build_prompt(self, tech_analysis: AnalysisResult, stock: Stock) -> str:
        
        indicator_details = ""
        if 'sma' in tech_analysis.indicators:
            indicator_details += f"- SMA: Current value is {tech_analysis.indicators['sma'][-1]:.2f}\n"
        if 'ema' in tech_analysis.indicators:
            indicator_details += f"- EMA: Current value is {tech_analysis.indicators['ema'][-1]:.2f}\n"
        if 'rsi' in tech_analysis.indicators:
            indicator_details += f"- RSI: Current value is {tech_analysis.indicators['rsi'][-1]:.2f}\n"
        if 'macd' in tech_analysis.indicators:
            indicator_details += f"- MACD: MACD line @ {tech_analysis.indicators['macd']['macd'][-1]:.2f}, Signal line @ {tech_analysis.indicators['macd']['signal'][-1]:.2f}\n"
        if 'bbands' in tech_analysis.indicators:
            indicator_details += f"- Bollinger Bands: Upper @ {tech_analysis.indicators['bbands']['upper'][-1]:.2f}, Lower @ {tech_analysis.indicators['bbands']['lower'][-1]:.2f}\n"
        if 'stoch' in tech_analysis.indicators:
            indicator_details += f"- Stochastic Oscillator: %K @ {tech_analysis.indicators['stoch']['k'][-1]:.2f}, %D @ {tech_analysis.indicators['stoch']['d'][-1]:.2f}\n"
        if 'atr' in tech_analysis.indicators:
            indicator_details += f"- ATR: Current value is {tech_analysis.indicators['atr'][-1]:.2f}\n"
        if 'obv' in tech_analysis.indicators:
            indicator_details += f"- OBV: Current value is {tech_analysis.indicators['obv'][-1]:.2f}\n"

        prompt = f"""
        **Persona:** You are a Stock Trader specializing in Technical Analysis at a top financial institution. Your language should be professional, clear, and focused on actionable insights.

        **Task:** Provide a structured JSON analysis for the stock below. Base your entire analysis *only* on the user-selected technical indicator data provided. Do not use any external knowledge or other indicators.

        **Stock Information:**
        - Symbol: {stock.symbol}
        - Name: {stock.name}
        - Current Price: {stock.prices[-1].close if stock.prices else 'N/A'}

        **User-Selected Indicator Data:**
        {indicator_details if indicator_details else "No specific indicators were selected by the user."}

        **Key Signals Detected by the System:**
        - {', '.join(tech_analysis.signals) if tech_analysis.signals else "None"}

        **Key Levels Identified by the System:**
        - Support: {tech_analysis.support_levels}
        - Resistance: {tech_analysis.resistance_levels}

        **Your Analysis (JSON Output Only):**
        Generate a JSON object with the following structure. Ensure your analysis in each field is derived *directly* from the data provided above.
        {{
          "recommendation": "BUY" | "SELL" | "HOLD",
          "confidence": "High" | "Medium" | "Low",
          "summary": "A concise summary of the aoverall market sentiment for this stock, referencing the provided data.",
          "detailed_analysis": {{
            "trend_analysis": "Analyze the trend based on Moving Averages if present. Is the price above/below the averages? Are there any crossovers?",
            "momentum_analysis": "Analyze momentum using RSI, MACD, and Stochastic Oscillator if present. Mention overbought/oversold levels and crossovers.",
            "volatility_analysis": "Analyze volatility using Bollinger Bands and ATR if present. Are the bands squeezing or expanding? Is volatility high or low?",
            "volume_analysis": "Analyze volume using OBV if present. Does the volume confirm the price trend?",
            "key_levels_analysis": "Discuss the importance of the identified support and resistance levels in the current context."
          }}
        }}
        """
        return prompt

    @async_retry()
    async def generate_text(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            # A real application should have more sophisticated logging/error handling
            print(f"Error generating text: {e}")
            raise e
