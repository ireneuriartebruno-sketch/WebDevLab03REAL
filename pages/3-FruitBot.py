import streamlit as st
import requests
import google.generativeai as genai

st.set_page_config(page_title="FruitBot 🍓", page_icon="🍍")
st.title("🍍 FruitBot - Ask Me About Fruits!")
st.markdown("Ask anything related to fruits! Powered by [Fruityvice](https://www.fruityvice.com).")

api_key = st.secrets["key"]  # Access the key directly from Streamlit secrets
genai.configure(api_key=api_key)
client = genai.GenerativeModel("gemini-1.5-flash")

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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
st.subheader("Chat History")
for msg in st.session_state.chat_history:
    role = "🧑 You" if msg["role"] == "user" else "🤖 FruitBot"
    st.markdown(f"**{role}:** {msg['content']}")
    
user_input = st.text_area("Any more Questions About Fruits?", height=50)
    
if st.button("Send") and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    fruit_facts = "\n".join([f"{fruit['name']}: {', '.join(f'{k}: {v}' for k, v in fruit['nutritions'].items())}" 
                            for fruit in fruit_data[:10]])

    prompt = f"""
    You are a helpful fruit expert. Use the following fruit data to answer the user's question.
    
    Fruit Data:
    {fruit_facts}

    Chat History:
    {''.join([f"{m['role']}: {m['content']}\n" for m in st.session_state.chat_history])}
        
    User Question:
    {user_input}
    """
    
    try:
        response = client.generate_content(prompt)
        reply = response.text.strip()
    except Exception as e:
        reply = f"❌ Gemini error: {e}"

    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    


