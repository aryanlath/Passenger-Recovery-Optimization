import requests
import os
from dotenv import load_dotenv
from k_nearest_airports import *
from constants import CITY_PAIR_THRESHOLD

# Load the .env file
load_dotenv()

# Access the API key
api_key = os.getenv('GMAPS_API_KEY')


def city_pairs_cost_function(distance, time, alpha=2, beta=3, epsilon=0.001):
    """
    A function to prioritize shorter distances and times.
    Args:
    distance (float): The distance between points A and B.
    time (float): The time taken to travel from A to B in seconds.
    alpha (float): The weight for the distance.
    beta (float): The weight for the time.
    epsilon (float): A small constant to avoid division by zero.

    Returns:
    float: The calculated value giving priority to shorter distances and times.
    """
    return 1e15 / (distance**alpha + time**beta + epsilon)


def get_city_pairs_cost(original_airport,departure_time=None):
    """
    A function to get the updated cost for considering different city pairs.
    Args:
    original_airport: Code for original airport arrival location
    new_airport: Code for new airport arrival location
    departure_time(optional) : to give calculate distances dynamically based on the real time
    Returns:
    float: The normalised score value depending on how near or far the new proposed arival location is
    """
    # Set up the API URL and parameters from distance matrix
    (l1,l2) = find_airport_location(original_airport)
    nearest_airports = find_nearest_airports(original_airport)
    city_pairs_and_cost = []
    for airport in nearest_airports:
        (l3,l4) = find_airport_location(airport)
        api_url = "https://api.distancematrix.ai/maps/api/distancematrix/json"
        params = {
            "origins": f"{l1},{l2}",
            "destinations": f"{l3},{l4}",
            "departure_time": "now" if departure_time is None else departure_time,
            "key": api_key 
        }


        # Make the request
        response = requests.get(api_url, params=params)

        # Handle the response
        if response.status_code == 200:
            # Request was successful
            data = response.json()
            # Extract distance and duration based on real life data
            duration_in_traffic_seconds = data['rows'][0]['elements'][0]['duration_in_traffic']['value']
            if(duration_in_traffic_seconds>=CITY_PAIR_THRESHOLD*60*60):
                continue
            distance_str = data['rows'][0]['elements'][0]['distance']['text']
            distance = float(distance_str.split()[0])
            priority_value = city_pairs_cost_function(distance, duration_in_traffic_seconds)
            city_pairs_and_cost.append((airport,float("{:.4f}".format(priority_value))))
        
    return city_pairs_and_cost