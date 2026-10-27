import logging
import os

from dotenv import load_dotenv
from groq import APIConnectionError, APIError, APIStatusError, RateLimitError
import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError
from langchain_groq import ChatGroq


load_dotenv()

st.set_page_config(
    page_title="Chatbot",
    page_icon="🤖",
    layout="centered",
)
st.title("💬ALLTechSoft Generative AI Chatbot")

api_key = (os.getenv("GROQ_API_KEY") or "").strip()
if not api_key:
    try:
        secret_api_key = st.secrets.get("GROQ_API_KEY")
    except StreamlitSecretNotFoundError:
        secret_api_key = None

    if isinstance(secret_api_key, str):
        api_key = secret_api_key.strip()
    elif secret_api_key is not None:
        st.error("GROQ_API_KEY must be configured as a string.")
        st.stop()

if not api_key:
    st.error(
        "Groq API key is missing. Set GROQ_API_KEY in your .env file "
        "or configure it in Streamlit secrets."
    )
    st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.0,
    api_key=api_key,
)

user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    try:
        with st.spinner("Waiting for a response..."):
            response = llm.invoke(
                input=[
                    {"role": "system", "content": "You are a helpful assistant"},
                    *st.session_state.chat_history,
                ]
            )
    except RateLimitError:
        logging.exception("Groq rate limit reached")
        st.error("Groq's rate limit has been reached. Please wait a moment and try again.")
    except APIConnectionError:
        logging.exception("Could not connect to the Groq API")
        st.error("Could not connect to Groq. Check your connection and try again.")
    except APIStatusError as error:
        logging.exception("Groq API returned HTTP %s", error.status_code)
        st.error(f"Groq returned an error (HTTP {error.status_code}). Please try again later.")
    except APIError:
        logging.exception("Groq API request failed")
        st.error("The request to Groq failed. Please try again later.")
    else:
        assistant_response = response.content
        st.session_state.chat_history.append(
            {"role": "assistant", "content": assistant_response}
        )

        with st.chat_message("assistant"):
            st.markdown(assistant_response)
