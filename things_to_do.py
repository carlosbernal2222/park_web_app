import pandas as pd
import streamlit as st
import requests
from collections import Counter
from matplotlib import pyplot as plt
import plotly.express as px

# Global Variable:
SPECIAL_CHARACTER_STRING_CLEANUP = ['<br />', '<strong>', '</strong>', '<p>', ' </p>', '<a href="', '">', '</a>',
                                    '</p>', '</li>', '<li>', '</ul>', '<ul>', '</h2>', '<h2>', '</h3>', '<h3>', '</h4>',
                                    '<h4>']


# API fetcher functions
def fetch_things_to_do_data(parkcode):
    api_key = "xXGaGLG1iESex0cTdncv76Kp2OWh1FIqnDbP2fH7"
    base_url = "https://developer.nps.gov/api/v1/thingstodo"
    start = 0
    limit = 25  # Adjust based on API's allowed limit
    params = {'api_key': api_key, 'start': start, 'limit': limit, 'parkCode': parkcode}
    response = requests.get(base_url, params=params)
    data = response.json()
    activities = data["data"]

    return activities


def fetch_park_name_and_code():
    api_key = "c1aDU7AI8ZjaDIJb3GsTBffXs6gRzGzmWdmJFpqk"
    base_url = "https://developer.nps.gov/api/v1/parks"
    park_names = []
    park_codes = []

    start = 0
    limit = 100  # Adjust based on API's allowed limit
    total_parks = None
    parkdict = {}

    while total_parks is None or start < total_parks:
        params = {'api_key': api_key, 'start': start, 'limit': limit}
        response = requests.get(base_url, params=params)
        data = response.json()
        parks = data['data']
        park_names.extend([park['fullName'] for park in parks])
        park_codes.extend([code['parkCode'] for code in parks])
        if total_parks is None:
            total_parks = int(data['total'])
        start += limit

    for name in park_names:
        for code in park_codes:
            parkdict[name] = code
            park_codes.remove(code)
            break

    return parkdict


# Helper Functions for readability
def get_activity_name(thing_to_do_number, file):
    return file[thing_to_do_number]['title']


def get_activity_description(thing_to_do_number, file):
    string = f"**Description**: %s"%file[thing_to_do_number]['shortDescription']
    return string_clean_up(string)


def get_activity_image(thing_to_do_number, file):
    return file[thing_to_do_number]['images'][0]['crops'][0]['url']


def get_topics(thing_to_do_number, file, interest_number):
    return file[thing_to_do_number]['topics'][interest_number]['name']


def get_topics_list(file):
    interests = []
    counter = 0
    counter2 = 0
    for num in file:
        for num2 in file[counter]['topics']:
            interests.append(get_topics(counter, file, counter2))
            counter2 += 1
        counter2 = 0
        counter += 1
    totalInterest = Counter(interests)
    return totalInterest


# these functions would help determine if users want to do certain activities and their caviots
def are_pets_allowed(number, file):
    petDescript = string_clean_up(file[number]['petsDescription'])
    string = ''
    if file[number]['arePetsPermitted'] == 'true':
        string = f"**Pets Allowed**: Yes   \n%s" % petDescript
    elif file[number]['arePetsPermitted'] == 'false':
        string = f"**Pets Allowed**: No   \n%s" % petDescript
    return string


def are_reservations_required(number, file):
    reserDescript = string_clean_up(file[number]['reservationDescription'])
    string = ''
    if file[number]['isReservationRequired'] == 'true':
        string = f"**Reservation needed**: Yes   \n%s" % reserDescript
    elif file[number]['isReservationRequired'] == 'false':
        string = f"**Reservation needed**: No   \n%s" % reserDescript
    return string


def what_type_of_activity(number, file):
    return f"**Type of Activity**: %s" % file[number]['activities'][0]['name']


def are_available_time_of_day(number, file):
    time_of_day = file[number]['timeOfDay']
    if not time_of_day:
        return f"**Activity Time**: Currently Unknown"
    string = ", ".join(str(element) for element in time_of_day)
    return f"**Activity Time**: Currently Unknown%s" % string


def are_available_seasons(number, file):
    seasons = file[number]['season']
    if not seasons:
        return f"**Season Available**: Currently Unknown"
    string = ", ".join(str(element) for element in seasons)
    return f"**Season Available**: Currently Unknown%s" % string


def are_fees_applicable(number, file):
    string = ''
    if file[number]['doFeesApply'] == 'true':
        string = f"**Fees:**: Yes \n%s" % file[number]['feeDescription']
    elif file[number]['doFeesApply'] == 'false':
        string = f"**Fees:**: No \n%s" % file[number]['feeDescription']
    else:
        string = f"**Fees:**: Currently Unknown \n"
    return string_clean_up(string)


# This is to Display activities
def display_activities(file):
    counter = 0
    for lists in file:
        expander = st.expander(label=("{0}\. {1}".format(str(counter + 1), get_activity_name(counter, file))))
        expander.image(get_activity_image(counter, file), width=600)
        expander.write(str(get_activity_description(counter, file)))
        expander.write(are_pets_allowed(counter, file))
        expander.write(what_type_of_activity(counter, file))
        expander.write(are_available_time_of_day(counter, file))
        expander.write(are_available_seasons(counter, file))
        expander.write(are_fees_applicable(counter, file))
        expander.write(are_reservations_required(counter, file))
        counter += 1


# This is to Display The graph Elements
def display_topics_graph(data):
    names = list(data.keys())
    values = list(data.values())
    dataFrame = pd.DataFrame({"Name of Topic": names, "Number of Appearances": values})
    st.bar_chart(dataFrame, x='Name of Topic', y='Number of Appearances')


def display_topics_dataframe(data):
    names = list(data.keys())
    values = list(data.values())
    dataFrame = pd.DataFrame({"Name of Topic": names, "Number of Appearances": values})
    st.write(dataFrame)


def display_topics_pie_chart(data):
    names = list(data.keys())
    values = list(data.values())
    dataFrame = pd.DataFrame({"Name of Topic": names, "Number of Appearances": values})

    fig = px.pie(dataFrame, values=values, names=names,
                 title=f'Pie Plot',
                 height=400, width=300)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0), )
    st.plotly_chart(fig, use_container_width=True)


# this is to clean some of the strings that the API brings
def string_clean_up(string):
    clean_string = string
    for special in SPECIAL_CHARACTER_STRING_CLEANUP:
        clean_string = clean_string.replace(special, '')
    return clean_string


# main
def show_things_to_do_page():
    st.title("Things to do")
    park_Name_and_code = fetch_park_name_and_code()
    choice_Of_Park = st.selectbox(label="Select a National Park", options=list(park_Name_and_code.keys()))
    ListOfThingsTodo = fetch_things_to_do_data(park_Name_and_code[choice_Of_Park])
    if ListOfThingsTodo:
        choices = st.sidebar.radio("Activity Visualization", ["Show List of Activities", "Show Data of Activities",
                                                              "Show Instances of Select Topic"])
        if choices == "Show List of Activities":
            st.success("You have chosen: {}".format(choice_Of_Park))
            display_activities(ListOfThingsTodo)
        if choices == "Show Data of Activities":
            st.title("The following list encompasses the diverse range of topics and attractions available within the "
                     "park.")
            col1, col2 = st.columns([1, 3])
            with col1:
                st.write("Data Frame Graph")
                display_topics_dataframe(get_topics_list(ListOfThingsTodo))
            with col2:
                st.write("Bar Graph")
                display_topics_graph(get_topics_list(ListOfThingsTodo))
                display_topics_pie_chart(get_topics_list(ListOfThingsTodo))
        if choices == "Show Instances of Select Topic":
            multiselect = st.multiselect(label='Select the topics you want to see',
                                         options=get_topics_list(ListOfThingsTodo).keys())
            for key in multiselect:
                # st.write("{}: {} Instances".format(key, get_topics_list(ListOfThingsTodo)[key]))
                st.write(f"**%s**: %s Instances" % (key, get_topics_list(ListOfThingsTodo)[key]))

    else:
        st.error(
            "You have chosen: {}. This park, currently, has no data. Please try another park".format(choice_Of_Park))
