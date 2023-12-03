import streamlit as st
import requests
import pandas as pd


# Function to fetch park data from the National Park Service API
def fetch_park_data():
    api_key = "c1aDU7AI8ZjaDIJb3GsTBffXs6gRzGzmWdmJFpqk"
    base_url = "https://developer.nps.gov/api/v1/parks"
    park_names = []

    start = 0
    limit = 100  # Adjust based on API's allowed limit
    total_parks = None

    while total_parks is None or start < total_parks:
        params = {'api_key': api_key, 'start': start, 'limit': limit}
        response = requests.get(base_url, params=params)
        data = response.json()
        parks = data['data']
        park_names.extend([park['fullName'] for park in parks])

        if total_parks is None:
            total_parks = int(data['total'])

        start += limit

    return park_names


# Function to fetch detailed park data
def fetch_detailed_park_data(park_name):
    api_key = "c1aDU7AI8ZjaDIJb3GsTBffXs6gRzGzmWdmJFpqk"
    base_url = "https://developer.nps.gov/api/v1/parks"
    params = {'api_key': api_key, 'q': park_name}
    response = requests.get(base_url, params=params)
    data = response.json()['data']

    if data:
        return data[0]  # Assuming the first item is the relevant park
    else:
        st.error("No detailed data found for the selected park.")
        return None


# Function to display park information
def display_park_info(park_data):
    st.subheader(park_data['fullName'])

    col1, col2 = st.columns(2)

    with col1:
        if 'images' in park_data and park_data['images']:
            st.image(park_data['images'][0]['url'], caption=park_data['images'][0]['caption'])
        st.text("Description")
        st.write(park_data.get('description', 'No description available'))

    with col2:
        st.text("Activities")
        for activity in park_data.get('activities', []):
            st.write(activity['name'])

        # st.text("Contact Information")
        # for contact in park_data.get('contacts', []):
        #     if 'phoneNumbers' in contact:
        #         for phone in contact['phoneNumbers']:
        #             st.write(f"Phone: {phone.get('phoneNumber', 'N/A')}")
        #     if 'emailAddresses' in contact:
        #         for email in contact['emailAddresses']:
        #             st.write(f"Email: {email.get('emailAddress', 'N/A')}")


# Function to display interactive map
def show_park_map(park_data):
    if 'latLong' in park_data and park_data['latLong']:
        lat, long = map(float, park_data['latLong'].replace('lat:', '').replace('long:', '').split(', '))
        map_data = pd.DataFrame({'lat': [lat], 'lon': [long]})
        st.map(map_data)


def show_explore_page():
    st.title("Explore National Parks")

    park_names = fetch_park_data()
    selected_park = st.selectbox("Select a Park", park_names)

    if st.button("Show Information"):
        detailed_park_data = fetch_detailed_park_data(selected_park)
        if detailed_park_data:
            display_park_info(detailed_park_data)
            show_park_map(detailed_park_data)
