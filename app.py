import streamlit as st
import requests
import uuid

st.title("Chatbot with Groq API")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")

if st.button("Send") and user_input:
    response = requests.post("http://localhost:8000/chat/", json={
        "session_id": st.session_state.session_id,
        "message": user_input
    })
    if response.status_code == 200:
        reply = response.json()["response"]
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", reply))
    else:
        st.error("Error communicating with the chatbot API.")

for role, text in st.session_state.chat_history:
    st.write(f"**{role}:** {text}")
