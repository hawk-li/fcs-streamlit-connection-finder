from utils import find_connection, find_top10_restaurants_for_trip

import streamlit as st
from datetime import datetime
import traceback
import pandas as pd

# Main function for the streamlit app
def main():
    st.set_page_config(page_title="Train Connection and Restaurant Finder", page_icon=":train:")
    st.title("Train Connection and Restaurant Finder")

    # Initialize session state for the connection, to be reused if the page is refreshed
    if 'con' not in st.session_state:
        st.session_state['con'] = None

    # Initialize session state for the restaurants, to be reused if the page is refreshed
    if 'restaurants' not in st.session_state:
        st.session_state['restaurants'] = None

    # User input for the journey
    origin = st.text_input("Origin")
    destination = st.text_input("Destination")
    departure_date = st.date_input("Departure Date", datetime.now())
    departure_time = st.time_input("Departure Time", datetime.now().time())

    # Button to find connections
    if st.button("Find Connection"):
        if not origin or not destination:
            st.error("Please enter an origin and a destination.")
        else:
            try:
                st.session_state.con = find_connection(origin, destination, departure_date.strftime("%Y-%m-%d"), departure_time.strftime("%H:%M"))
            except Exception as e:
                st.error(f"An error occurred: {e}")
                # show the traceback to help with debugging, should be removed in production
                st.error(traceback.format_exc())  
    # Display connection if it was already loaded previously
    if st.session_state.con != None:
        display_connection(st.session_state.con)
    # Button and slider for restaurant search, only if a connection has been found
    if st.session_state.con != None:
        radius = st.slider("Restaurant Search Radius (in meters)", 100, 1000, 500)
        if st.button("Find Restaurants"):
            try:
                st.session_state.restaurants = find_top10_restaurants_for_trip(st.session_state.con, radius)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.error(traceback.format_exc())
        # Display restaurants if they were already loaded previously
        if st.session_state.restaurants != None:
            display_restaurants(st.session_state.restaurants)

# Display functions, included here because they use streamlit functions directly
def display_connection(con):
    """
    Displays information about a connection.

    Args:
        con (Connection): The connection to display information about.
    """
    st.markdown(f"### Connection Found")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Transport Means:**")
        for mean in con.transport_means:
            st.markdown(f"- {mean}")
    with col2:
        st.markdown("**Departure:**")
        st.markdown(f"`{con.departure_time.strftime('%Y-%m-%d %H:%M')}`")
        st.markdown("**Arrival:**")
        st.markdown(f"`{con.arrival_time.strftime('%Y-%m-%d %H:%M')}`")

def display_restaurants(restaurants):
    """
    Displays the top restaurants at a destination, along with their ratings, number of reviews, and categories.
    Also displays the restaurants on a map.

    Parameters:
    restaurants (list): A list of dictionaries containing information about the restaurants, including name, rating,
                        number of reviews, categories, latitude, and longitude.

    Returns:
    None
    """
    st.markdown(f"### Top Restaurants at Destination")
    df = pd.DataFrame(restaurants, columns=["Name", "Rating", "Number of Reviews", "Categories", "latitude", "longitude"])
    st.table(df[["Name", "Rating", "Number of Reviews", "Categories"]])

    # Display restaurants on map
    df_map = df[["Name", "latitude", "longitude"]]
    st.map(df_map, size=1)

if __name__ == "__main__":
    main()
