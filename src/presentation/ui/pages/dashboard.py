import streamlit as st
from ....application.services.analysis_service import AnalysisService

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
        
    def _render_market_overview(self):
        """渲染市場概況"""
        st.header("市場概況")
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        with metrics_col1:
            st.metric(label="台股大盤", value="18,000", delta="120")
        with metrics_col2:
            st.metric(label="恆生指數", value="16,500", delta="-230")
        with metrics_col3:
            st.metric(label="道瓊指數", value="38,780", delta="450")
        with metrics_col4:
            st.metric(label="納斯達克", value="16,340", delta="220")
            
    def _render_watchlist(self):
        """渲染觀察清單"""
        st.subheader("觀察清單")
        if "watchlist" not in st.session_state:
            st.session_state.watchlist = ["2330.TW", "2317.TW", "2454.TW"]
            
        # 顯示觀察清單
        for symbol in st.session_state.watchlist:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.button(symbol, key=f"btn_{symbol}", 
                          on_click=self._view_stock_detail, args=(symbol,))
            with col2:
                st.write("...")
                
        # 新增股票
        with st.form("add_stock_form", clear_on_submit=True):
            new_symbol = st.text_input("新增股票")
            submitted = st.form_submit_button("新增")
            if submitted and new_symbol:
                if new_symbol not in st.session_state.watchlist:
                    st.session_state.watchlist.append(new_symbol)
                    st.rerun()
        
    def _render_main_chart(self):
        """渲染主要圖表區域"""
        st.subheader("大盤走勢")
        # 這裡只是一個佔位符，實際應用中應該顯示真實圖表
        st.line_chart({"data": [10, 20, 30, 40, 50, 40, 30, 20, 50, 60]})
        
    def _render_news_feed(self):
        """渲染新聞摘要"""
        st.subheader("市場新聞")
        
        news_items = [
            "台積電擴大投資計劃，砸2000億擴充先進製程產能",
            "鴻海宣布進軍電動車市場，攜手國際大廠共同開發",
            "聯發科新一代旗艦晶片發布，效能超越同級對手20%",
            "美股科技股續創新高，帶動台股相關族群表現",
            "央行宣布維持利率不變，經濟前景保持審慎樂觀"
        ]
        
        for news in news_items:
            st.write(f"- {news}")
            
    def _render_technical_summary(self):
        """渲染技術指標摘要"""
        st.subheader("技術指標摘要")
        
        summary_col1, summary_col2 = st.columns(2)
        with summary_col1:
            st.write("### 強勢股票")
            st.write("- 台積電 (2330.TW): 多頭趨勢")
            st.write("- 緯創 (3231.TW): 突破壓力線")
            st.write("- 聯發科 (2454.TW): 量價齊揚")
            
        with summary_col2:
            st.write("### 弱勢股票")
            st.write("- 聯電 (2303.TW): 跌破支撐")
            st.write("- 鴻海 (2317.TW): 量縮下跌")
            st.write("- 日月光 (3711.TW): 頭肩頂形態確認")
            
    def _view_stock_detail(self, symbol):
        """切換到股票詳情頁面"""
        st.session_state.selected_stock = symbol
        st.session_state.page = "stock_detail"