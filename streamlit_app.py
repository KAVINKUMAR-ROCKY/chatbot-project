import streamlit as st
import openai

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"]

st.set_page_config(page_title="AI Chatbot", layout="centered")
st.title("🤖 AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi! How can I help you today?"}]

# Display chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Text input
user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    # Show user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state["messages"].append({"role": "user", "content": user_prompt})

    # Get response from OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state["messages"]
        )
        reply = response['choices'][0]['message']['content']
        st.session_state["messages"].append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)
    except Exception as e:
        st.error(f"OpenAI error: {e}")
