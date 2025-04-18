import streamlit as st
import requests
import google.generativeai as genai

# --- Page Setup ---
st.set_page_config(page_title="FruitBot 🍓", page_icon="🍍")
st.title("🍍 FruitBot - Ask Me About Fruits!")
st.markdown("Ask anything related to fruits! Powered by [Fruityvice](https://www.fruityvice.com).")

# --- Load Gemini API key from secrets ---
try:
    api_key = st.secrets["google_gemini_api_key"]["key"]
    genai.configure(api_key=api_key)
    client = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error("❌ Could not load Gemini API key. Make sure it's set in .streamlit/secrets.toml")
    st.stop()

# --- Fetch Fruit Data from Fruityvice API ---
@st.cache_data
def fetch_fruit_data():
    try:
        response = requests.get("https://www.fruityvice.com/api/fruit/all")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"⚠️ Failed to fetch fruit data: {e}")
        return []

fruit_data = fetch_fruit_data()

# --- Session State for Chat ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display Chat History ---
st.subheader("🧠 Chat History")
for msg in st.session_state.chat_history:
    role = "🧑 You" if msg["role"] == "user" else "🤖 FruitBot"
    st.markdown(f"**{role}:** {msg['content']}")

# --- Input Form ---
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Any more Questions About Fruits?")
    submitted = st.form_submit_button("Send")

# --- Handle Submission ---
if submitted and user_input.strip():
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare fruit facts (limited to 10 fruits for brevity)
    fruit_facts = ""
    for fruit in fruit_data[:10]:
        name = fruit.get("name", "Unknown")
        nutrition = fruit.get("nutritions", {})
        nutrition_str = ", ".join(f"{k}: {v}" for k, v in nutrition.items())
        fruit_facts += f"{name}: {nutrition_str}\n"

    # Compose prompt
    prompt = f"""
You are a helpful fruit expert. Use the following fruit data to answer the user's question.

Fruit Data:
{fruit_facts}

User Question:
{user_input}
"""

    # Get response from Gemini
    try:
        response = model.generate_content(prompt)
        reply = response.text.strip()
    except Exception as e:
        reply = f"❌ Gemini error: {e}"

    # Save assistant reply and rerun
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.experimental_rerun()
