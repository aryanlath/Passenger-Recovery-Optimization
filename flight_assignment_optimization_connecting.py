import pandas as pd
from ortools.linear_solver import pywraplp
from utils import *
from Models.Flights import Flight
from collections import defaultdict
from feasible_flights import *
from cost_function import *
all_flights =[]

def get_flight_cabin_mappings(flights, current_mapping=None, flight_index=0):
    """
    To generate the tuple of all possible cabin Mappings.
    Takes Flight_Tuple as input
    Returns the list of cabin_tuples
    """
    if current_mapping is None:
        current_mapping = []

    if flight_index == len(flights):
        yield tuple(cabin for _, cabin in current_mapping)
        return

    flight = flights[flight_index]

    for cabin in flight.cabins:
        current_mapping.append((flight.flight_number, cabin))
        yield from get_flight_cabin_mappings(flights, current_mapping, flight_index + 1)
        current_mapping.pop()

def optimize_flight_assignments(PNR_List , all_flights):
    g=create_flight_graph()
    PNR_to_Flight_Object=init_PNR_to_Flight_Object()
    """
        PNR_List = List of Impacted PNRs
        PNR_to_Feasible_Flights now returns a list of tuples of flight objects Ex. [(Flight1),(Flight1->Flight2),(Flight3)]
        X_PNR_Constraint -> dictionary where keys are PNR objects and each value is a list of variables for that Particular PNR in its constraint
        X_Flight_Capacity_Constraint-> dictionary of dictionaries where outer keys are Flight objects and inner keys are cabins, each value is a list of variables for that Particular Flight,Cabin in its constraint
    """
    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    if not solver:
        return "No solver available."
    X_PNR_Constraint = defaultdict(list)
    #
    X_Flight_Capacity_Constraint = defaultdict(lambda: defaultdict(list))
    # Variables
    # X_ijk = 1 if the ith PNR is assigned to the jth flight's kth class
    X = {}
    Y = {} # Store the complements of X
    # PNR_to_Feasible_Flights now returns a list of tuples of flight objects 
    # Ex. [(Flight1),(Flight1->Flight2),(Flight3)]
    for PNR in PNR_List:
        for Flight_Tuple in PNR_to_Feasible_Flights(g,PNR_to_Flight_Object,PNR):
            cabins_tuple = get_flight_cabin_mappings(Flight_Tuple)
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('A','B')
                X[(PNR,Flight_Tuple,cabin)] = solver.BoolVar(f'X[{PNR},{Flight_Tuple},{cabin}]')
                Y[(PNR,Flight_Tuple,cabin)] = solver.BoolVar(f'Y[{PNR},{Flight_Tuple},{cabin}]')
                solver.Add(X[(PNR,Flight_Tuple,cabin)]+Y[(PNR,Flight_Tuple,cabin)]==1)
                X_PNR_Constraint[PNR].append(X[(PNR,Flight_Tuple,cabin)])

            for flight in Flight_Tuple:
                for cabin in cabins_tuple:
                    X_Flight_Capacity_Constraint[flight][cabin].append(X[(PNR, flight, cabins_tuple)] * PNR.PAX)



          
    # Constraints
    # Each PNR can be assigned to only one flight class
    for PNR in PNR_List :
        solver.Add(sum(X_PNR_Constraint[PNR]) <= 1)

    # The number of assigned passengers should not exceed available seats
    for Flight, constraint_dic in X_Flight_Capacity_Constraint.items():
        for cabin, cabin_list in constraint_dic.items():
            solver.Add(sum(cabin_list) <= Flight.cabins[cabin])

    # Objective
    # Maximise the total cost
    objective = solver.Objective()

    for PNR in PNR_List:
        for Flight_Tuple in PNR_to_Feasible_Flights(g,PNR_to_Flight_Object,PNR):
            cabins_tuple = get_flight_cabin_mappings(Flight_Tuple)
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('A','B')
                objective.SetCoefficient(X[(PNR,Flight_Tuple,cabin)],cost_function(PNR,Flight_Tuple,cabin))
                objective.SetCoefficient((Y[(PNR, Flight_Tuple,cabin)]),cost_function(PNR,None,None))
                

    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    # Checking if a solution exists
    if status == pywraplp.Solver.OPTIMAL:
        # Extract the solution
        result = {'Total Cost': objective.Value(), 'Assignments': []}
        for PNR in PNR_List:
            for Flight_Tuple in PNR_to_Feasible_Flights(g,PNR_to_Flight_Object,PNR):
                cabins_tuple = get_flight_cabin_mappings(Flight_Tuple)
                for cabin in cabins_tuple:
                    # cabin is a tuple Eg: ('A','B')
                    if X[(PNR,Flight_Tuple,cabin)].solution_value() == 1:
                        result['Assignments'].append((PNR, Flight_Tuple, cabin))
        print()
        print(len(result['Assignments']))
        return result
    
    else:
        return "The problem does not have an optimal solution."

pnr_list = extract_PNR_from_CSV("./Dataset/passenger_pnr_dataset.csv")
all_flights = extract_Flights_from_CSV("./Dataset/flight_schedule_dataset.csv")

passenger_pnr_path = 'passenger_pnr_dataset.csv'
flight_schedule_path = 'flight_schedule_dataset.csv'

# print(pnr_list)
# print(all_flights)
# print()
# print()
# print()
# Call the optimization function
result = optimize_flight_assignments(pnr_list, all_flights)

print(result)