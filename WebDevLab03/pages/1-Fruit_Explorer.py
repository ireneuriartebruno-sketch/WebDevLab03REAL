import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

response = requests.get("https://www.fruityvice.com/api/fruit/all")
data = response.json()

fruitName = [fruit["name"] for fruit in data]

selectedFruit = st.selectbox("Choose a fruit:", fruitName)

fruitInfo = next(fruit for fruit in data if fruit["name"] == selectedFruit)

emoji_map = {
    "Apple": "🍎", "Banana": "🍌", "Strawberry": "🍓", "Orange": "🍊", 
    "Lemon": "🍋", "Grapes": "🍇", "Mango": "🥭", "Pineapple": "🍍"
}
emoji = emoji_map.get(selectedFruit, "🍉")

st.markdown(f"<h1 style='text-align: center;'>{emoji} {selectedFruit} {emoji}</h1>", unsafe_allow_html=True)


st.subheader(f"Nutrition Facts for {selectedFruit}")
st.write(f"Genus: {fruitInfo['genus']}")
st.write(f"Family: {fruitInfo['family']}")
st.write(f"Order: {fruitInfo['order']}")
nutrients = fruitInfo["nutritions"]


labels = nutrients.keys()
sizes = nutrients.values()
colors= ['#f94144', '#f3722c', '#f9844a', '#43aa8b', '#577590']

fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=colors)
ax.axis('equal')
st.pyplot(fig)

if st.checkbox("Show full fruit data"):
    st.json(fruitInfo)

st.write("---")
st.subheader("Find fruits by sugar content")

target_sugar = st.slider("Select sugar level (g)", 0, 30, 5)
filtered_fruits = [fruit for fruit in data if round(fruit["nutritions"]["sugar"]) == target_sugar]

filtered_names = [fruit["name"] for fruit in filtered_fruits]
st.write(f"{len(filtered_names)} fruits have exactly {target_sugar}g of sugar:")

if filtered_names:
    with st.expander(f"Show {len(filtered_names)} fruits with exactly {target_sugar}g of sugar"):
        for name in filtered_names:
            st.markdown(f"- {name}")
else:
    st.info("No fruits found with that exact sugar level.")



fruit2 = st.selectbox("Compare with another fruit:", [f for f in fruitName if f != selectedFruit])
fruitInfo2 = next(f for f in data if f["name"] == fruit2)

nut1 = fruitInfo["nutritions"]
nut2 = fruitInfo2["nutritions"]

comparisonInfo = pd.DataFrame({
    selectedFruit: nut1,
    fruit2: nut2
})
st.markdown(f"#### 🍒 Comparing {selectedFruit} vs {fruit2}")
st.table(comparisonInfo)


