import pandas as pd
from Models.PNR import *

def PNR_ranking():
    pass

def  Flight_score(pnr, flight):
    pass


def extract_PNR(file_name):
    pnr_df = pd.read_csv(file_name)
    # pnr_number, flight_cabin, flight_number, special_requirements, is_checkin,passenger_loyalty,PAX
    pnr_list = [
    PNR(row['PNR Number'],row['Cabin'],row['Flight Number'],row['Special Requirements'],row['isCheckin'],row['Passenger Loyalty'],row['PAX'])
    for index, row in pnr_df.iterrows()
    ]


    # Display the PNR objects
    # for pnr in pnr_list:
    #     print(f"PNR Number: {pnr.pnr_number}, Flight Number: {pnr.flight_number}, Cabin: {pnr.flight_cabin}, "
    #         f"Special Requirements: {pnr.special_requirements}, PAX: {pnr.PAX}, "
    #         f"Passenger Loyalty: {pnr.passenger_loyalty}, isCheckin: {pnr.is_checkin}")
    
    return pnr_list

# extract_PNR("./Dataset/passenger_pnr_dataset.csv")