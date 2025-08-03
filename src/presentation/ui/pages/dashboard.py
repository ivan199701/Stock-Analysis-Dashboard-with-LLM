import streamlit as st
import asyncio
import nest_asyncio
from copy import deepcopy
from application.services.analysis_service import AnalysisService
from infrastructure.external_services.yahoo_finance import YahooFinance
from infrastructure.external_services.google_gemini_service import GoogleGeminiService
from presentation.ui.components.charts.price_chart import PriceChart
from presentation.ui.components.widgets.analysis_panel import AnalysisPanel
from presentation.ui.components.widgets.stock_info import StockInfo
from presentation.ui.components.widgets.chat_widget import render_chat
from application.services.chat_service import ChatService
from application.dtos.chat_dto import ChatRequest
from presentation.ui.utils.localization import get_localizer

nest_asyncio.apply()

@st.cache_data(ttl=86400)
def load_stock_data(symbol):
    try:
        market_data_service = YahooFinance()
        # Assuming get_stock_data returns an object with attributes like prices, name, symbol
        return asyncio.run(market_data_service.get_stock_data(symbol, period="5y"))
    except Exception as e:
        st.error(f"Failed to load data for {symbol}: {e}")
        return None

def get_timeframe_days(timeframe_str):
    return {"3 Months": 90, "6 Months": 180, "1 Year": 365, "5 Years": 1825}.get(timeframe_str, 365)

def render_dashboard():
    t = get_localizer()

    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'dragmode' not in st.session_state:
        st.session_state.dragmode = 'pan'

    # --- Top Controls ---
    with st.container(border=True):
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            symbol = st.text_input(t("symbol_input_label"), "", key="stock_symbol_input")
        with c2:
            timeframe = st.selectbox(t("timeframe_select_label"), options=["3 Months", "6 Months", "1 Year", "5 Years"], index=2)
        with c3:
            st.write("") 
            st.write("")
            analyze_button = st.button(t("analyze_button"), use_container_width=True)

        with st.expander("Advanced Options"):
            available_indicators = ["SMA", "EMA", "RSI", "MACD", "Bollinger Bands"]
            selected_indicators = st.multiselect(
                t("indicator_select_label"),
                options=available_indicators,
                default=["SMA", "EMA"]
            )

    # --- Analysis Logic ---
    if analyze_button and symbol:
        st.session_state.stock_data = load_stock_data(symbol)
        if st.session_state.stock_data:
            with st.spinner(f"Analyzing {symbol}..."):
                try:
                    analysis_stock_data = deepcopy(st.session_state.stock_data)
                    days_to_keep = get_timeframe_days(timeframe)
                    analysis_stock_data.prices = analysis_stock_data.prices[-days_to_keep:]
                    
                    llm_service = GoogleGeminiService()
                    analysis_service = AnalysisService(llm_service)
                    # This needs to be adapted to how indicators are actually calculated and returned
                    results = asyncio.run(analysis_service.analyze_stock(analysis_stock_data, timeframe, selected_indicators))
                    
                    st.session_state.analysis_results = results
                    st.session_state.messages = []
                    st.rerun()
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")
                    st.session_state.analysis_results = None

    # --- Display Area ---
    stock_data = st.session_state.stock_data
    analysis_results = st.session_state.analysis_results

    if stock_data:
        stock_info = StockInfo()
        stock_info.render(stock_data)
        st.divider()

        tab1, tab2 = st.tabs(["Chart", "AI Analysis & Chat"])

        with tab1:
            st.subheader("Price Chart")
            
            # Drawing tools
            c1, c2, c3, _ = st.columns([1,1,1,4])
            if c1.button("Pan/Zoom", use_container_width=True):
                st.session_state.dragmode = 'pan'
            if c2.button("Draw Trendline", use_container_width=True):
                st.session_state.dragmode = 'drawline'
            if c3.button("Draw Horizontal", use_container_width=True):
                st.session_state.dragmode = 'drawopenpath'

            # Placeholder for indicator data - this needs to be correctly populated
            indicators_data = analysis_results.indicators if analysis_results and hasattr(analysis_results, 'indicators') else {}
            
            price_chart = PriceChart(stock_data, indicators_data)
            fig = price_chart.plot(st.session_state.dragmode, selected_indicators)
            st.plotly_chart(fig, use_container_width=True, config={'scrollZoom': True})

        with tab2:
            if analysis_results:
                analysis_panel = AnalysisPanel()
                analysis_panel.render(analysis_results)
                st.divider()
                
                user_question = render_chat()
                if user_question:
                    # Placeholder for chat logic
                    pass
            else:
                st.info("Analysis results will be displayed here.")
    else:
        # Initial blank state
        price_chart = PriceChart(None, None)
        st.plotly_chart(price_chart.plot(), use_container_width=True)
        st.markdown(f"<div style='text-align: center; padding: 20px;'></div>", unsafe_allow_html=True)
