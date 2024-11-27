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

    df['destructive'] = df['magnitudo'].apply(lambda x: np.log10(max(1, x))) * df['significance']

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

st.subheader('The trend of the quantile (80%) over time')

center_title_h5('Quantile trend of magnitude')
st.line_chart(data.groupby('year').agg({'magnitudo': lambda x: x.quantile(0.8)}), x_label='Year', y_label='Magnitudo')

center_title_h5('Quantile trend of significance')
st.line_chart(data.groupby('year').agg({'significance': lambda x: x.quantile(0.8)}), x_label='Year',
              y_label='Significance')

center_title_h5('Quantile trend of depth')
st.line_chart(data.groupby('year').agg({'depth': lambda x: x.quantile(0.8)}), x_label='Year', y_label='Depth')

st.subheader('The trend of the maximal value over time')

center_title_h5('Max trend of magnitude')
st.line_chart(data.groupby('year').agg({'magnitudo': 'max'}, x_label='Year', y_label='Magnitudo'))

center_title_h5('Max trend of significance')
st.line_chart(data.groupby('year').agg({'significance': 'max'}), x_label='Year',
              y_label='Significance')

center_title_h5('Max trend of depth')
st.line_chart(data.groupby('year').agg({'depth': 'max'}), x_label='Year', y_label='Depth')

st.header('Hypothesis')
st.markdown('**Tsunamis are more destructive than earthquakes.**')
st.markdown("""**Destructive definition**

$destructive = \\log(\\max(1, magnitudo))*significance$""")

st.subheader('Analysis')

center_title_h5('Mean of destructive')
st.bar_chart(data.groupby('tsunami').agg({'destructive': 'mean'}), x_label='Tsunami', y_label='Destructive')
st.markdown('*As we can see, on average tsunami is more destructive than ordinary earthquakes.*')

center_title_h5('Quantile (50%) of destructive')
st.bar_chart(data.groupby('tsunami').agg({'destructive': lambda x: x.quantile(0.5)}), x_label='Tsunami',
             y_label='Destructive')
st.markdown(
    '*Here we see, 50 percent of tsunamis are more destructive than earthquakes. Also, we see that destructive of 50 '
    'percent of earthquakes less than 50 points.*')

center_title_h5('Quantile (90%) of destructive')
st.bar_chart(data.groupby('tsunami').agg({'destructive': lambda x: x.quantile(0.9)}), x_label='Tsunami',
             y_label='Destructive')
st.markdown('*In this case, the 10 percent of tsunamis are more destructive than earthquakes*')

center_title_h5('Maximal value of destructive')
st.bar_chart(data.groupby('tsunami').agg({'destructive': 'max'}), x_label='Tsunami', y_label='Destructive')
st.markdown(
    '*The most destructive of the recorded tsunamis was more powerful than the most destructive of the recorded '
    'earthquakes.*')

st.subheader('Some statistics for conclusion')

tsunami = data[data['tsunami'] == 1]

pie(tsunami['state'].value_counts().head(15), title='The number of tsunamis in different states')
pie(tsunami[tsunami['destructive'] >= tsunami['destructive'].mean()]['state'].value_counts().head(15),
    title='The number of significance tsunamis in different states')
pie(tsunami[tsunami['destructive'] >= tsunami['destructive'].max() // 2]['state'].value_counts().head(15),
    title='The number of destructive tsunamis in different states')

st.markdown("""
## Hypothesis has been proved

**Why?**

- The most destructive earthquake was a tsunami. $\triangle max=63.2$ (**Maximal value of destructive** plot) - The 
average tsunami is more destructive than the average earthquake. (**Mean of destructive** plot) - The 90 percent of 
tsunamis are more destructive than the 10 percent of earthquakes. (**Quantile (90%) of destructive** plot)

### Conclusion

As we can see, tsunamis often occur in Alaska, but they are usually not destructive. Destructive events typically happen
in Japan, Mexico and Chile.
""")
