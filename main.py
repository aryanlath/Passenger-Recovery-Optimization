from feasible_flights import *
from constants import *
from init_functions import *
from gurobi_optimisation import *
from gurobi_optimisation_2 import *
from Leap_Quantum import *
import pprint
import constants_immutable
pp = pprint.PrettyPrinter(indent=4)
from Assign_Class import *


def Main_function():

    # initializes the loyalty scores for the passengers
    init_loyalty_dictionary()

    # global all_flights, pnr_objects,  pnr_flight_mapping, pnr_to_s2
    constants_immutable.all_flights, constants_immutable.pnr_objects, constants_immutable.pnr_flight_mapping, constants_immutable.pnr_to_s2 = Get_All_Maps()
    # finds the normalization factors for the cost function
    init_normalize_factors()



    # Identify the impacted PNRs
    Impacted_PNR = Get_Impacted_passengers(constants_immutable.all_flights, constants_immutable.pnr_objects)

    print(Cabin_to_Class(result["Assignments"]))

    print("Total impacted Passengers: ",len(Impacted_PNR))
    pp.pprint(Impacted_PNR)
    start = time.time()
    result = optimize_flight_assignments(Impacted_PNR)
    end = time.time()
    print("Classical Time " , end -start)
    print("Total Reassigned: ",len(result['Assignments']))

    pp.pprint(result['Assignments'])
    print("Not Assigned PNRs: ")
    pp.pprint(result['Non Assignments'])
    print("\n\n\n\n")
    start = time.time()
    quantum_result =quantum_optimize_flight_assignments(Impacted_PNR)
    end = time.time()
    print("QUANTUM TIME ", end-start)
    # print(quantum_result)

    # print(Cabin_to_Class(result["Assignments"]))


    print("QUANTUM RESULTS")
    print("Total Reassigned: ",len(quantum_result['Assignments']))

    pp.pprint(quantum_result['Assignments'])
    print("Not Assigned PNRs: ")
    pp.pprint(quantum_result['Non Assignments'])
    print("\n\n\n\n")
    
    print("Exception List handling...")
    print() 
    print()
    result2 = optimize_flight_assignments_2(result['Non Assignments'],constants_immutable.all_flights)
    pp.pprint(result2['Assignments'])
    print("Not Assigned PNRs: ")
    pp.pprint(result2['Non Assignments'])
    print("\n\n\n\n")


if __name__==  "__main__":
    Main_function()
