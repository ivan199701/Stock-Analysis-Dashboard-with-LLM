from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    應用程式設定
    """
    OPENAI_API_KEY: str
    DEFAULT_TIMEFRAME: str = "1y"
    UPDATE_INTERVAL: int = 60
    TECHNICAL_INDICATORS: List[str] = [
        "SMA", "RSI", "MACD"
    ]

    class Config:
        env_file = ".env"