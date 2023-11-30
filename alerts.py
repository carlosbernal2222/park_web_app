import streamlit as st
import requests
from datetime import date

def get_park_alerts(api_key, park_code):
    base_url = f"https://developer.nps.gov/api/v1/alerts"
    params = {
        'parkCode': park_code,
        'api_key': api_key,
        'limit': 5,
    }

    response = requests.get(base_url, params=params)
    alerts_data = response.json()

    return alerts_data.get('data', [])

def show_park_alerts():
    st.subheader("Park Alerts")

    # Fetch a list of parks for the dropdown
    parks_response = requests.get("https://developer.nps.gov/api/v1/parks", params={'api_key': 'c1aDU7AI8ZjaDIJb3GsTBffXs6gRzGzmWdmJFpqk'})
    parks_data = parks_response.json()
    park_options = {park['fullName']: park['parkCode'] for park in parks_data['data']}

    # Dropdown for selecting a park
    park_name = st.selectbox("Select a Park:", list(park_options.keys()))

    if st.button("Show Alerts"):
        try:
            park_code = park_options[park_name]
            alerts = get_park_alerts(api_key="c1aDU7AI8ZjaDIJb3GsTBffXs6gRzGzmWdmJFpqk", park_code=park_code)

            if alerts:
                st.success(f"{len(alerts)} Alerts have been found for the specified park:")
                for alert in alerts:
                    st.write(f"**Title:** {alert['title']}")
                    st.write(f"**Category:** {alert['category']}")
                    st.write(f"**Description:** {alert['description']}")
                    st.write("---")
            else:
                st.warning("No alerts found for the specified park.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    # Checkbox to enable or disable alerts
    enable_alerts = st.checkbox("Enable Text Alerts")

    if enable_alerts:
        # Text box for entering the phone number
        phone_number = st.text_input("Enter your Phone Number:")

        if st.button("Get Alerts"):
            try:
                park_code = park_options[park_name]
                alerts = get_park_alerts(api_key="c1aDU7AI8ZjaDIJb3GsTBffXs6gRzGzmWdmJFpqk", park_code=park_code)

                if alerts:
                    st.success(f"{len(alerts)} Alerts have been found for the specified park. SMS alerts sent to {phone_number}.")
                    for alert in alerts:
                        st.write(f"**Title:** {alert['title']}")
                        st.write(f"**Category:** {alert['category']}")
                        st.write(f"**Description:** {alert['description']}")
                        st.write("---")
                else:
                    st.warning("No alerts found for the specified park.")
            except Exception as e:
                st.error(f"An error occurred: {e}")


