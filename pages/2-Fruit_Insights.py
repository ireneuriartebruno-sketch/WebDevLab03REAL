import streamlit as st
import requests
from google.genai import Client

api_key = st.secrets["google_gemini_api_key"]["key"]
client = Client(api_key = api_key)

def fetchFruitData(fruit_name):
    url = f"https://www.fruityvice.com/api/fruit/all"
    response = requests.get(url)
    data = response.json()
    fruit = next(fruit for fruit in data if fruit['name'].lower() == fruit_name.lower())
    return fruit

def generateFruitInsights(data):
    prompt = f"Generate an insightful commentary on the following fruit: {data['name']}, with the following nutritional facts: {data['nutritions']}."
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text.strip()

def generateFruitChoice(data, choice = "vacation"):
    if choice == "vacation":
        prompt = f"Envision in what type of vacation you would be eating the following fruit: {data['name']}."
    elif choice == "celebrities":
        prompt = f"Find out which worldwide celebrities like the fruit {data['name']}."
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text.strip()

fruit_emoji = {
    "Apple": "🍎",
    "Banana": "🍌",
    "Mango": "🥭",
    "Orange": "🍊"
}

fruit_name = st.text_input("Write any fruit here!", "Apple")
fruit_emoji_icon = fruit_emoji.get(fruit_name, "🍏")
data = fetchFruitData(fruit_name)

if fruit_name:
    st.markdown(f"### {fruit_emoji_icon} Fruit Information {fruit_emoji_icon}")
    st.write("Here are some AI-Provided insightful commentary:")
    insights = generateFruitInsights(data)
    st.write(insights)

st.write("---")
st.write("Choose an option below to get even more information!")

choice = st.radio("What would you like to learn about this fruit?", ("What type of vacation fits with this fruit?", "Which worldwide celebrities like this fruit?"))
if choice:
    if choice == "What type of vacation fits with this fruit?":
        st.write("Here are the vacation insights:")
        insights_vacation = generateFruitChoice(data, choice="vacation")
        st.write(insights_vacation)
    elif choice == "Which worldwide celebrities like this fruit?":
        st.write("Here are the celebrity insights:")
        insights_celebrities = generateFruitChoice(data, choice="celebrities")
        st.write(insights_celebrities)


