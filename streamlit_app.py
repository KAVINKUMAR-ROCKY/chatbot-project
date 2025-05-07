import streamlit as st
from openai import OpenAI
import os

# ✅ Create OpenAI client (new v1+ way)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Chatbot", layout="centered")
st.title("🤖 AI Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! How can I help you today?"}]

# Display past messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})

    try:
        # ✅ Call OpenAI using the new client
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["messages"]
        )
        reply = response.choices[0].message.content
        st.session_state["messages"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as e:
        st.error(f"⚠️ OpenAI API error: {e}")
