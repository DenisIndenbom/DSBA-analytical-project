import streamlit as st

from config import ABOUT_PATH

with open(ABOUT_PATH, 'r', encoding='utf-16le') as file:
    readme = file.read()

st.markdown(readme, unsafe_allow_html=False)
