import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    df = pd.read_csv('./data/Earthquakes-1990-2023.csv', engine='pyarrow')
    df.drop_duplicates(keep='first', inplace=True)

    df['date'] = pd.to_datetime(df['date'], format='mixed')
    df['time'] = pd.to_datetime(df['time'], format='mixed').dt.time
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    return df


st.title('Earthquakes 1990-2023')

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('')

st.table(data.head())
st.line_chart(data=data.groupby('year').agg({'magnitudo': 'max'}), y='magnitudo', x_label='Year', y_label='Magnitude')
