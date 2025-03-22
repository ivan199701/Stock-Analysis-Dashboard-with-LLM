import streamlit as st
from .....domain.entities.stock import Stock

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
        if not stock or not stock.prices:
            st.warning("無股票數據可顯示")
            return
            
        latest_price = stock.prices[-1] if stock.prices else None
        prev_price = stock.prices[-2] if len(stock.prices) > 1 else None
        
        # 計算漲跌幅
        change = 0
        change_percent = 0
        if latest_price and prev_price:
            change = latest_price.close - prev_price.close
            change_percent = (change / prev_price.close) * 100
            
        # 顯示基本信息
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label=f"{stock.name} ({stock.symbol})",
                value=f"{latest_price.close:.2f}" if latest_price else "N/A",
                delta=f"{change:.2f} ({change_percent:.2f}%)" if latest_price and prev_price else "N/A"
            )
            
        with col2:
            st.metric(
                label="成交量",
                value=f"{latest_price.volume:,}" if latest_price else "N/A"
            )
            
        # 更多詳細信息
        with st.expander("更多詳細信息"):
            if latest_price:
                details_col1, details_col2, details_col3, details_col4 = st.columns(4)
                with details_col1:
                    st.write("**開盤價**")
                    st.write(f"{latest_price.open:.2f}")
                with details_col2:
                    st.write("**最高價**")
                    st.write(f"{latest_price.high:.2f}")
                with details_col3:
                    st.write("**最低價**")
                    st.write(f"{latest_price.low:.2f}")
                with details_col4:
                    st.write("**收盤價**")
                    st.write(f"{latest_price.close:.2f}")
                    
                # 計算當天漲幅
                today_change = latest_price.calculate_change()
                st.write(f"**當日漲跌幅**: {today_change:.2f}%")