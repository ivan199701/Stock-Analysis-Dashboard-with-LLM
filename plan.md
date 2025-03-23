# 股票分析系統開發計畫書 - 詳細檔案說明

## 1. Domain Layer

### 1.1 aggregates/stock_analysis.py
```python
from dataclasses import dataclass
from typing import List, Dict

class StockAnalysis:
    """
    股票分析的聚合根，整合所有分析結果
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
```

### 1.2 entities/stock.py
```python
@dataclass
class Stock:
    """
    股票實體類別
    """
    symbol: str
    name: str
    prices: List[Price]
    
    def calculate_sma(self, period: int = 20) -> List[float]:
        """計算簡單移動平均"""
        pass

    def calculate_rsi(self, period: int = 14) -> List[float]:
        """計算RSI"""
        pass

    def calculate_macd(self) -> Dict[str, List[float]]:
        """計算MACD"""
        pass
```

### 1.3 value_objects/price.py
```python
@dataclass(frozen=True)
class Price:
    """
    價格值物件
    """
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    def calculate_change(self) -> float:
        """計算漲跌幅"""
        return (self.close - self.open) / self.open * 100
```

### 1.4 value_objects/timeframe.py
```python
@dataclass(frozen=True)
class TimeFrame:
    """
    時間範圍值物件
    """
    start: datetime
    end: datetime

    def duration_days(self) -> int:
        """計算天數"""
        return (self.end - self.start).days

    def is_valid(self) -> bool:
        """檢查時間範圍是否有效"""
        return self.start < self.end
```

### 1.5 value_objects/analysis_result.py
```python
@dataclass(frozen=True)
class AnalysisResult:
    """
    分析結果值物件
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
```

### 2.2 interfaces/external/market_data.py
```python
from abc import ABC, abstractmethod

class MarketDataInterface(ABC):
    """
    市場數據介面定義
    """
    @abstractmethod
    async def get_stock_data(self, symbol: str) -> Stock:
        """獲取股票數據"""
        pass

    @abstractmethod
    async def get_real_time_price(self, symbol: str) -> Price:
        """獲取即時價格"""
        pass
```

### 2.3 interfaces/external/llm_service.py
```python
from abc import ABC, abstractmethod

class LLMServiceInterface(ABC):
    """
    LLM 服務介面定義
    """
    @abstractmethod
    async def analyze(self, 
                     technical_data: Dict, 
                     stock_data: Stock) -> str:
        """執行 AI 分析"""
        pass
```

### 2.4 dtos/stock_dto.py
```python
@dataclass
class StockDTO:
    """
    股票資料傳輸物件
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
    分析結果傳輸物件
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
    Yahoo Finance API 實現
    """
    async def get_stock_data(self, symbol: str) -> Stock:
        """
        獲取股票歷史數據
        - 使用 yfinance 下載數據
        - 轉換為 Stock 實體
        """
        pass

    async def get_real_time_price(self, symbol: str) -> Price:
        """獲取即時價格"""
        pass
```

### 3.2 external_services/openai_service.py
```python
from openai import AsyncOpenAI
from ...application.interfaces.external.llm_service import LLMServiceInterface

class OpenAIService(LLMServiceInterface):
    """
    OpenAI API 實現
    """
    def __init__(self):
        self.client = AsyncOpenAI()
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
        pass
```

### 3.3 config/settings.py
```python
from pydantic_settings import BaseSettings

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
```

## 4. Presentation Layer

### 4.1 ui/pages/main.py
```python
import streamlit as st

def main():
    """
    主頁面
    - 設定頁面配置
    - 初始化服務
    - 處理頁面路由
    """
    st.set_page_config(
        page_title="股票分析系統",
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
    儀表板頁面
    """
    def __init__(self):
        self.analysis_service = AnalysisService()

    def render(self):
        """
        渲染儀表板
        布局：
        - 頂部：市場概況
        - 左側：觀察清單
        - 中間：主要圖表
        - 右側：新聞摘要
        - 底部：技術指標摘要
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
    股票詳情頁面
    """
    def __init__(self):
        self.analysis_service = AnalysisService()
        self.price_chart = PriceChart()
        self.indicator_chart = IndicatorChart()

    def render(self):
        """
        渲染股票詳情
        布局：
        - 頂部：股票資訊和控制項
        - 中間：K線圖
        - 下方：技術指標和 AI 分析
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
    價格圖表元件
    """
    def render(self, stock_data: Stock):
        """
        繪製 K 線圖
        - 主圖：K線
        - 副圖：成交量
        - 疊加技術指標
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
    指標圖表元件
    """
    def render(self, indicators: Dict):
        """
        繪製技術指標圖
        - 支援多個指標
        - 可切換顯示
        """
        pass
```

### 4.6 ui/components/widgets/stock_info.py
```python
class StockInfo:
    """
    股票資訊元件
    """
    def render(self, stock: Stock):
        """
        顯示股票基本資訊
        - 當前價格
        - 漲跌幅
        - 成交量
        - 其他基本資訊
        """
        pass
```

### 4.7 ui/components/widgets/analysis_panel.py
```python
class AnalysisPanel:
    """
    分析面板元件
    """
    def render(self, analysis_result: AnalysisResult):
        """
        顯示分析結果
        - 技術分析摘要
        - AI 分析結果
        - 交易建議
        """
        pass
```

### 4.8 ui/components/widgets/metrics_display.py
```python
class MetricsDisplay:
    """
    指標顯示元件
    """
    def render(self, metrics: Dict):
        """
        顯示關鍵指標
        - 技術指標值
        - 警示訊號
        - 市場強弱
        """
        pass
```

## 5. 使用者介面流程

### 5.1 主要工作流程
1. 使用者進入儀表板
2. 選擇股票代碼
3. 系統執行分析
4. 顯示分析結果
5. 自動更新數據

### 5.2 更新機制
```python
def auto_update():
    """
    定期更新機制
    """
    while True:
        update_data()
        time.sleep(settings.UPDATE_INTERVAL)
```

## 6. 開發指南

### 6.1 環境設置
```bash
# 建立環境
python -m venv venv
source venv/bin/activate

# 安裝依賴
pip install -r requirements.txt
```

### 6.2 運行應用
```bash
streamlit run src/presentation/ui/pages/main.py
```

### 6.3 測試
```bash
pytest tests/
```