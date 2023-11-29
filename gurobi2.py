import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from utils import *
from Models.Flights import Flight
from collections import defaultdict
from feasible_flights import *
from cost_function import *
all_flights =[]

def get_flight_cabin_mappings(flights, current_mapping=None, flight_index=0):
    """
    To generate the tuple of all possible cabin Mappings.
    Takes FT as input
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
    # solver = pywraplp.Solver.CreateSolver('SCIP')

    # if not solver:
    #     return "No solver available."
    model = gp.Model()

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
        for FT in PNR_to_Feasible_Flights(g,PNR_to_Flight_Object,PNR):
            cabins_tuple = get_flight_cabin_mappings(FT)
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('A','B')
                X[(PNR,FT,cabin)] = model.addVar(vtype=GRB.BINARY, name=f'X_{PNR}_{FT}_{cabin}')
                Y[(PNR,FT,cabin)] = model.addVar(vtype=GRB.BINARY, name=f'Y_{PNR}_{FT}_{cabin}')
                model.addConstr(X[(PNR,FT,cabin)]+Y[(PNR,FT,cabin)]==1)
                X_PNR_Constraint[PNR].append(X[(PNR,FT,cabin)])

            for flight in FT:
                for cabin in cabins_tuple:
                    X_Flight_Capacity_Constraint[flight][cabin].append(X[(PNR, flight, cabins_tuple)] * PNR.PAX)



          
    # Constraints
    # Each PNR can be assigned to only one flight class
    for PNR in PNR_List :
        model.addConstr(sum(X_PNR_Constraint[PNR]) <= 1)

    # The number of assigned passengers should not exceed available seats
    for Flight, constraint_dic in X_Flight_Capacity_Constraint.items():
        for cabin, cabin_list in constraint_dic.items():
            model.addConstr(sum(cabin_list) <= Flight.cabins[cabin])

    objective = gb.LinExpr()

    for PNR in PNR_List:
        for FT in PNR_to_Feasible_Flights(g, PNR_to_Flight_Object, PNR):
            cabins_tuple = get_flight_cabin_mappings(FT)
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('A', 'B')
                X_coeff = cost_function(PNR, FT, cabin)
                Y_coeff = cost_function(PNR, None, None)
                
                # Add coefficients to the objective
                objective += X[(PNR, FT, cabin)] * X_coeff
                objective += Y[(PNR, FT, cabin)] * Y_coeff

    # Set the objective to maximize
    model.setObjective(objective, gb.GRB.MAXIMIZE)
    model.optimize()

    # Checking if a solution exists
    if model.status == gb.GRB.OPTIMAL:
        # Extract the solution
        result = {'Total Cost': model.objVal, 'Assignments': []}
        for PNR in PNR_List:
            for FT in PNR_to_Feasible_Flights(g, PNR_to_Flight_Object, PNR):
                cabins_tuple = get_flight_cabin_mappings(FT)
                for cabin in cabins_tuple:
                    # cabin is a tuple Eg: ('A', 'B')
                    if X[(PNR, FT, cabin)].x == 1:
                        result['Assignments'].append((PNR, FT, cabin))
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