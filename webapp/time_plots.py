import altair as alt
import streamlit as st

from utils import *

# Title
st.title('Interactive Graphics')

# Sidebar for user options
st.sidebar.header('Select Chart Options')
chart_type = st.sidebar.selectbox(
    'Choose chart type',
    ['Not selected', 'Line Chart', 'Bar Chart']
)

data = load_data()

chart = None

# Conditional input fields for chart-specific options
if chart_type == 'Line Chart':
    st.sidebar.subheader('Common Options')
    y_axis = st.sidebar.selectbox('Choose Y-axis', ['magnitudo', 'significance', 'depth', 'destructive'])

    st.sidebar.subheader('Line Chart Options')
    agg_function = st.sidebar.selectbox('Aggregate functions', ['mean', 'median', 'max'])
    df = data.groupby('year').agg({y_axis: agg_function}).reset_index()

    chart = alt.Chart(df).mark_line().encode(
        x=alt.X('year', title='Year'),
        y=alt.Y(y_axis, title=y_axis)
    ).properties(title=f'Trend of {agg_function} {y_axis}')

elif chart_type == 'Bar Chart':
    st.sidebar.subheader('Bar Chart Options')

    feature = st.sidebar.selectbox('Feature', ['No feature', 'magnitudo', 'significance', 'depth', 'destructive'])

    if feature != 'No feature':
        threshold = st.sidebar.slider('Threshold',
                                      value=float(data[feature].mean()),
                                      min_value=float(data[feature].min()),
                                      max_value=float(data[feature].max()),
                                      step=0.1)

        df = data['year'][data[feature] >= threshold].value_counts(sort=False).reset_index()
    else:
        df = data['year'].value_counts(sort=False).reset_index()

    chart = alt.Chart(df).mark_bar(size=15).encode(
        x=alt.X('year', title='Year'),
        y=alt.Y('count', title='Count')
    ).properties(title=f'Number of earthquake events' + (f' filtered by {feature}' if feature != 'No feature' else ''))

# Display chart
if chart is not None:
    st.altair_chart(chart, use_container_width=True)
else:
    st.markdown('*Choose a chart!*')
