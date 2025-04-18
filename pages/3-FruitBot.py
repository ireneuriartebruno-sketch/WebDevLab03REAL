import streamlit as st
import requests
from google.genai import Client

# --- Set up Google Gemini API ---
api_key = st.secrets["google_gemini_api_key"]["key"]
client = Client(api_key=api_key)

# --- Page Setup ---
st.set_page_config(page_title="FruitBot", page_icon="🍓")
st.title("🍍 Ask Me About Fruits!")
st.markdown("Ask anything related to fruits! Data is powered by [Fruityvice](https://www.fruityvice.com).")

# --- Fetch fruit data from API ---
@st.cache
def get_fruit_data():
    url = "https://www.fruityvice.com/api/fruit/all"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch fruit data: {e}")
        return []

fruit_data = get_fruit_data()

# --- Session State Initialization ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display previous messages ---
st.subheader("Chat History")
for entry in st.session_state.chat_history:
    if entry["role"] == "user":
        st.markdown(f"**You:** {entry['content']}")
    else:
        st.markdown(f"**FruitBot:** {entry['content']}")

# --- Chat Input ---
user_input = st.text_input("Any more Questions About Fruits?", key="user_input")

# --- Handle user input ---
if user_input:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare fruit facts string
    fruit_facts = "\n".join([f"{fruit['name']}: {fruit['nutritions']}" for fruit in fruit_data])

    # Prompt for Gemini
    prompt = f"""
You are a helpful fruit expert bot. Based on the following data about fruits, answer the user's question.

Fruit Data:
{fruit_facts}

Question: {user_input}
"""

    # Call Gemini API
    try:
        response = client.generate_content(prompt)
        reply = response.text.strip()
    except Exception as e:
        reply = f"❌ Error fetching response: {e}"

    # Add reply to history and clear input
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.experimental_rerun()
