from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    DEFAULT_TIMEFRAME: str = "1y"
    UPDATE_INTERVAL: int = 60
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()