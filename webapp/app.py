import streamlit as st

main_page = st.Page('main_page.py', title='About project', icon=':material/home:')
basic_analysis_page = st.Page('basic_analysis_page.py', title='Basic analysis', icon=':material/docs:')
hypothesis_analysis_page = st.Page('hypothesis_analysis_page.py', title='Hypothesis analysis', icon=':material/docs:')

pg = st.navigation([main_page, basic_analysis_page, hypothesis_analysis_page])
st.set_page_config(page_title='Earthquakes 1990-2023', page_icon=':material/public:')
pg.run()
