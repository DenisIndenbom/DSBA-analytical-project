import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px

__all__ = ['load_data', 'center_title_h5', 'hist', 'pie']

sns.set_style('darkgrid')


@st.cache_data
def load_data() -> pd.DataFrame:
    """
        Load and preprocess earthquake data from a CSV file.

        The function reads a CSV file containing earthquake data, removes duplicates, and adds additional columns:
        - `date`: Parsed datetime column for the earthquake date.
        - `time`: Parsed time component of the `time` column.
        - `year`, `month`, `day`: Extracted components from the `date` column.
        - `destructive`: A computed value based on earthquake magnitude and significance.

        Returns:
            pd.DataFrame: A preprocessed DataFrame with additional columns.
    """
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
    """
       Display a centered H5 HTML title in a Streamlit app.

       Args:
           title (str): The title text to display.
    """
    st.html(f'<h5 align="center"> {title} </h5>')


def hist(series, bins: int = 10, title: str = '', log: bool = False) -> None:
    """
    Display a histogram of the data using Plotly in a Streamlit app.

    Args:
        series (pd.Series): The Series containing the data to plot.
        bins (int, optional): Number of bins for the histogram. Defaults to 10.
        title (str, optional): Title of the histogram. Defaults to an empty string.
        log (bool, optional): Whether to use a logarithmic scale for the y-axis. Defaults to False.

    Returns:
        None
    """
    fig = px.histogram(
        pd.DataFrame({'values':series}),
        x='values',
        nbins=bins,
        title=title,
        log_y=log
    )

    fig.update_layout(bargap=0.2, xaxis_title=series.name, yaxis_title='Frequency')

    st.plotly_chart(fig, use_container_width=True)


def pie(df, categories_field, values_field, title: str = '') -> None:
    """
    Display a pie chart of the data using Plotly in a Streamlit app.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to plot. It should have a field for categories and a field for values.
        categories_field (str): The field containing the categories to plot.
        values_field (str): The field containing the values to plot.
        title (str, optional): Title of the pie chart. Defaults to an empty string.

    Returns:
        None: The function directly renders the plot in the Streamlit app.
    """
    fig = px.pie(
        df,
        names=categories_field,
        values=values_field,
        title=title
    )

    st.plotly_chart(fig, use_container_width=True)
