import streamlit as st
import requests
import google.generativeai as genai

# --- Page Setup ---
st.set_page_config(page_title="FruitBot 🍓", page_icon="🍍")
st.title("🍍 FruitBot - Ask Me About Fruits!")
st.markdown("Ask anything related to fruits! Powered by [Fruityvice](https://www.fruityvice.com).")

# --- Load Gemini API key from secrets ---
api_key = st.secrets["key"]
genai.configure(api_key=api_key)
client = genai.GenerativeModel("gemini-1.5-flash")

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

# --- Display Chat History above the input form ---
st.subheader("🧠 Chat History")
for msg in st.session_state.chat_history:
    role = "🧑 You" if msg["role"] == "user" else "🤖 FruitBot"
    st.markdown(f"**{role}:** {msg['content']}")

# --- Create an empty container for the input box (this keeps it at the bottom) ---
with st.container():
    # Input form (bottom of the page)
    user_input = st.text_input("Any more Questions About Fruits?", key="input_box")
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Prepare fruit facts
        fruit_facts = "\n".join([f"{fruit['name']}: {', '.join(f'{k}: {v}' for k, v in fruit['nutritions'].items())}" 
                                for fruit in fruit_data[:10]])

        # Compose prompt for Gemini
        prompt = f"""
        You are a helpful fruit expert. Use the following fruit data to answer the user's question.
        
        Fruit Data:
        {fruit_facts}
        
        User Question:
        {user_input}
        """

        # Get response from Gemini
        try:
            response = client.generate_content(prompt)
            reply = response.text.strip()
        except Exception as e:
            reply = f"❌ Gemini error: {e}"

        # Add assistant's reply to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        # Force the page to rerun and show the updated messages
        st.experimental_rerun()
