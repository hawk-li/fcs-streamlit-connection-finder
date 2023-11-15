import json
import pandas as pd

import streamlit as st
from connection import Connection
import requests

def find_connection(origin, destination, departure_date, departure_time):
    url = 'http://transport.opendata.ch/v1/connections'

    params = {}
    params['from'] = origin
    params['to'] = destination
    params['date'] = departure_date
    params['time'] = departure_time

    r = requests.get(url, params = params)
    
    first_conn= r.json()['connections'][0]
    # Uncomment the next line to see the JSON object of first_conn
    # print(json.dumps(first_conn, ensure_ascii=False, indent=4))

    x = first_conn['to']['station']['coordinate']['x']
    y = first_conn['to']['station']['coordinate']['y']
    departure = first_conn['from']['departure']
    arrival = first_conn['to']['arrival']
    transport_means = first_conn['products']

    return Connection(x, y, departure, arrival, transport_means)

def find_restaurants(x, y, open_at, radius):
    api_key = st.secrets["API_KEY"]
    url = 'https://api.yelp.com/v3/businesses/search'
    
    headers = {"Authorization": "Bearer " + api_key}
    
    restaurants = []
    params = {}
    params['latitude'] = x
    params['longitude'] = y
    params['open_at'] = open_at
    params['radius'] = radius
    params['categories'] = "restaurants"
    
    r = requests.get(url, params=params, headers=headers)
    #print(json.dumps(r.json(), ensure_ascii=False, indent=4))
   
    for b in r.json()['businesses']:
        name = b['name']
        rating = b['rating']
        # in addition to the data used in the assignment, we also store the categories and the number of reviews
        num_reviews = b['review_count']
        categories = [c['title'] for c in b['categories']]
        # create a string with the categories separated by commas
        categories = ', '.join(categories)
        # add coordinates for map
        latitude = b['coordinates']['latitude']
        longitude = b['coordinates']['longitude']
        
        restaurants.append((name, rating, num_reviews, categories, latitude, longitude))
    return restaurants

def find_top10_restaurants_for_trip(con, radius):
    limit = 10

    rests= find_restaurants(con.destination_x, con.destination_y, con.get_unix_arrival_time(), radius)
    rests_sorted = sorted(rests, key=lambda tup: tup[1], reverse=True)
    
    return rests_sorted[:limit]