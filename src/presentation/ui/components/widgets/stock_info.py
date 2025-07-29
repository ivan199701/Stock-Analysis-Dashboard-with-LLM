import streamlit as st
from domain.entities.stock import Stock

class StockInfo:
    def render(self, stock_data: Stock):
        if not stock_data.prices:
            st.warning("No price data available to display stock info.")
            return

        latest_price = stock_data.prices[-1]
        previous_price = stock_data.prices[-2] if len(stock_data.prices) > 1 else latest_price

        change = latest_price.close - previous_price.close
        change_percent = (change / previous_price.close) * 100 if previous_price.close != 0 else 0

        st.header(f"{stock_data.name} ({stock_data.symbol})")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Last Close", f"${latest_price.close:.2f}", f"{change:.2f} ({change_percent:.2f}%)")
        col2.metric("Volume", f"{latest_price.volume:,}")
        col3.metric("Day Range", f"${latest_price.low:.2f} - ${latest_price.high:.2f}")
