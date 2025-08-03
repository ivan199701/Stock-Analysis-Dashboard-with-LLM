import streamlit as st
import asyncio
import nest_asyncio
from domain.entities.stock import Stock
from copy import deepcopy

nest_asyncio.apply()

from application.services.analysis_service import AnalysisService
from infrastructure.external_services.yahoo_finance import YahooFinance
from infrastructure.external_services.google_gemini_service import GoogleGeminiService
from presentation.ui.components.charts.price_chart import PriceChart
from presentation.ui.components.widgets.analysis_panel import AnalysisPanel
from presentation.ui.components.widgets.stock_info import StockInfo
from presentation.ui.components.widgets.chat_widget import render_chat
from presentation.ui.components.tradingview_chart import render_tradingview_chart
from application.services.chat_service import ChatService
from application.dtos.chat_dto import ChatRequest
from presentation.ui.utils.localization import get_localizer

@st.cache_data(ttl=86400)
def load_stock_data(symbol):
    try:
        market_data_service = YahooFinance()
        return asyncio.run(market_data_service.get_stock_data(symbol, period="5y"))
    except Exception as e:
        st.error(f"Failed to load data for {symbol}: {e}")
        return None

def get_timeframe_days(timeframe_str):
    return {"3 Months": 90, "6 Months": 180, "1 Year": 365, "5 Years": 1825}.get(timeframe_str, 365)

def initialize_ui_components():
    if 'price_chart' not in st.session_state:
        st.session_state.price_chart = PriceChart()
    if 'analysis_panel' not in st.session_state:
        st.session_state.analysis_panel = AnalysisPanel()
    if 'stock_info' not in st.session_state:
        st.session_state.stock_info = StockInfo()

def render_dashboard():
    t = get_localizer()
    initialize_ui_components()

    # Initialize chat state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # --- Top Controls ---
    with st.container(border=True):
        # Row 1: Main controls
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            symbol = st.text_input(t("symbol_input_label"), "", key="stock_symbol_input")
        with c2:
            timeframe = st.selectbox(t("timeframe_select_label"), options=["3 Months", "6 Months", "1 Year", "5 Years"], index=2)
        with c3:
            st.write("") # Spacer
            st.write("") # Spacer
            analyze_button = st.button(t("analyze_button"), use_container_width=True)

        # Row 2: Secondary controls (collapsible)
        with st.expander("Advanced Options"):
            available_indicators = ["SMA", "EMA", "RSI", "MACD", "Bollinger Bands", "Stochastic", "ATR", "OBV"]
            selected_indicators = st.multiselect(
                t("indicator_select_label"),
                options=available_indicators,
                default=["SMA", "EMA", "Bollinger Bands"]
            )

    # --- Main Dashboard Area ---
    if 'stock_data' not in st.session_state:
        st.session_state.stock_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None

    # Instantiate services once
    llm_service = GoogleGeminiService()
    analysis_service = AnalysisService(llm_service)

    # --- Easter Egg Logic ---
    if symbol.lower() == "laaaaaa":
        st.balloons()
        st.image("src/presentation/ui/assets/alpaca.jpeg", caption="You found the secret alpaca!")
        st.stop()

    if analyze_button and symbol:
        st.session_state.stock_data = load_stock_data(symbol)
        if st.session_state.stock_data:
            with st.spinner(f"Analyzing {symbol}..."):
                try:
                    analysis_stock_data = deepcopy(st.session_state.stock_data)
                    days_to_keep = get_timeframe_days(timeframe)
                    analysis_stock_data.prices = analysis_stock_data.prices[-days_to_keep:]
                    
                    results = asyncio.run(analysis_service.analyze_stock(analysis_stock_data, timeframe, selected_indicators))
                    st.session_state.analysis_results = results
                    st.session_state.messages = []  # Reset chat on new analysis
                except Exception as e:
                    st.error(f"An error occurred during analysis: {e}")
                    st.session_state.analysis_results = None
    
    if st.session_state.stock_data:
        stock_data = st.session_state.stock_data
        analysis_results = st.session_state.analysis_results
        
        st.session_state.stock_info.render(stock_data)
        st.divider()

        tab1, tab2 = st.tabs(["Chart", "AI Analysis & Chat"])

        with tab1:
            render_tradingview_chart(stock_data, key="tv_chart")

        with tab2:
            if analysis_results:
                st.session_state.analysis_panel.render(analysis_results)
                st.divider()

                # --- Chat Section ---
                user_question = render_chat()

                if user_question:
                    st.session_state.messages.append({"role": "user", "content": user_question})
                    
                    with st.spinner("Thinking..."):
                        try:
                            chat_service = ChatService(llm_service)
                            request_dto = ChatRequest(
                                stock_analysis=analysis_results.ai_analysis,
                                chat_history=st.session_state.messages,
                                user_question=user_question
                            )
                            response_dto = asyncio.run(chat_service.get_response(request_dto))
                            assistant_response = response_dto.assistant_response
                            
                            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                            st.rerun()

                        except Exception as e:
                            st.error(f"An error occurred in the chat: {e}")
            else:
                st.info("Analysis results will be displayed here.")
    else:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 50px;">
                <h2>{t("welcome_header")}</h2>
                <p>{t("welcome_message")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_tradingview_chart(None, key="blank_tv_chart")