import streamlit as st

with open('README.md', 'r', encoding='utf-16le') as file:
    readme = file.read()

st.markdown(readme, unsafe_allow_html=False)
