import pandas as pd
from constants import *
from Models.PNR import *
from Models.Flights import *

def PNR_ranking():
    pass

def  Flight_score(pnr, flight):
    pass

def extract_PNR_from_CSV(file_name):
    pnr_df = pd.read_csv(file_name)
    # pnr_number, flight_cabin, flight_number, special_requirements, is_checkin,passenger_loyalty,PAX
    pnr_list = [
    PNR(row['PNR Number'],row['Cabin'],row['Flight Number'],row['Special Requirements'],row['isCheckin'],row['Passenger Loyalty'],row['PAX'])
    for index, row in pnr_df.iterrows()
    ]
    return pnr_list

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
