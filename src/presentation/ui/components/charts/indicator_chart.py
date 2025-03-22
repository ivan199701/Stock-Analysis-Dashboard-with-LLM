import plotly.graph_objects as go
import streamlit as st
from typing import Dict, List
import pandas as pd
from plotly.subplots import make_subplots

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
        # 創建選項卡以顯示不同指標
        tabs = st.tabs(["RSI", "MACD", "移動平均線"])
        
        with tabs[0]:
            if 'rsi' in indicators:
                self._render_rsi_chart(indicators['rsi'])
            else:
                st.info("RSI 數據不可用")
                
        with tabs[1]:
            if 'macd' in indicators:
                self._render_macd_chart(indicators['macd'])
            else:
                st.info("MACD 數據不可用")
                
        with tabs[2]:
            if 'sma' in indicators:
                self._render_ma_chart(indicators)
            else:
                st.info("移動平均線數據不可用")
    
    def _render_rsi_chart(self, rsi_data: List[float]):
        """渲染 RSI 圖表"""
        # 創建 dataframe 以便於繪圖
        df = pd.DataFrame({
            'RSI': rsi_data,
            'index': range(len(rsi_data))
        })
        
        fig = go.Figure()
        
        # 添加 RSI 線
        fig.add_trace(go.Scatter(
            x=df['index'], 
            y=df['RSI'],
            mode='lines',
            name='RSI',
            line=dict(color='blue', width=1.5)
        ))
        
        # 添加超買和超賣線
        fig.add_hline(y=70, line_dash="dash", line_color="red", 
                      annotation_text="超買區域", annotation_position="top right")
        fig.add_hline(y=30, line_dash="dash", line_color="green", 
                      annotation_text="超賣區域", annotation_position="bottom right")
        
        # 更新布局
        fig.update_layout(
            title='相對強弱指數 (RSI)',
            xaxis_title='時間',
            yaxis_title='RSI 值',
            yaxis=dict(range=[0, 100]),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    def _render_macd_chart(self, macd_data: Dict[str, List[float]]):
        """渲染 MACD 圖表"""
        macd = macd_data.get('macd', [])
        signal = macd_data.get('signal', [])
        histogram = macd_data.get('histogram', [])
        
        if not macd or not signal:
            st.info("缺少 MACD 數據")
            return
        
        # 創建 dataframe
        df = pd.DataFrame({
            'MACD': macd,
            'Signal': signal,
            'Histogram': histogram if histogram else [m - s for m, s in zip(macd, signal)],
            'index': range(len(macd))
        })
        
        # 創建帶有子圖的圖表
        fig = make_subplots(rows=1, cols=1)
        
        # 添加 MACD 線
        fig.add_trace(go.Scatter(
            x=df['index'], 
            y=df['MACD'],
            mode='lines',
            name='MACD',
            line=dict(color='blue', width=1.5)
        ))
        
        # 添加信號線
        fig.add_trace(go.Scatter(
            x=df['index'], 
            y=df['Signal'],
            mode='lines',
            name='Signal',
            line=dict(color='red', width=1.5)
        ))
        
        # 添加柱狀圖
        colors = ['red' if h < 0 else 'green' for h in df['Histogram']]
        fig.add_trace(go.Bar(
            x=df['index'], 
            y=df['Histogram'],
            name='Histogram',
            marker_color=colors
        ))
        
        # 更新布局
        fig.update_layout(
            title='MACD 指標',
            xaxis_title='時間',
            yaxis_title='值',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    def _render_ma_chart(self, indicators: Dict):
        """渲染移動平均線圖表"""
        sma_data = indicators.get('sma', {})
        
        if not sma_data:
            st.info("移動平均線數據不可用")
            return
            
        # 取得不同週期的 SMA 數據
        sma_periods = {}
        for key, value in sma_data.items():
            if isinstance(key, int):  # 如果鍵是整數，表示 SMA 週期
                sma_periods[key] = value
            elif key.startswith('sma') and key[3:].isdigit():
                period = int(key[3:])  # 例如從 'sma20' 提取 20
                sma_periods[period] = value
                
        if not sma_periods:
            # 如果是單一列表，假定為 SMA20
            if isinstance(sma_data, list):
                sma_periods[20] = sma_data
            else:
                st.info("無法識別的移動平均線數據格式")
                return
                
        # 創建圖表
        fig = go.Figure()
        colors = ['blue', 'red', 'green', 'purple', 'orange', 'cyan']
        color_idx = 0
        
        for period, data in sma_periods.items():
            fig.add_trace(go.Scatter(
                x=list(range(len(data))), 
                y=data,
                mode='lines',
                name=f'SMA({period})',
                line=dict(color=colors[color_idx % len(colors)], width=1.5)
            ))
            color_idx += 1
        
        # 更新布局
        fig.update_layout(
            title='移動平均線指標',
            xaxis_title='時間',
            yaxis_title='價格',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)