import altair as alt
import streamlit as st

from utils import *

# Title
st.title('Interactive Graphics')

# Sidebar for user options
st.sidebar.header('Select Chart Options')
chart_type = st.sidebar.selectbox(
    'Choose chart type',
    ['Not selected', 'Pie Chart', 'Bar Chart']
)

st.sidebar.subheader('Chart Options')

feature = st.sidebar.selectbox('Feature', ['No feature', 'magnitudo', 'significance', 'depth', 'destructive'])
event_type = st.sidebar.selectbox('Event Type', ['Earthquake & Tsunami', 'Earthquake', 'Tsunami'])

chart = None

if chart_type != 'Not selected':
    data = load_data()

    if event_type == 'Earthquake':
        df = data[data['tsunami'] == 0]
    elif event_type == 'Tsunami':
        df = data[data['tsunami'] == 1]
    else:
        df = data

    if feature != 'No feature':
        threshold = st.sidebar.slider('Threshold',
                                      value=float(data[feature].mean()),
                                      min_value=float(data[feature].min()),
                                      max_value=float(data[feature].max()),
                                      step=0.1)

        df = df['state'][data[feature] >= threshold]
    else:
        df = df['state']

    df = df.value_counts().reset_index()

    states = st.sidebar.slider('Number of states', min_value=1, max_value=40, step=1, value=10)

    if chart_type == 'Bar Chart':
        chart = alt.Chart(df.head(states)).mark_bar(size=15).encode(
            x=alt.X('state', title='State'),
            y=alt.Y('count', title='Count')
        )
    elif chart_type == 'Pie Chart':
        chart = alt.Chart(df.head(states)).mark_arc().encode(
            theta=alt.Theta(field='count', type='quantitative'),
            color=alt.Color(field='state', type='nominal'),
            tooltip=['state', 'count']
        )

# Display chart
if chart is not None:
    chart = chart.properties(
        title=f'Number of {event_type} events' + (f' filtered by {feature}' if feature != 'No feature' else ''))

    st.altair_chart(chart, use_container_width=True)
else:
    st.markdown('*Choose a chart!*')
