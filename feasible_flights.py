from utils import *
from Models.PNR import *
from Models.Flights import *
from constants import *

def init_PNR_to_Flight_Object():
    res = {}
    all_flights = {}
    pnr_list    = extract_PNR_from_CSV(pnr_data_file)
    all_flight  = extract_Flights_from_CSV(flight_data_file)
    for flight in all_flight:
        all_flights[flight.flight_number] = flight
    for pnr in pnr_list:
        res[pnr.pnr_number] = all_flights.get(str(pnr.flight_number))
    return res

def PNR_to_Feasible_Flights(PNR_Object):
    all_flights = extract_Flights_from_CSV(flight_data_file)
    PNR_to_Flight_Object = init_PNR_to_Flight_Object()
    feasible_flight_list = []
    my_flight            = PNR_to_Flight_Object[PNR_Object.pnr_number]
    my_arrival_time      = my_flight.arrival_time
    my_departure_time  = my_flight.departure_time
    for flight in all_flights:
        flight_arrival_time = flight.arrival_time
        flight_departure_time = flight.departure_time
        if((flight_departure_time - my_arrival_time).seconds >= 0 and (flight_departure_time - my_arrival_time).seconds <= ETD*60*60 and flight.status):
            feasible_flight_list.append(flight)

    return feasible_flight_list