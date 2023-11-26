# Flight Number	Remaining Capacity A	Remaining Capacity F	Departure City	Departure Time	Arrival City	Arrival Time	Status
from datetime import datetime

def convert_to_datetime(time):
        date_format = "%Y-%m-%d %H:%M"
        return datetime.strptime(time, date_format)

class Flight:
    
    def __init__(self, flight_number,departure_city, departure_time, arrival_city, arrival_time, status,**cabins):
        self.flight_number = str(flight_number)
        self.cabins = cabins
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.arrival_time = convert_to_datetime(arrival_time)
        self.departure_time = convert_to_datetime(departure_time)
        self.status = status.lower()=="on time"

    def __hash__(self) -> int:
        return hash(self.flight_number)

    def __repr__(self):
        cabins_str = ', '.join([f'{k}: {v}' for k, v in self.cabins.items()])
        return f"Flight({self.flight_number}, Departure: {self.departure_time}, Destination: {self.departure_city}, Classes: {cabins_str})"



