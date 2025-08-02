import streamlit as st

def render_chat():
    """
    Renders the chat interface, including message history and user input.
    This function does not handle the logic of getting a response, only the UI.
    """
    st.subheader("Ask a follow-up question")

    # Display chat messages from history on app rerun
    for message in st.session_state.get("messages", []):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # The chat input is returned by this function and handled in the main dashboard page
    return st.chat_input("What do you want to know about this analysis?")
