import streamlit as st
import requests
import google.generativeai as genai

st.set_page_config(page_title="FruitBot 🍓", page_icon="🍍")
st.title("🍍 FruitBot - Ask Me About Fruits!")
st.markdown("Ask anything related to fruits! Powered by [Fruityvice](https://www.fruityvice.com).")

api_key = st.secrets["key"]  
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




    
user_input = st.text_area("Any more Questions About Fruits?", height=68)
if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.start_chat()
if st.button("Send") and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    fruit_facts = "\n".join([f"{fruit['name']}: {', '.join(f'{k}: {v}' for k, v in fruit['nutritions'].items())}" 
                             
for fruit in fruit_data[:10]])

    prompt = f"""
    You are a helpful fruit expert. Use the following fruit data to answer the user's question.
    Fruit Data: {fruit_facts}
    User Question: {user_input}
    """
    try: 
        chat = client.start_chat(history=[{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.chat_history])
        response = chat.send_message(prompt)
        reply = response.text.strip()
    except Exception as e:
        reply = f"❌ Gemini error: {e}"
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

st.subheader("Chat History")

with st.container():
    html = """
    <style>
        .chat-box {
            height: 300px;
            overflow-y: auto;
            display: flex;
            flex-direction: column-reverse;
            border: 1px solid #ccc;
            border-radius: 6px;
            padding: 10px;
            background-color: #f9f9f9;
        }
        .chat-message {
            margin-bottom: 10px;
        }
        .user { color: #333; }
        .bot { color: #1a73e8; }
    </style>
    <div class="chat-box">
    """

    for msg in reversed(st.session_state.chat_history):
        role = "🧑 You" if msg["role"] == "user" else "🤖 FruitBot"
        css_class = "user" if msg["role"] == "user" else "bot"
        html += f"""
        <div class="chat-message {css_class}">
            <strong>{role}:</strong> {msg['content']}
        </div>
        """

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    


