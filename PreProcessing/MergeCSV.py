import pandas as pd
from datetime import timedelta
import sys
sys.path.append('./Passenger-Recovery-Optimization')
from constants import * 
def MergeDataframes(schedule_csv_path,inventory_csv_path):
    """
        returns merged flightschedule pandas dataframe 
    """
    inv_df = pd.read_csv(inventory_csv_path)
    sch_df = pd.read_csv(schedule_csv_path)
    for i, row in inv_df.iterrows():
        # Find the matching row in sch_df based on FlightNumber
        matching_row = sch_df[sch_df['FlightNumber'] == row['FlightNumber']]

        # Check if there is a matching row and then update
        if not matching_row.empty:
            inv_df.at[i,'DepartureTime'] = matching_row['DepartureTime'].iloc[0]
            inv_df.at[i, 'ArrivalTime'] = matching_row['ArrivalTime'].iloc[0]
        
    inv_df['DepartureTime']=pd.to_datetime(inv_df['DepartureTime'])
    inv_df['ArrivalTime']=pd.to_datetime(inv_df['ArrivalTime'])
    inv_df['DepartureDate']=pd.to_datetime(inv_df['DepartureDate'])
    inv_df['ArrivalDate']=pd.to_datetime(inv_df['ArrivalDate'])
    for i, row in inv_df.iterrows():
        if row['ArrivalTime'] < row['DepartureTime']:
            # Add one day to the ArrivalTime
            inv_df.at[i, 'ArrivalDate'] = row['ArrivalDate'] + timedelta(days=1)
            
    inv_df['DepartureDatetime'] = pd.to_datetime(inv_df['DepartureDate']) + pd.to_timedelta(inv_df['DepartureTime'].dt.strftime('%H:%M:%S'))
    inv_df['ArrivalDatetime'] = pd.to_datetime(inv_df['ArrivalDate']) + pd.to_timedelta(inv_df['ArrivalTime'].dt.strftime('%H:%M:%S'))
    inv_df.drop(['DepartureDate','ArrivalDate','ArrivalTime','DepartureTime'],axis=1,inplace=True)
    inv_df['Status'] = "On Time"
    return inv_df

    