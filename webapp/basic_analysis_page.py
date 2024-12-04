import streamlit as st

from utils import load_data, center_title_h5, hist

st.title('Earthquakes 1990-2023')

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('')

st.dataframe(data.head(100), use_container_width=True)

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

center_title_h5('Magnitude distribution')
hist(data['magnitudo'].reset_index(), 'magnitudo', bins=20, log=True)

center_title_h5('Significance distribution')
hist(data['significance'].reset_index(), 'significance', bins=50, log=True)

center_title_h5('Depth distribution')
hist(data['depth'].reset_index(), 'depth', bins=50, log=True)

st.subheader('The trend of the quantile (80%) over time')

center_title_h5('Quantile trend of magnitude')
st.line_chart(data.groupby('year').agg({'magnitudo':lambda x:x.quantile(0.8)}), x_label='Year', y_label='Magnitudo')

center_title_h5('Quantile trend of significance')
st.line_chart(data.groupby('year').agg({'significance':lambda x:x.quantile(0.8)}), x_label='Year',
              y_label='Significance')

center_title_h5('Quantile trend of depth')
st.line_chart(data.groupby('year').agg({'depth':lambda x:x.quantile(0.8)}), x_label='Year', y_label='Depth')

st.subheader('The trend of the maximal value over time')

center_title_h5('Max trend of magnitude')
st.line_chart(data.groupby('year').agg({'magnitudo':'max'}, x_label='Year', y_label='Magnitudo'))

center_title_h5('Max trend of significance')
st.line_chart(data.groupby('year').agg({'significance':'max'}), x_label='Year',
              y_label='Significance')

center_title_h5('Max trend of depth')
st.line_chart(data.groupby('year').agg({'depth':'max'}), x_label='Year', y_label='Depth')
