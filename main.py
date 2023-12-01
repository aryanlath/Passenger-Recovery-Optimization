from feasible_flights import *
from constants import *
from utils import *
from gurobi_optimisation import *

import pprint 
pp = pprint.PrettyPrinter(indent=4)


# initializes the loyalty scores for the passengers
init_loyalty_dictionary()

all_flights,pnr_objects,pnr_flight_mapping,pnr_to_s2 = Get_All_Maps()
# finds the normalization factors for the cost function
init_normalize_factors(all_flights,pnr_objects,pnr_flight_mapping,pnr_to_s2)



# Identify the impacted PNRs
Impacted_PNR = Get_Impacted_passengers(all_flights,pnr_objects)
print("Total impacted Passengers: ",len(Impacted_PNR))
pp.pprint(Impacted_PNR)
result = optimize_flight_assignments(Impacted_PNR)
print("Total Reassigned: ",len(result['Assignments']))

pp.pprint(result['Assignments'])
print("Not Assigned PNRs: ")
pp.pprint(result['Non Assignments'])


