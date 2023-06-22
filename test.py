from embedchain import App as ECApp
import openai
import streamlit as st
from streamlit_chat import message


bible = ECApp()



def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():

    with st.sidebar:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    st.title("NT - Bible GPT (by Rodrigo)")
    #openai.api_key = st.secrets.openai_api_key
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    with st.form("chat_input", clear_on_submit=True):
        a, b = st.columns([4, 1])
        user_input = a.text_input(
            label="Your message:",
            placeholder="What would you like to ask?",
            label_visibility="collapsed",
        )
        b.form_submit_button("Send", use_container_width=True)

    for msg in st.session_state.messages:
        message(msg["content"], is_user=msg["role"] == "user")

    if user_input and not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        
    if user_input and openai_api_key:
        openai.api_key = openai_api_key
        st.session_state.messages.append({"role": "user", "content": user_input})
        message(user_input, is_user=True)
        messages=st.session_state.messages
        response = bible.query(user_input)
        msg = response
        st.session_state.messages.append(msg)
        message(msg.content)