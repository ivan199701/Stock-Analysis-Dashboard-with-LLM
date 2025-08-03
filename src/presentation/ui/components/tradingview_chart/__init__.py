import os
import streamlit as st
from typing import List, Dict, Any

_RELEASE = True

@st.cache_resource
def get_tradingview_component():
    if not _RELEASE:
        return st.components.v1.declare_component(
            "tradingview_chart",
            url="http://localhost:3001",
        )
    else:
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        build_dir = os.path.join(parent_dir, "frontend/build")
        return st.components.v1.declare_component("tradingview_chart", path=build_dir)

def _prepare_data(stock_data) -> List[Dict[str, Any]]:
    if stock_data is None or not hasattr(stock_data, 'prices') or not isinstance(stock_data.prices, list):
        return []

    return [
        {
            "time": price.timestamp.strftime('%Y-%m-%d'),
            "open": price.open,
            "high": price.high,
            "low": price.low,
            "close": price.close,
        }
        for price in stock_data.prices
    ]

def render_tradingview_chart(stock_data, key=None):
    component_func = get_tradingview_component()
    ohlc_data = _prepare_data(stock_data) if stock_data else []
    
    component_func(
        data=ohlc_data,
        key=key,
        default=None,
    )
