import streamlit as st
import openai

# ✅ Load API key securely from Streamlit secrets
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.error("❌ OPENAI_API_KEY not found in secrets. Please add it in Streamlit Cloud > Settings > Secrets.")
    st.stop()

st.set_page_config(page_title="Chatbot", layout="centered")
st.title("🤖 AI Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

# Display chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input from user
user_input = st.chat_input("Type your message...")

if user_input:
    # Display user's message
    st.chat_message("user").markdown(user_input)
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Call OpenAI API
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
        st.error(f"⚠️ OpenAI API error: {e}")
