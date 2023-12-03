import streamlit as st
import requests
from datetime import date, timedelta, datetime


def get_park_events(park_code, start_date, end_date):
    # Function to fetch events for a specific park using the National Park Service API
    api_key = "c1aDU7AI8ZjaDIJb3GsTBffXs6gRzGzmWdmJFpqk"
    base_url = "https://developer.nps.gov/api/v1/events"

    params = {
        'parkCode': park_code,
        'api_key': api_key,
        'start_date': start_date,
        'end_date': end_date,
    }

    response = requests.get(base_url, params=params)
    events_data = response.json()

    return events_data['data']


def show_park_events():
    st.subheader("Park Events")

    # Fetch a list of parks for the dropdown
    parks_response = requests.get("https://developer.nps.gov/api/v1/parks",
                                  params={'api_key': 'c1aDU7AI8ZjaDIJb3GsTBffXs6gRzGzmWdmJFpqk'})
    parks_data = parks_response.json()
    park_options = {park['fullName']: park['parkCode'] for park in parks_data['data']}

    # Dropdown for selecting a park
    park_name = st.selectbox("Select a Park:", list(park_options.keys()))

    # Radio button to choose between searching within the current month or a custom date range
    search_option = st.radio("Choose a search option:",
                             ["Search events within current month", "Search within a custom date range"])

    if search_option == "Search within a custom date range":
        # Date input for selecting a date or date range (horizontal)
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", date.today())
        end_date = col2.date_input("End Date (Optional)", date.today())
    else:
        # If searching within the current month, update start and end dates
        start_date = date.today().replace(day=1)
        end_date = (date.today() + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    if st.button("Show Events"):
        try:
            park_code = park_options[park_name]
            events = get_park_events(park_code, start_date, end_date)

            if events:
                st.success("Events have been found for this date range:")
                for event in events:
                    st.write(f"**{event['title']}**")
                    st.write(f"Location: {event['location']}")
                    st.write(
                        f"Date: {datetime.strptime(event['datestart'], '%Y-%m-%d').strftime('%B %d, %Y')} to {datetime.strptime(event['dateend'], '%Y-%m-%d').strftime('%B %d, %Y')}")
                    st.write(f"Description: {event['description']}", unsafe_allow_html=True)
                    st.write("---")
            else:
                st.warning("No events found for the specified park and date range.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
