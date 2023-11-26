# Flight Number	Remaining Capacity A	Remaining Capacity F	Departure City	Departure Time	Arrival City	Arrival Time	Status


class Flight:
    def __init__(self, flight_number, remaining_capacity,departure_city, arrival_city, arrival_time, status):
        self.flight_number = flight_number
        self.remaining_capacity = remaining_capacity
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        self.arrival_time = arrival_time
        self.status = status
