import openai
import streamlit as st
import requests

api_key = st.secrets["key"]
openai.api_key = api_key

def fetchFruitData(fruit_name):
    url = f"https://www.fruityvice.com/api/fruit/all"
    response = requests.get(url)
    return response.json()

def generateFruitInsights(data):
    prompt = f"Generate an insightful commentary on the following fruit: {data['name']}, with the following nutritional facts: {data['nutritional_info']}."
    response = openai.Completion.create(engine="gpt-4", prompt=prompt, max_tokens=200)
    return response.choices[0].text.strip()

fruit_name = st.text_input("Enter the fruit name", "Apple")
data = fetchFruitData(fruit_name)
insights = generateFruitInsights(data)
st.write("AI=generated Insights:")
st.write(insights)


