import plotly.graph_objects as go
import streamlit as st
from .....domain.entities.stock import Stock

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
        return st.plotly_chart(fig, use_container_width=True)
    
    def _create_candlestick(self, stock_data: Stock):
        """建立 K 線圖"""
        # 轉換數據為 plotly 可用格式
        dates = [p.timestamp for p in stock_data.prices]
        opens = [p.open for p in stock_data.prices]
        highs = [p.high for p in stock_data.prices]
        lows = [p.low for p in stock_data.prices]
        closes = [p.close for p in stock_data.prices]
        
        # 創建 K 線圖
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=dates,
            open=opens,
            high=highs,
            low=lows,
            close=closes,
            name='K線'
        ))
        
        # 設定圖表布局
        fig.update_layout(
            title=f'{stock_data.name} ({stock_data.symbol}) 價格走勢',
            xaxis_title='日期',
            yaxis_title='價格',
            xaxis_rangeslider_visible=False,
            height=500
        )
        
        return fig
    
    def _add_volume(self, fig, stock_data: Stock):
        """添加成交量圖"""
        dates = [p.timestamp for p in stock_data.prices]
        volumes = [p.volume for p in stock_data.prices]
        
        # 建立成交量子圖
        fig.add_trace(go.Bar(
            x=dates,
            y=volumes,
            name='成交量',
            marker_color='rgba(0, 0, 255, 0.5)',
            yaxis="y2"
        ))
        
        # 更新布局以包含成交量子圖
        fig.update_layout(
            yaxis2=dict(
                title="成交量",
                overlaying="y",
                side="right",
                showgrid=False
            )
        )
        
    def _add_indicators(self, fig, stock_data: Stock):
        """添加技術指標到圖表"""
        # 計算 SMA 20
        sma = stock_data.calculate_sma(period=20)
        if sma:
            dates = [p.timestamp for p in stock_data.prices][-len(sma):]
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=sma,
                mode='lines',
                name='SMA(20)',
                line=dict(color='rgba(255, 165, 0, 0.8)', width=1.5)
            ))