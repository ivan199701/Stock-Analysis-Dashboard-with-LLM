import streamlit as st
from .....domain.value_objects.analysis_result import AnalysisResult

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
        if not analysis_result:
            st.warning("無分析結果可顯示")
            return
            
        # 顯示趨勢和強度
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**趨勢**: {analysis_result.trend}")
        with col2:
            st.write(f"**強度**: {self._format_strength(analysis_result.strength)}")
        
        # 顯示支撐和阻力位
        st.subheader("價格水平")
        levels_col1, levels_col2 = st.columns(2)
        
        with levels_col1:
            st.write("**支撐位**")
            if analysis_result.support_levels:
                for level in analysis_result.support_levels:
                    st.write(f"- {level:.2f}")
            else:
                st.write("無支撐位數據")
                
        with levels_col2:
            st.write("**阻力位**")
            if analysis_result.resistance_levels:
                for level in analysis_result.resistance_levels:
                    st.write(f"- {level:.2f}")
            else:
                st.write("無阻力位數據")
        
        # 顯示交易訊號
        st.subheader("交易訊號")
        if analysis_result.signals:
            for signal in analysis_result.signals:
                self._render_signal(signal)
        else:
            st.write("無交易訊號")
            
        # 顯示建議
        st.subheader("交易建議")
        self._render_recommendation(analysis_result.recommendation)
    
    def _format_strength(self, strength: float) -> str:
        """格式化強度顯示"""
        if strength >= 0.8:
            return f"很強 ({strength:.2f})"
        elif strength >= 0.6:
            return f"強 ({strength:.2f})"
        elif strength >= 0.4:
            return f"中等 ({strength:.2f})"
        elif strength >= 0.2:
            return f"弱 ({strength:.2f})"
        else:
            return f"很弱 ({strength:.2f})"
            
    def _render_signal(self, signal: str):
        """渲染交易訊號"""
        if "買入" in signal or "看多" in signal:
            st.success(f"📈 {signal}")
        elif "賣出" in signal or "看空" in signal:
            st.error(f"📉 {signal}")
        else:
            st.info(f"📊 {signal}")
            
    def _render_recommendation(self, recommendation: str):
        """渲染交易建議"""
        if "買入" in recommendation or "看多" in recommendation:
            st.success(recommendation)
        elif "賣出" in recommendation or "看空" in recommendation:
            st.error(recommendation)
        elif "持有" in recommendation:
            st.info(recommendation)
        else:
            st.write(recommendation)