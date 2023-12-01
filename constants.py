pnr_data_file = 'Dataset/passenger_pnr_dataset.csv'
flight_data_file = 'Dataset/flight_schedule_dataset.csv'
test_PNR_data_file = 'Dataset/test_data/PNR_test.csv'
test_flight_data_file = 'Dataset/test_data/flight_test.csv'
airport_code_location_data_file = 'Dataset/airport-code-to-location.csv'
test_PNR_data_file = 'Dataset/test_data/PNR_Test.csv'
test_flight_data_file = 'Dataset/test_data/flight_test.csv'
n_cabin=2
ETD=72
MCT=1
NON_ASSIGNMENT_COST=100
MAXCT=12
PNR_SSR=200
PNR_connection=100
PNR_paidservice=200
PNR_bookingtype=500
PNR_pax=50
PNR_penalty=-50
Loyalty_CM=2000
Loyalty_platinum=1800
Loyalty_gold=1600
Loyalty_silver=1500
weight_flight_map = 100
weight_pnr_map = 100
weight_cabin_map = 100
pnr_normalize_factor = 100
flight_normalize_factor = 100
cabin_normalize_factor = 100
loyalty_dict = {}

def init_normalize_factors(all_flights,pnr_objects,pnr_flight_mapping,pnr_to_s2):
    global pnr_normalize_factor
    for pnr in pnr_to_s2:
        pnr_normalize_factor = max(pnr_normalize_factor,pnr_to_s2[pnr])
    global flight_normalize_factor
    flight_normalize_factor = 100
    global cabin_normalize_factor
    cabin_normalize_factor = 100

def init_loyalty_dictionary():
    """
    Initialize the loyalty dictionary
    """
    global loyalty_dict
    loyalty_dict["CM"] = Loyalty_CM
    loyalty_dict["Platinum"] = Loyalty_platinum
    loyalty_dict["Gold"] = Loyalty_gold
    loyalty_dict["Silver"] = Loyalty_silver
    print(loyalty_dict)