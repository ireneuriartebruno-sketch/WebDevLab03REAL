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
@st.cache_data
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

# --- Chat Input ---
user_input = st.chat_input("Any more Questions About Fruits?")

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display previous messages ---
for entry in st.session_state.chat_history:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

# --- Handle user question ---
if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare the prompt with fruit data
    fruit_facts = "\n".join([f"{fruit['name']}: {fruit['nutritions']}" for fruit in fruit_data])
    prompt = f"""You are a helpful fruit expert bot. Based on the following data about fruits, answer the user's question.

Fruit Data:
{fruit_facts}

Question: {user_input}
"""

    # Get response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.generate_content(prompt)
                reply = response.text.strip()
            except Exception as e:
                reply = f"❌ Error fetching response: {e}"
            st.markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
