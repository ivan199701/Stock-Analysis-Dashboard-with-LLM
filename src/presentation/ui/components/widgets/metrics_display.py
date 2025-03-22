import streamlit as st
from typing import Dict

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
        if not metrics:
            st.warning("無指標數據可顯示")
            return
            
        # 顯示主要技術指標
        st.subheader("技術指標摘要")
        
        # 從指標數據中獲取最新值
        rsi = self._get_latest_value(metrics.get('rsi', []))
        macd = self._get_latest_value(metrics.get('macd', {}).get('macd', []))
        signal = self._get_latest_value(metrics.get('macd', {}).get('signal', []))
        
        # 使用 st.metric 顯示指標值
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if rsi is not None:
                self._render_rsi_metric(rsi)
            else:
                st.metric("RSI", "N/A")
                
        with col2:
            if macd is not None and signal is not None:
                macd_status = "看多" if macd > signal else "看空"
                macd_delta = macd - signal
                st.metric("MACD", macd_status, f"{macd_delta:.2f}")
            else:
                st.metric("MACD", "N/A")
                
        with col3:
            trend = metrics.get('trend', 'N/A')
            st.metric("趨勢", trend)
        
        # 警示訊號
        self._render_alerts(metrics)
    
    def _get_latest_value(self, data_list):
        """獲取列表中最後一個值"""
        if data_list and len(data_list) > 0:
            return data_list[-1]
        return None
        
    def _render_rsi_metric(self, rsi_value):
        """渲染 RSI 指標"""
        # 根據 RSI 值判斷狀態
        if rsi_value > 70:
            status = "超買"
            delta_color = "inverse"  # 紅色，超買是負面信號
        elif rsi_value < 30:
            status = "超賣"
            delta_color = "normal"   # 綠色，超賣是正面信號
        else:
            status = "中性"
            delta_color = "off"      # 灰色，中性沒有明顯信號
            
        # 顯示 RSI 值和狀態
        st.metric(
            label="RSI", 
            value=f"{rsi_value:.0f}",
            delta=status,
            delta_color=delta_color
        )
        
    def _render_alerts(self, metrics):
        """渲染警示訊號"""
        alerts = metrics.get('alerts', [])
        
        if alerts:
            st.subheader("警示訊號")
            
            for alert in alerts:
                if "危險" in alert or "賣出" in alert:
                    st.error(alert)
                elif "機會" in alert or "買入" in alert:
                    st.success(alert)
                else:
                    st.info(alert)
        else:
            # 如果沒有提供警示，根據指標狀態創建一些基本警示
            rsi = self._get_latest_value(metrics.get('rsi', []))
            macd = self._get_latest_value(metrics.get('macd', {}).get('macd', []))
            signal = self._get_latest_value(metrics.get('macd', {}).get('signal', []))
            
            alerts_generated = []
            
            if rsi is not None:
                if rsi > 70:
                    alerts_generated.append("RSI 處於超買區間，可能即將回落")
                elif rsi < 30:
                    alerts_generated.append("RSI 處於超賣區間，可能出現反彈")
                    
            if macd is not None and signal is not None:
                if macd > signal and abs(macd - signal) > 0.1:
                    alerts_generated.append("MACD 金叉，可能是買入信號")
                elif macd < signal and abs(macd - signal) > 0.1:
                    alerts_generated.append("MACD 死叉，可能是賣出信號")
            
            if alerts_generated:
                st.subheader("系統生成警示")
                for alert in alerts_generated:
                    if "買入" in alert:
                        st.success(alert)
                    elif "賣出" in alert:
                        st.error(alert)
                    else:
                        st.info(alert)