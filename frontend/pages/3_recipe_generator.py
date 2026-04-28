import streamlit as st
from backend.services.dataset_service import ask_kimi
import streamlit as st

st.set_page_config(page_title="Recipe Generation", page_icon="‼️")

st.title("Recipe Generation")

# store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# input box
prompt = st.chat_input("Type a message...")

if prompt:
    # save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # get ai response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = ask_kimi(prompt, st.session_state.messages)
            st.markdown(reply)

    # save ai response
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )