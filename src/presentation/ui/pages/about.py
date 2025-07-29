import streamlit as st
from presentation.ui.utils.localization import get_localizer

def render_about_page():
    t = get_localizer()
    st.title(t("about_title"))

    st.header(t("about_how_to_use"))
    st.markdown(t("about_how_to_use_steps"))

    st.header(t("about_indicators_header"))
    st.markdown(t("about_indicators_intro"))

    with st.expander(t("indicator_ma_name")):
        st.markdown(t("indicator_ma_desc"))

    with st.expander(t("indicator_rsi_name")):
        st.markdown(t("indicator_rsi_desc"))

    with st.expander(t("indicator_macd_name")):
        st.markdown(t("indicator_macd_desc"))

    with st.expander(t("indicator_bb_name")):
        st.markdown(t("indicator_bb_desc"))

    with st.expander(t("indicator_stoch_name")):
        st.markdown(t("indicator_stoch_desc"))

    with st.expander(t("indicator_atr_name")):
        st.markdown(t("indicator_atr_desc"))

    with st.expander(t("indicator_obv_name")):
        st.markdown(t("indicator_obv_desc"))

