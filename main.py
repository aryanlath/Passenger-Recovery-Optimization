from feasible_flights import *
from constants import *
from init_functions import *
from gurobi_optimisation import *
from Gurobi_Quantum_2 import *
import pprint
import constants_immutable
pp = pprint.PrettyPrinter(indent=4)
from Assign_Class import *
from handle_city_pairs import *




# initializes the loyalty scores for the passengers
init_loyalty_dictionary()

# global all_flights, pnr_objects,  pnr_flight_mapping, pnr_to_s2
constants_immutable.all_flights, constants_immutable.pnr_objects, constants_immutable.pnr_flight_mapping, constants_immutable.pnr_to_s2 = Get_All_Maps()
# finds the normalization factors for the cost function
init_normalize_factors()



# Identify the impacted PNRs
Impacted_PNR = Get_Impacted_passengers(constants_immutable.all_flights, constants_immutable.pnr_objects)



print("Total impacted Passengers: ",len(Impacted_PNR))
pp.pprint(Impacted_PNR)
result = optimize_flight_assignments(Impacted_PNR)
print("Total Reassigned: ",len(result['Assignments']))

pp.pprint(result['Assignments'])
print("Not Assigned PNRs: ")
pp.pprint(result['Non Assignments'])

print("\n\n\n\n")
quantum_result =quantum_optimize_flight_assignments(Impacted_PNR)
print(quantum_result)

print(Cabin_to_Class(result["Assignments"]))

for pnr in result["Non Assignments"]:
    original_arrival = pnr.inv_list
# print("\n\n\n\n")
# quantum_result =optimize_flight_assignments(Impacted_PNR)
# print(quantum_result)

# print(Cabin_to_Class(result["Assignments"]))


# print("QUANTUM RESULTS")
# print("Total Reassigned: ",len(quantum_result['Assignments']))

# pp.pprint(quantum_result['Assignments'])
# print("Not Assigned PNRs: ")
# pp.pprint(quantum_result['Non Assignments'])
# print("\n\n\n\n")

