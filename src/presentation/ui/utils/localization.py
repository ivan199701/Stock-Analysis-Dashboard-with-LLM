import json
import streamlit as st
from pathlib import Path

# Path to the locales directory, going up from utils -> ui -> presentation -> src
LOCALE_DIR = Path(__file__).parent.parent.parent.parent / "locales"

@st.cache_data
def load_translation(language: str) -> dict:
    """Loads the translation file for the selected language."""
    try:
        with open(LOCALE_DIR / f"{language}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback to English if the language file doesn't exist
        with open(LOCALE_DIR / "en.json", "r", encoding="utf-8") as f:
            return json.load(f)

def get_localizer():
    """
    Initializes the localizer in the session state and returns a function
    that can be used to get translated strings.
    """
    if 'language' not in st.session_state:
        st.session_state.language = "en"  # Default language

    if 'translation' not in st.session_state or st.session_state.get('lang_changed', False):
        st.session_state.translation = load_translation(st.session_state.language)
        st.session_state.lang_changed = False

    def t(key):
        return st.session_state.translation.get(key, key)

    return t
