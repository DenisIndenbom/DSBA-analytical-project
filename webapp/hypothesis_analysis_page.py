import streamlit as st

from utils import load_data, center_title_h5, pie

data = load_data()

st.title('Hypothesis')
st.markdown('**Tsunamis are more destructive than earthquakes.**')
st.markdown("""**Destructive definition**

$destructive = \\log(\\max(1, magnitudo))*significance$""")

st.subheader('Analysis')

center_title_h5('Mean of destructive')
st.bar_chart(data.groupby('tsunami').agg({'destructive':'mean'}), x_label='Tsunami', y_label='Destructive')
st.markdown('*As we can see, on average tsunami is more destructive than ordinary earthquakes.*')

center_title_h5('Quantile (50%) of destructive')
st.bar_chart(data.groupby('tsunami').agg({'destructive':lambda x:x.quantile(0.5)}), x_label='Tsunami',
             y_label='Destructive')
st.markdown(
    '*Here we see, 50 percent of tsunamis are more destructive than earthquakes. Also, we see that destructive of 50 '
    'percent of earthquakes less than 50 points.*')

center_title_h5('Quantile (90%) of destructive')
st.bar_chart(data.groupby('tsunami').agg({'destructive':lambda x:x.quantile(0.9)}), x_label='Tsunami',
             y_label='Destructive')
st.markdown('*In this case, the 10 percent of tsunamis are more destructive than earthquakes*')

center_title_h5('Maximal value of destructive')
st.bar_chart(data.groupby('tsunami').agg({'destructive':'max'}), x_label='Tsunami', y_label='Destructive')
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

- The most destructive earthquake was a tsunami. $\triangle max=63.2$ (**Maximal value of destructive** plot) 
- The average tsunami is more destructive than the average earthquake. (**Mean of destructive** plot) 
- The 90 percent of tsunamis are more destructive than the 10 percent of earthquakes. (**Quantile (90%) of destructive** plot)

### Conclusion

As we can see, tsunamis often occur in Alaska, but they are usually not destructive. Destructive events typically happen
in Japan, Mexico and Chile.
""")
