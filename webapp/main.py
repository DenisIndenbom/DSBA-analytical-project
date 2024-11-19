import pandas as pd
import streamlit as st


@st.cache_data
def load_data(nrows=None):
    return pd.read_csv('../data/Earthquakes-1990-2023.csv', nrows=nrows)


st.title('Earthquakes 1990-2023')

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text('')

st.table(data.head())
