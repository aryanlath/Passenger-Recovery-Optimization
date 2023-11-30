import googlemaps
from datetime import datetime
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the API key
api_key = os.getenv('GMAPS_API_KEY')

def get_distance(api_key, source_lat, source_lng, dest_lat, dest_lng, departure_datetime):
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=api_key)

    # Format the departure time
    departure_datetime = datetime.strptime(f'{date} {departure_time}', '%Y-%m-%d %H:%M:%S')

    # Make the API request
    result = gmaps.distance_matrix(origins=(source_lat, source_lng),
                                   destinations=(dest_lat, dest_lng),
                                   mode="driving",
                                   departure_time=departure_datetime)

    # Extract the distance from the response
    distance = result['rows'][0]['elements'][0]['distance']['text']
    return distance

# Example usage
api_key = 'YOUR_API_KEY'
source_lat = 40.7128  # Example latitude
source_lng = -74.0060 # Example longitude
dest_lat = 34.0522    # Example latitude
dest_lng = -118.2437  # Example longitude
departure_datetime = '2024-05-25 04:37:00'   # Example date

distance = get_distance(api_key, source_lat, source_lng, dest_lat, dest_lng, date, departure_time)
print(distance)
