import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

from application.interfaces.external.market_data import MarketDataInterface
from domain.entities.stock import Stock
from domain.value_objects.price import Price
from infrastructure.utils.retry_decorator import async_retry

class YahooFinance(MarketDataInterface):

    @async_retry()
    async def get_stock_data(self, symbol: str, period: str = "1y") -> Stock:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                raise ValueError(f"No data found for symbol {symbol}")

            prices = [
                Price(
                    timestamp=index.to_pydatetime(),
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close'],
                    volume=row['Volume']
                )
                for index, row in hist.iterrows()
            ]
            
            stock_info = ticker.info
            stock_name = stock_info.get('longName', symbol)

            return Stock(symbol=symbol, name=stock_name, prices=prices)
        except Exception as e:
            # This allows the retry decorator to catch the exception
            raise e

    @async_retry()
    async def get_real_time_price(self, symbol: str) -> Price:
        try:
            ticker = yf.Ticker(symbol)
            # Get data for the last 2 minutes to ensure we get the latest price
            data = ticker.history(period="1d", interval="1m")
            
            if data.empty:
                raise ValueError(f"Could not fetch real-time price for {symbol}")

            latest = data.iloc[-1]
            return Price(
                timestamp=latest.name.to_pydatetime(),
                open=latest['Open'],
                high=latest['High'],
                low=latest['Low'],
                close=latest['Close'],
                volume=latest['Volume']
            )
        except Exception as e:
            raise e
