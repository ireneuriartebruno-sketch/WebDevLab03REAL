import streamlit as st
import requests
import google.generativeai

# Page setup
st.set_page_config(page_title="Fruit Test", page_icon="🍓")
st.title("🍍 Hello from FruitBot!")

# API test
@st.cache
def get_fruits():
    try:
        response = requests.get("https://www.fruityvice.com/api/fruit/all")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return []

fruit_data = get_fruits()

# Show fruit names
if fruit_data:
    st.subheader("Fruits Available:")
    for fruit in fruit_data[:5]:
        st.write(fruit.get("name"))
else:
    st.warning("No fruit data available.")

# Basic input
question = st.text_input("Ask a fruit question:")
if question:
    st.write(f"You asked: {question}")
    st.write("🍉 I'll answer once Gemini is set up.")
