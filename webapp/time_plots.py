import plotly.express as px
import streamlit as st

from utils import load_data

# Title
st.title('Interactive Graphics')

# Sidebar for user options
st.sidebar.header('Select Chart Options')
chart_type = st.sidebar.selectbox(
    'Choose chart type',
    ['Not selected', 'Line Chart', 'Bar Chart']
)

fig = None

# Conditional input fields for chart-specific options
if chart_type == 'Line Chart':
    data = load_data()

    st.sidebar.subheader('Common Options')
    y_axis = st.sidebar.selectbox('Choose Y-axis', ['magnitudo', 'significance', 'depth', 'destructive'])

    st.sidebar.subheader('Line Chart Options')
    agg_function = st.sidebar.selectbox('Aggregate functions', ['mean', 'median', 'max'])
    df = data.groupby('year').agg({y_axis: agg_function}).reset_index()

    fig = px.line(
        df,
        x='year',
        y=y_axis,
        title=f'Trend of {agg_function} {y_axis}',
        labels={'year': 'Year', y_axis: y_axis}
    )

elif chart_type == 'Bar Chart':
    data = load_data()

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

    fig = px.bar(
        df,
        x='year',
        y='count',
        title=f"Number of earthquake events" + (f" filtered by {feature}" if feature != 'No feature' else ''),
        labels={'year': 'Year', 'count': 'Count'}
    )

    fig.update_traces(width=0.8)

# Display chart
if fig is not None:
    st.plotly_chart(fig, use_container_width=True)
else:
    st.markdown('*Choose a chart!*')
