import streamlit as st
import requests
from google.genai import Client

# --- Set up Google Gemini API ---
try:
    api_key = st.secrets["google_gemini_api_key"]["key"]
    client = Client(api_key=api_key)
except Exception as e:
    st.error("🔑 Gemini API key not found in st.secrets. Please add it to secrets.toml.")
    st.stop()

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
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**🧑 You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**🤖 FruitBot:** {msg['content']}")

# --- Chat Input ---
user_input = st.text_input("Any more Questions About Fruits?", "")

# --- Handle user input ---
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare fruit facts (keep it short for performance)
    fruit_facts = ""
    for fruit in fruit_data[:10]:  # Limit to first 10 fruits
        name = fruit.get("name", "Unknown")
        nutrition = fruit.get("nutritions", {})
        nutrition_str = ", ".join(f"{k}: {v}" for k, v in nutrition.items())
        fruit_facts += f"{name}: {nutrition_str}\n"

    prompt = f"""
You are a helpful fruit expert bot. Based on the following fruit data, answer the user's question.

Fruit Data:
{fruit_facts}

Question: {user_input}
"""

    try:
        response = client.generate_content(prompt)
        reply = getattr(response, "text", "Sorry, I couldn't generate a response.").strip()
    except Exception as e:
        reply = f"❌ Error from Gemini: {e}"

    # Save assistant reply and clear input
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.experimental_rerun()  # Refresh to clear input
