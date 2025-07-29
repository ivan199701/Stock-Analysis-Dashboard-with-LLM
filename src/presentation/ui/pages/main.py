import streamlit as st
from streamlit_option_menu import option_menu
from presentation.ui.pages.dashboard import render_dashboard
from presentation.ui.pages.about import render_about_page
from presentation.ui.utils.localization import get_localizer

def main():
    t = get_localizer()

    st.set_page_config(
        page_title=t("app_title"),
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    with st.sidebar:
        st.title("📈 " + t("app_title"))
        
        # Language Selector
        def on_lang_change():
            st.session_state.lang_changed = True

        lang = st.selectbox(
            "Language / 語言",
            options=["en", "zh_TW"],
            format_func=lambda x: "English" if x == "en" else "繁體中文",
            key='language',
            on_change=on_lang_change
        )

        page = option_menu(
            menu_title=None,
            options=[t("nav_dashboard"), t("nav_about")],
            icons=["house", "info-circle"],
            menu_icon="cast",
            default_index=0,
        )

    if page == t("nav_dashboard"):
        render_dashboard()
    elif page == t("nav_about"):
        render_about_page()

if __name__ == "__main__":
    main()