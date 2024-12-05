import plotly.express as px
import streamlit as st

from utils import load_data

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

fig = None

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
        fig = px.bar(
            df.head(states),
            x='state',
            y='count',
            labels={'state': 'State', 'count': 'Count'}
        )

        fig.update_traces(width=0.8)
    elif chart_type == 'Pie Chart':
        fig = px.pie(
            df.head(states),
            names='state',
            values='count',
        )

# Display chart
if fig is not None:
    fig = fig.update_layout(
        title=f'Number of {event_type} events' + (f' filtered by {feature}' if feature != 'No feature' else ''))

    st.plotly_chart(fig, use_container_width=True)
else:
    st.markdown('*Choose a chart!*')
