from scipy.spatial import KDTree
from utils import *

# Example data: Replace this with your actual data
iata_codes = get_all_airports(test_flight_data_file)
airports = {code: find_airport_location(code) for code in iata_codes}

# Extracting the coordinates and creating a KDTree
coordinates = list(airports.values())
tree = KDTree(coordinates)

# Function to find k nearest airports
def find_nearest_airports(iata_code, k=3):
    if iata_code not in airports:
        return "Airport code not found."

    query_point = airports[iata_code]
    distances, indices = tree.query(query_point, k+1) 

    nearest_airports = []
    for i in indices[1:]:
        for code, coord in airports.items():
            if coord == coordinates[i]:
                nearest_airports.append(code)
                break

    return nearest_airports

