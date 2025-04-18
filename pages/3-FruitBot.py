import streamlit as st
import requests
import google.generativeai

# --- Set Page Info ---
st.set_page_config(page_title="FruitBot 🍓", page_icon="🍍")
st.title("🍍 FruitBot - Ask Me About Fruits!")

# --- Load Gemini API Key from Secrets ---
try:
    api_key = st.secrets["google_gemini_api_key"]["key"]
    client = Client(api_key=api_key)
except Exception as e:
    st.error("❌ Could not load Gemini API key. Make sure it's set in .streamlit/secrets.toml")
    st.stop()

# --- Fetch Fruit Data ---
@st.cache
def fetch_fruit_data():
    try:
        url = "https://www.fruityvice.com/api/fruit/all"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"⚠️ Could not fetch fruit data: {e}")
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
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Prepare context (limited for performance)
    fruit_facts = ""
    for fruit in fruit_data[:10]:  # Limit to 10 fruits
        name = fruit.get("name", "Unknown")
        nutrition = fruit.get("nutritions", {})
        nutrition_str = ", ".join(f"{k}: {v}" for k, v in nutrition.items())
        fruit_facts += f"{name}: {nutrition_str}\n"

    # Prompt to Gemini
    prompt = f"""
You are a helpful fruit expert. Use the following fruit data to answer the user's question.

Fruit Data:
{fruit_facts}

User Question:
{user_input}
"""

    # Get Gemini response
    try:
        response = client.generate_content(prompt)
        reply = getattr(response, "text", "Sorry, I couldn't generate a response.").strip()
    except Exception as e:
        reply = f"❌ Error from Gemini: {e}"

    # Add Gemini reply to history and rerun
    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.experimental_rerun()
