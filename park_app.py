
import streamlit as st
from home import show_home
from footer import show_footer
from events import show_park_events
from explore import show_explore_page
from alerts import show_park_alerts
from datetime import date
import pandas as pd
import numpy as np

api_key="c1aDU7AI8ZjaDIJb3GsTBffXs6gRzGzmWdmJFpqk"

# Set page config
st.set_page_config(
    page_title="National Parks Data Visualizer",
    layout="wide",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': 'https://www.gregoryreis.com',
        'About': '# Welcome to the National Parks Data Visualizer. Developed by Gregory Murad Reis'
    }
)

# Header
st.title("National Parks Data Visualizer")
# st.header("Explore the natural beauty preserved across the country")

# Sidebar for navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.radio("Choose a page:",
                              ["Home", "Explore", "Events", "Visitor Statistics", "Park Conservation", "Park Alerts"])

if navigation == "Explore":
    show_explore_page()

elif navigation == "Events":
    show_park_events()

elif navigation == "Visitor Statistics":
    st.write("Visitor Statistics page is under construction.")
    # Code for the Visitor Statistics page needs to be in different file and imported to the app

elif navigation == "Park Conservation":
    st.write("Park Conservation page is under construction.")
    # Code for the Park Conservation page needs to be in different file and imported to the app

elif navigation == "Park Alerts":
    show_park_alerts()

else:
    # Home Page Content
    show_home()

# Footer
show_footer()
