import streamlit as st

main_page = st.Page('main_page.py', title='About project', icon=':material/home:', default=True)
basic_analysis_page = st.Page('basic_analysis_page.py', title='Basic analysis', icon=':material/docs:')
hypothesis_analysis_page = st.Page('hypothesis_analysis_page.py', title='Hypothesis analysis', icon=':material/docs:')
time_plots = st.Page('time_plots.py', title='Time plots', icon=':material/monitoring:')
state_plots = st.Page('state_plots.py', title='State plots', icon=':material/monitoring:')
api_docs = st.Page('api_docs.py', title='API Documentation', icon=':material/docs:')

pg = st.navigation({
    'Project': [main_page, basic_analysis_page, hypothesis_analysis_page],
    'Interactive plots': [time_plots, state_plots],
    'FastAPI': [api_docs]
})

st.set_page_config(page_title='Earthquakes 1990-2023', page_icon=':material/monitoring:')
pg.run()
