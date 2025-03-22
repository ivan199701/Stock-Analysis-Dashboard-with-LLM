import streamlit as st

def main():
    """
    主頁面
    - 設定頁面配置
    - 初始化服務
    - 處理頁面路由
    """
    st.set_page_config(
        page_title="股票分析系統",
        layout="wide"
    )
    
    if "page" not in st.session_state:
        st.session_state.page = "dashboard"

    render_current_page()
    
def render_current_page():
    """根據當前頁面狀態渲染對應頁面"""
    from .dashboard import DashboardPage
    from .stock_detail import StockDetailPage
    
    if st.session_state.page == "dashboard":
        dashboard = DashboardPage()
        dashboard.render()
    elif st.session_state.page == "stock_detail":
        stock_detail = StockDetailPage()
        stock_detail.render()
        
if __name__ == "__main__":
    main()