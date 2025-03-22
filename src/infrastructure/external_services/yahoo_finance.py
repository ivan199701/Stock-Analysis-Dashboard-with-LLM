import yfinance as yf
from ...application.interfaces.external.market_data import MarketDataInterface
from ...domain.entities.stock import Stock
from ...domain.value_objects.price import Price

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
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1y")
        
        # 轉換數據為 Price 值物件列表
        prices = [
            Price(
                timestamp=index,
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            )
            for index, row in history.iterrows()
        ]
        
        # 建立 Stock 實體
        return Stock(
            symbol=symbol,
            name=ticker.info.get('shortName', symbol),
            prices=prices
        )

    async def get_real_time_price(self, symbol: str) -> Price:
        """獲取即時價格"""
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        
        if data.empty:
            raise ValueError(f"無法獲取股票 {symbol} 的即時價格")
        
        latest = data.iloc[-1]
        return Price(
            timestamp=data.index[-1],
            open=latest['Open'],
            high=latest['High'],
            low=latest['Low'],
            close=latest['Close'],
            volume=latest['Volume']
        )