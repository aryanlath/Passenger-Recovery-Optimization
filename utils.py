import pandas as pd
from constants import *
from Models.PNR import *
from Models.Flights import *
import re

def PNR_ranking():
    pass

def  Flight_score(pnr, flight):
    pass


def extract_PNR_from_CSV(file_path):
    pnr_objects = []
    with open(file_path, 'r') as file:
        for line in file:
            # pnr = parse_pnr_line(line)/
    # Using regex to extract values within brackets and the remaining parts
            matches = re.findall(r'\[.*?\]|[^,]+', line)
            #/print(matches)
            # Extracting and parsing each part
            pnr_number = matches[0]
           # print(int(x) for x in matches[1].strip('[]').split(','))
            inv_list = [x for x in matches[1].strip('[]').split(',')]
            cabin_list= matches[2].strip('[]').split(',')
            special_requirements = matches[3] == "True"
            PAX = matches[4]
            passenger_loyalty = matches[5]
            is_checkin = matches[6] == "True"

    # Combining all elements into a list
            parsed_list = [pnr_number, inv_list, cabin_list, special_requirements, PAX, passenger_loyalty, is_checkin]
            if(parsed_list==None) :break
            #aprint(parsed_list)
            PNR_Object=PNR(*parsed_list)
            pnr_objects.append(PNR_Object)
    #print(pnr_objects)
    return pnr_objects

def extract_Flights_from_CSV(file_name):
    flights = []
    df = pd.read_csv(file_name)

    for _, row in df.iterrows():

        flight_number = row['Flight Number']
        departure_time = row['Departure Time']
        departure_city = row['Departure City']
        arrival_city = row['Arrival City']
        arrival_time = row['Arrival Time']
        status = row['Status']
        
        # Extracting variable class columns
        cabins= row.drop(['Flight Number', 'Departure City','Departure Time','Arrival City','Arrival Time','Status']).to_dict()
        #print(cabins)
        flights.append(Flight(flight_number, departure_city, departure_time,arrival_city,arrival_time,status, **cabins))
    
    return flights

def convert_result_to_csv(result):
    dataframe = pd.DataFrame()
    PNR = []
    Flight = []
    Cabin = []
    ArrivalCity= []
    DepartureCity = []
    ArrivalTime = []
    DepartureTime = []
    

    
    for result_entry in result['Assignments']:
        PNR.append(result_entry[0].pnr_number)
        Flight.append(result_entry[1].flight_number)
        Cabin.append(result_entry[2])
        ArrivalCity.append(result_entry[1].arrival_city)
        DepartureCity.append(result_entry[1].departure_city)
        ArrivalTime.append(result_entry[1].arrival_time)
        DepartureTime.append(result_entry[1].departure_time)
    dataframe['PNR'] = PNR
    dataframe['Flight'] = Flight 
    dataframe['Cabin'] = Cabin
    dataframe['Arrival City'] = ArrivalCity
    dataframe['Departure City'] = DepartureCity
    dataframe['Arrival Time'] = ArrivalTime
    dataframe['Departure Time'] = DepartureTime
    dataframe.to_csv('result.csv',index = False)


# pnr_object=parse_pnr_file(test_PNR_data_file)
# print(pnr_object)

def find_airport_location(airport_code):
    """
    This function creates a dictionary of airport codes and their corresponding locations in the form of (longitude, latitude).
    Usage: (longitude, latitude) = find_airport_location(airport_code)
    """
    df = pd.read_csv(airport_code_location_data_file)
    for _, row in df.iterrows():
        if row['iata'] == airport_code:
            return row['latitude'], row['longitude']
    return None, None