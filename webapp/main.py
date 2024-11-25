import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

sns.set_style('darkgrid')


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


def center_title_h5(title):
    st.html(f'<h5 align="center"> {title} </h5>')


def hist(df, bins=None, title='', x_label=None, y_label=None, log=False):
    fig, ax = plt.subplots()

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

    ax.hist(df, bins=bins, log=log)

    st.pyplot(fig)


st.title('Earthquakes 1990-2023')

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('')

st.table(data.head(10))

st.header('Plots and analysis')

st.subheader('Number of earthquake events in different states')

center_title_h5('All Earthquakes')
st.bar_chart(data['state'].value_counts().head(30), x_label='State', y_label='Number of events')

center_title_h5('Significant Earthquakes')
significant_earthquakes = data['state'][data['significance'] > data['significance'].max() // 2].value_counts()
st.bar_chart(significant_earthquakes, x_label='State', y_label='Number of events')

center_title_h5('Powerful Earthquakes')
big_magnitudo_earthquakes = data['state'][data['magnitudo'] >= 6].value_counts()
st.bar_chart(big_magnitudo_earthquakes.head(10), x_label='State', y_label='Number of events')

center_title_h5('Small Earthquakes')
small_magnitudo_earthquakes = data['state'][data['magnitudo'] <= 4].value_counts()
st.bar_chart(small_magnitudo_earthquakes.head(10), x_label='State', y_label='Number of events')

st.subheader('The number of earthquakes at all time')

center_title_h5('Earthquakes at all time')
st.bar_chart(data['year'].value_counts(sort=False), x_label='Year', y_label='Number of events')

center_title_h5('Powerful earthquakes at all time')
st.bar_chart(data['year'][data['magnitudo'] >= 6].value_counts(sort=False), x_label='Year', y_label='Number of events')

center_title_h5('Significant earthquakes at all time')
st.bar_chart(data['year'][data['significance'] >= data['significance'].max() // 4].value_counts(sort=False),
             x_label='Year',
             y_label='Number of events')

st.subheader('Distribution by magnitude, significance and depth')

hist(data['magnitudo'], bins=np.arange(-3., 10., 0.5), log=True, title='Magnitude distribution',
     x_label='Magnitude')

hist(data['significance'], bins=np.arange(0., data['significance'].max(), 50), log=True,
     title='Significance distribution', x_label='Significance')

hist(data['depth'], bins=np.arange(data['depth'].min(), data['depth'].max(), 50), log=True,
     title='Depth distribution',
     x_label='Depth')
