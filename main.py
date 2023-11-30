from feasible_flights import *
from constants import *

graph=create_flight_graph()
# PNR_to_FLight_Object=init_PNR_to_Flight_Object()

all_flights,pnr_objects,pnr_flight_mapping,pnr_to_s2 = Get_All_Maps()
# finds the normalization factors for the cost function
init_normalize_factors(all_flights,pnr_objects,pnr_flight_mapping,pnr_to_s2)
# initializes the loyalty scores for the passengers
init_loyalty_dictionary()