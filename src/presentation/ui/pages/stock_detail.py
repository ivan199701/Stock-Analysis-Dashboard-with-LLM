import streamlit as st
from ....application.services.analysis_service import AnalysisService
from ..components.charts.price_chart import PriceChart
from ..components.charts.indicator_chart import IndicatorChart
from ..components.widgets.stock_info import StockInfo
from ..components.widgets.analysis_panel import AnalysisPanel

class StockDetailPage:
    """
    股票詳情頁面
    """
    def __init__(self):
        self.analysis_service = AnalysisService()
        self.price_chart = PriceChart()
        self.indicator_chart = IndicatorChart()
        self.stock_info = StockInfo()
        self.analysis_panel = AnalysisPanel()

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
        
    def _render_stock_header(self):
        """渲染股票頭部資訊"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.button("返回儀表板", on_click=self._back_to_dashboard)
            
        with col2:
            if "selected_stock" in st.session_state:
                st.header(f"股票詳情: {st.session_state.selected_stock}")
            else:
                st.header("股票詳情")
                st.warning("未選擇股票，請返回儀表板選擇股票")
                return
                
        with col3:
            timeframes = ["1D", "5D", "1M", "3M", "6M", "1Y", "5Y"]
            selected_timeframe = st.selectbox(
                "時間範圍", 
                timeframes,
                index=timeframes.index("1M")
            )
            
    def _render_charts(self):
        """渲染圖表區域"""
        if "selected_stock" not in st.session_state:
            return
            
        # 假設我們已經獲取了股票數據
        symbol = st.session_state.selected_stock
        
        # 這個應該是非同步的，但為了示範先使用同步方式
        try:
            with st.spinner(f"正在分析 {symbol}..."):
                # 實際應用中，這裡應該調用 self.analysis_service.analyze_stock(symbol)
                # 但為了示範，我們先使用假數據
                stock_data = None  # 假設這是從服務獲取的數據
                
                # 渲染 K 線圖
                st.subheader("價格走勢")
                # 假設的圖表
                chart_placeholder = st.empty()
                with chart_placeholder.container():
                    st.line_chart({"data": [50, 45, 55, 50, 60, 65, 55, 60, 70, 75]})
                
                # 渲染技術指標圖
                st.subheader("技術指標")
                indicators_placeholder = st.empty()
                with indicators_placeholder.container():
                    tab1, tab2, tab3 = st.tabs(["SMA", "RSI", "MACD"])
                    with tab1:
                        st.line_chart({"SMA(20)": [48, 46, 47, 49, 51, 53, 52, 55, 58, 60]})
                    with tab2:
                        st.line_chart({"RSI": [60, 55, 65, 50, 70, 75, 60, 65, 80, 70]})
                    with tab3:
                        st.line_chart({
                            "MACD": [2, 1.8, 2.2, 1.5, 1.8, 2.5, 1.8, 2.2, 2.8, 2.5],
                            "Signal": [1.8, 1.9, 2.0, 1.8, 1.7, 2.0, 2.1, 2.2, 2.3, 2.4]
                        })
        except Exception as e:
            st.error(f"分析時發生錯誤: {str(e)}")
        
    def _render_analysis(self):
        """渲染分析結果區域"""
        if "selected_stock" not in st.session_state:
            return
            
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("技術分析")
            st.write("""
            ### 趨勢分析
            - **短期(5-10天)**: 上漲趨勢
            - **中期(10-30天)**: 盤整
            - **長期(30+天)**: 溫和上漲
            
            ### 支撐和阻力位
            - **支撐位**: 530、510、490
            - **阻力位**: 580、600、620
            """)
            
        with col2:
            st.subheader("AI 分析")
            st.info("""
            根據技術指標和價格模式分析，該股票正處於一個關鍵的技術水平。
            
            1. RSI 已從超賣區回升，但尚未進入超買區域，有進一步上漲空間。
            2. MACD 指標顯示動能正在增強，柱狀圖正在擴大。
            3. 支撐位在近期低點附近得到確認。
            4. 成交量在上漲日增加，在下跌日減少，是積極信號。
            
            **建議**: 可考慮在回調至支撐位時進行買入，設置止損在支撐位下方。短期目標價可設在最近阻力位。
            """)
            
        # 交易信號區域
        st.subheader("交易信號")
        signal_col1, signal_col2, signal_col3, signal_col4 = st.columns(4)
        
        with signal_col1:
            st.metric("RSI", "65", "5")
        with signal_col2:
            st.metric("MACD", "Bullish", "2.1")
        with signal_col3:
            st.metric("趨勢", "上漲", "")
        with signal_col4:
            st.metric("建議", "買入", "")
        
    def _back_to_dashboard(self):
        """返回儀表板"""
        st.session_state.page = "dashboard"