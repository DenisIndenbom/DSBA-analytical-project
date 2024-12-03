import altair as alt
import streamlit as st

from utils import *

# Title
st.title('Interactive Graphics')

# Sidebar for user options
st.sidebar.header('Select Chart Options')
chart_type = st.sidebar.selectbox(
    'Choose chart type',
    ['Line Chart', 'Bar Chart', 'Scatter Plot']
)

data = load_data()

# Common customization options
st.sidebar.subheader('Common Options')
y_axis = st.sidebar.selectbox('Choose Y-axis', ['magnitudo'])

chart = None

# Conditional input fields for chart-specific options
if chart_type == 'Line Chart':
    st.sidebar.subheader("Line Chart Options")
    agg_function = st.sidebar.selectbox('Aggregate functions', ['mean', 'median', 'max'])
    df = data.groupby('year').agg({y_axis: agg_function})

    chart = alt.Chart(df).mark_line().encode(x='year', y=y_axis)

# elif chart_type == 'Bar Chart':
#     st.sidebar.subheader('Bar Chart Options')
#     bar_width = st.sidebar.slider('Bar Width', 0.2, 1.0, 0.5)
#
#     chart = alt.Chart(data).mark_bar(size=bar_width * 50).encode(
#         x=alt.X('x:O', title=x_axis_label),
#         y=alt.Y('y', title=y_axis_label),
#         color='category'
#     ).properties(title=title)
#
# elif chart_type == 'Scatter Plot':
#     st.sidebar.subheader('Scatter Plot Options')
#     size_by_value = st.sidebar.checkbox('Size by Value', value=False)
#
#     chart = alt.Chart(data).mark_circle().encode(
#         x=alt.X('x', title=x_axis_label),
#         y=alt.Y('y', title=y_axis_label),
#         size='y' if size_by_value else alt.value(60),
#         color='category'
#     ).properties(title=title)

# Display chart
st.altair_chart(chart, use_container_width=True)

st.write('Done!')
