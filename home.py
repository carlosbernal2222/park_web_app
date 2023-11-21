import streamlit as st

def show_home():
    st.subheader("Welcome to the Home Page")
    st.markdown("""
        This web application provides interactive visualizations and insights into America's National Parks.
        - **Park Data**: Get detailed information about each park.
        - **Wildlife**: Discover the wildlife that inhabits each park.
        - **Visitor Statistics**: Analyze visitor trends and statistics.
        - **Park Conservation**: Learn about conservation efforts and how you can contribute.

        Start by selecting a feature from the navigation sidebar to explore the data.
    """)

    # Example of a simple interactive element
    if st.button('Click here for a quick tour'):
        st.sidebar.write("The sidebar is used for navigation between different pages of the app.")
        st.balloons()
