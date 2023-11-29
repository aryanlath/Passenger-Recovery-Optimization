import pandas as pd
import numpy as np
import random
from MergeCSV import *

def gen_random_flights():
    flight_data = MergeDataframes()
    random_int = random.randint(0, (len(flight_data)-1)//10)
    cancelled_flight = np.random.randint(0, (len(flight_data)-1), size = random_int)
    for index in cancelled_flight:
        flight_data.at[index, 'Status'] = 'Cancelled'
    csv_file_path = 'Dataset/updated_dataset.csv'  # Replace with your desired file path
    flight_data.to_csv(csv_file_path, index=False)

gen_random_flights()