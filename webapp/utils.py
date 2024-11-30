import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

__all__ = ['load_data', 'center_title_h5', 'hist', 'pie']

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

    df['destructive'] = df['magnitudo'].apply(lambda x:np.log10(max(1, x))) * df['significance']

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


def pie(df, title=''):
    fig, ax = plt.subplots()

    plt.title(title)

    ax.pie(df, labels=df.index.tolist())

    st.pyplot(fig)
