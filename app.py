import streamlit as st
import pandas as pd

import streamlit as st

st.set_page_config(page_title="Marketing Campaign Performance", 
                   layout="wide", initial_sidebar_state = "collapsed")

home = st.Page(page = "pages/1_home.py",title = "Home")
dash = st.Page(page = "pages/2_dashboard.py", title = "Dashboard")
pred = st.Page(page = "pages/3_prediction.py", title = "Prediction")

pg = st.navigation([home, dash, pred])
pg.run()







