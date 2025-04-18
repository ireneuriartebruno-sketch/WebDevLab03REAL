import streamlit as st
import requests
import google.generativeai as genai

# --- Page Setup ---
st.set_page_config(page_title="FruitBot 🍓", page_icon="🍍")
st.title("🍍 FruitBot - Ask Me About Fruits!")
st.markdown("Ask anything related to fruits! Powered by [Fruityvice](https://www.fruityvice.com).")

# --- Configure Gemini ---
api_key = st.secrets["key"]
genai.configure(api_key=api_key)
client = genai.GenerativeModel("gemini-1.5-flash")

# --- Fetch Fruit Data ---
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

# --- Initialize session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.start_chat()

# --- Chat History Container ---
with st.container():
    for msg in st.session_state.chat_history:
        role = "🧑 You" if msg["role"] == "user" else "🤖 FruitBot"
        st.markdown(f"**{role}:** {msg['content']}")

# --- Fixed Position Input at Bottom ---
st.markdown("---")  # separator
with st.container():
    user_input = st.text_area("💬 Ask a question about fruits:", height=68, label_visibility="collapsed")

    send_button = st.button("Send", use_container_width=True)

    if send_button and user_input.strip():
        # Save user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Format fruit data
        fruit_facts = "\n".join([
            f"{fruit['name']}: {', '.join(f'{k}: {v}' for k, v in fruit['nutritions'].items())}"
            for fruit in fruit_data[:10]
        ])

        # Compose prompt
        prompt = f"""
        You are a helpful fruit expert. Use the following fruit data to answer the user's question.

        Fruit Data:
        {fruit_facts}

        Question:
        {user_input}
        """

        try:
            # Maintain conversational context
            chat = client.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.chat_history
            ])
            response = chat.send_message(prompt)
            reply = response.text.strip()
        except Exception as e:
            reply = f"❌ Gemini error: {e}"

        # Save assistant message
        st.session_state.chat_history.append({"role": "assistant", "content": reply})




    


