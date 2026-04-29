import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from backend.services.dataset_service import ask_model

st.set_page_config(page_title="Recipe Generator", page_icon="🧑🏻‍🍳")

st.title("Recipe Generator")


user_profile = st.session_state.get("user_profile", {})
profile_allergies = user_profile.get("allergies", "")
budget = user_profile.get("budget", None)
health_goals = user_profile.get("health_goals", "")
cooking_level = user_profile.get("cooking_level", "")
people_amount = user_profile.get("people_amount", 1)

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
            reply = ask_model(
                chat_history=st.session_state.messages,
                budget=budget,                       
                user_input = prompt, 
                nutrition_priority=True,            
                dietary_restrictions=profile_allergies,   
                health_goals=health_goals,           
                cooking_level=cooking_level,         
                people_amount=people_amount)
            st.markdown(reply)

    # save ai response
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )