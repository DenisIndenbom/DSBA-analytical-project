import plotly.express as px
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

__all__ = ['load_data', 'center_title_h5', 'hist', 'pie']

sns.set_style('darkgrid')


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv('./data/Earthquakes-1990-2023.csv', engine='pyarrow')
    df.drop_duplicates(keep='first', inplace=True)

    df['date'] = pd.to_datetime(df['date'], format='mixed')
    df['time'] = pd.to_datetime(df['time'], format='mixed').dt.time
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    df['destructive'] = df['magnitudo'].apply(lambda x:np.log10(max(1, x))) * df['significance']

    return df


def center_title_h5(title: str) -> None:
    st.html(f'<h5 align="center"> {title} </h5>')


def hist(df, bins: float = None, title: str = '', log: bool = False) -> None:
    fig = px.histogram(df, nbins=bins, log_y=log)

    fig.update_layout(title=title, showlegend=True)

    st.plotly_chart(fig)


def pie(df, title: str = '') -> None:
    fig = px.pie(df, values=df.values.tolist(), names=df.index.tolist(), title=title)

    fig.update_layout(title=title, showlegend=True)

    st.plotly_chart(fig)
