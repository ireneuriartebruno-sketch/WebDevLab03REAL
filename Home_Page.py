import streamlit as st

# Title of App
st.title("Web Development Lab03")

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("CS 1301")
st.subheader("Team 60, Web Development - Section A")
st.subheader("FruitWise: Choose the Healthy Lifestyle")
st.subheader("Irene Uriarte, Matthew Townsend")

st.image("Images/fruit.jpg", use_container_width=True)

# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description
#       4. **Page Name**: Description

st.markdown("""
<span style="color:#339af0">
Welcome to our Streamlit Web Development Lab03 app! You can navigate between the pages using the sidebar to the left. The following pages are:</span>
""", unsafe_allow_html=True)


st.write("""
1. Fruit Explorer: Learn everything there is to know about a specific fruit!
2. Fruit Insights: AI-generated commentary on a fruit
3. FruitBot: Ask the FruitBot for specific questions! 

""")

