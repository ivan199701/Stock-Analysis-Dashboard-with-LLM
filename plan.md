# Stock Analysis System Development Plan - Detailed File Description

## 1. Domain Layer

### 1.1 aggregates/stock_analysis.py
```python
from dataclasses import dataclass
from typing import List, Dict

class StockAnalysis:
    """
    Stock analysis aggregate root, integrating all analysis results
    """
    def __init__(self, stock: Stock):
        self.stock = stock
        self.indicators = {}
        self.analysis_results = {}

    def analyze(self) -> Dict:
        """Execute complete analysis process"""
        self._calculate_indicators()
        self._analyze_trend()
        self._generate_signals()
        return self.get_analysis_results()

    def _calculate_indicators(self):
        """Calculate all technical indicators"""
        self.indicators.update({
            'sma': self.stock.calculate_sma(),
            'rsi': self.stock.calculate_rsi(),
            'macd': self.stock.calculate_macd()
        })

    def _analyze_trend(self):
        """Analyze trend"""
        pass

    def _generate_signals(self):
        """Generate trading signals"""
        pass
```

### 1.2 entities/stock.py
```python
@dataclass
class Stock:
    """
    Stock entity class
    """
    symbol: str
    name: str
    prices: List[Price]
    
    def calculate_sma(self, period: int = 20) -> List[float]:
        """Calculate Simple Moving Average"""
        pass

    def calculate_rsi(self, period: int = 14) -> List[float]:
        """Calculate RSI"""
        pass

    def calculate_macd(self) -> Dict[str, List[float]]:
        """Calculate MACD"""
        pass
```

### 1.3 value_objects/price.py
```python
@dataclass(frozen=True)
class Price:
    """
    Price value object
    """
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    def calculate_change(self) -> float:
        """Calculate price change percentage"""
        return (self.close - self.open) / self.open * 100
```

### 1.4 value_objects/timeframe.py
```python
@dataclass(frozen=True)
class TimeFrame:
    """
    Time frame value object
    """
    start: datetime
    end: datetime

    def duration_days(self) -> int:
        """Calculate number of days"""
        return (self.end - self.start).days

    def is_valid(self) -> bool:
        """Check if time range is valid"""
        return self.start < self.end
```

### 1.5 value_objects/analysis_result.py
```python
@dataclass(frozen=True)
class AnalysisResult:
    """
    Analysis result value object
    """
    trend: str
    strength: float
    signals: List[str]
    support_levels: List[float]
    resistance_levels: List[float]
    recommendation: str
```

## 2. Application Layer

### 2.1 services/analysis_service.py
```python
class AnalysisService:
    """
    Analysis service: coordinates the entire analysis process
    """
    def __init__(self):
        self.market_data = YahooFinance()
        self.llm_service = OpenAIService()

    async def analyze_stock(self, symbol: str) -> AnalysisDTO:
        """
        Execute complete stock analysis
        1. Get market data
        2. Perform technical analysis
        3. Get AI analysis
        4. Integrate results
        """
        stock_data = await self.market_data.get_stock_data(symbol)
        analysis = StockAnalysis(stock_data)
        technical_results = analysis.analyze()
        
        ai_analysis = await self.llm_service.analyze(
            technical_results,
            stock_data
        )
        
        return self._create_analysis_dto(technical_results, ai_analysis)
```

### 2.2 interfaces/external/market_data.py
```python
from abc import ABC, abstractmethod

class MarketDataInterface(ABC):
    """
    Market data interface definition
    """
    @abstractmethod
    async def get_stock_data(self, symbol: str) -> Stock:
        """Get stock data"""
        pass

    @abstractmethod
    async def get_real_time_price(self, symbol: str) -> Price:
        """Get real-time price"""
        pass
```

### 2.3 interfaces/external/llm_service.py
```python
from abc import ABC, abstractmethod

class LLMServiceInterface(ABC):
    """
    LLM service interface definition
    """
    @abstractmethod
    async def analyze(self, 
                     technical_data: Dict, 
                     stock_data: Stock) -> str:
        """Execute AI analysis"""
        pass
```

### 2.4 dtos/stock_dto.py
```python
@dataclass
class StockDTO:
    """
    Stock data transfer object
    """
    symbol: str
    name: str
    current_price: float
    change_percent: float
    volume: int
    indicators: Dict[str, List[float]]
```

### 2.5 dtos/analysis_dto.py
```python
@dataclass
class AnalysisDTO:
    """
    Analysis result data transfer object
    """
    technical_analysis: Dict
    ai_analysis: str
    signals: List[str]
    recommendation: str
```

## 3. Infrastructure Layer

### 3.1 external_services/yahoo_finance.py
```python
import yfinance as yf
from ...application.interfaces.external.market_data import MarketDataInterface

class YahooFinance(MarketDataInterface):
    """
    Yahoo Finance API implementation
    """
    async def get_stock_data(self, symbol: str) -> Stock:
        """
        Get stock historical data
        - Download data using yfinance
        - Convert to Stock entity
        """
        pass

    async def get_real_time_price(self, symbol: str) -> Price:
        """Get real-time price"""
        pass
```

### 3.2 external_services/openai_service.py
```python
from openai import AsyncOpenAI
from ...application.interfaces.external.llm_service import LLMServiceInterface

class OpenAIService(LLMServiceInterface):
    """
    OpenAI API implementation
    """
    def __init__(self):
        self.client = AsyncOpenAI()
        self.system_prompt = self._load_system_prompt()

    async def analyze(self, 
                     technical_data: Dict, 
                     stock_data: Stock) -> str:
        """
        Execute AI analysis
        1. Prepare input data
        2. Call OpenAI API
        3. Process response
        """
        pass
```

### 3.3 config/settings.py
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings
    """
    OPENAI_API_KEY: str
    DEFAULT_TIMEFRAME: str = "1y"
    UPDATE_INTERVAL: int = 60
    TECHNICAL_INDICATORS: List[str] = [
        "SMA", "RSI", "MACD"
    ]

    class Config:
        env_file = ".env"
```

## 4. Presentation Layer

### 4.1 ui/pages/main.py
```python
import streamlit as st

def main():
    """
    Main page
    - Set page configuration
    - Initialize services
    - Handle page routing
    """
    st.set_page_config(
        page_title="Stock Analysis System",
        layout="wide"
    )
    
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    render_current_page()
```

### 4.2 ui/pages/dashboard.py
```python
class DashboardPage:
    """
    Dashboard page
    """
    def __init__(self):
        self.analysis_service = AnalysisService()

    def render(self):
        """
        Render dashboard
        Layout:
        - Top: Market overview
        - Left: Watchlist
        - Middle: Main chart
        - Right: News summary
        - Bottom: Technical indicator summary
        """
        self._render_market_overview()
        
        col1, col2, col3 = st.columns([2,5,2])
        with col1:
            self._render_watchlist()
        with col2:
            self._render_main_chart()
        with col3:
            self._render_news_feed()
            
        self._render_technical_summary()
```

### 4.3 ui/pages/stock_detail.py
```python
class StockDetailPage:
    """
    Stock detail page
    """
    def __init__(self):
        self.analysis_service = AnalysisService()
        self.price_chart = PriceChart()
        self.indicator_chart = IndicatorChart()

    def render(self):
        """
        Render stock details
        Layout:
        - Top: Stock information and controls
        - Middle: Candlestick chart
        - Bottom: Technical indicators and AI analysis
        """
        self._render_stock_header()
        self._render_charts()
        self._render_analysis()
```

### 4.4 ui/components/charts/price_chart.py
```python
import plotly.graph_objects as go

class PriceChart:
    """
    Price chart component
    """
    def render(self, stock_data: Stock):
        """
        Draw candlestick chart
        - Main chart: Candlesticks
        - Sub-chart: Volume
        - Overlay technical indicators
        """
        fig = self._create_candlestick(stock_data)
        self._add_volume(fig, stock_data)
        self._add_indicators(fig, stock_data)
        return fig
```

### 4.5 ui/components/charts/indicator_chart.py
```python
class IndicatorChart:
    """
    Indicator chart component
    """
    def render(self, indicators: Dict):
        """
        Draw technical indicator charts
        - Support multiple indicators
        - Toggleable display
        """
        pass
```

### 4.6 ui/components/widgets/stock_info.py
```python
class StockInfo:
    """
    Stock information component
    """
    def render(self, stock: Stock):
        """
        Display basic stock information
        - Current price
        - Price change percentage
        - Volume
        - Other basic information
        """
        pass
```

### 4.7 ui/components/widgets/analysis_panel.py
```python
class AnalysisPanel:
    """
    Analysis panel component
    """
    def render(self, analysis_result: AnalysisResult):
        """
        Display analysis results
        - Technical analysis summary
        - AI analysis results
        - Trading recommendations
        """
        pass
```

### 4.8 ui/components/widgets/metrics_display.py
```python
class MetricsDisplay:
    """
    Metrics display component
    """
    def render(self, metrics: Dict):
        """
        Display key metrics
        - Technical indicator values
        - Alert signals
        - Market strength
        """
        pass
```

## 5. User Interface Flow

### 5.1 Main Workflow
1. User enters dashboard
2. Selects stock symbol
3. System performs analysis
4. Displays analysis results
5. Automatically updates data

### 5.2 Update Mechanism
```python
def auto_update():
    """
    Periodic update mechanism
    """
    while True:
        update_data()
        time.sleep(settings.UPDATE_INTERVAL)
```

## 6. Development Guide

### 6.1 Environment Setup
```bash
# Create environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 6.2 Run Application
```bash
streamlit run src/presentation/ui/pages/main.py
```

### 6.3 Testing
```bash
pytest tests/
```