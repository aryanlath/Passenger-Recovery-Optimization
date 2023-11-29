import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from utils import *
from Models.Flights import Flight
from collections import defaultdict
from feasible_flights import *
from cost_function import *
all_flights =[]
import pprint 
pp = pprint.PrettyPrinter(indent=4)

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

def optimize_flight_assignments(PNR_List):
    g=create_flight_graph()
    all_flights, pnr_objects,_ = init_FlightNumber_to_Flight_Object()
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
    objective = gp.LinExpr(0)

    X_PNR_Constraint = defaultdict(list)
    #
    X_Flight_Capacity_Constraint = defaultdict(lambda: defaultdict(list))
    # Variables
    # X_ijk = 1 if the ith PNR is assigned to the jth flight's kth class
    X = {}
    Y = {} # Store the complements of X
    # PNR_to_Feasible_Flights now returns a list of tuples of flight objects 
    # Ex. [(Flight1),(Flight1->Flight2),(Flight3)]
    i=0
    for PNR in PNR_List:
        for FT in PNR_to_Feasible_Flights(g,all_flights,PNR):
            cabins_tuple = list(get_flight_cabin_mappings(FT))
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('A','B')
                X[(PNR,FT,cabin)] = model.addVar(vtype=GRB.BINARY, name=f'X_i')
                Y[(PNR,FT,cabin)] = model.addVar(vtype=GRB.BINARY, name=f'Y_i')
                i+=1
                model.addConstr(X[(PNR,FT,cabin)]+Y[(PNR,FT,cabin)]==1)
                X_PNR_Constraint[PNR].append(X[(PNR,FT,cabin)])

            for flight_index,flight in enumerate(FT): # Flight is a object
                for cabin in cabins_tuple: # cabin is a tuple Eg: ('A','B') and cabins_tuple = list of cabins
                        print("hehe",cabin[flight_index])
                        X_Flight_Capacity_Constraint[flight][cabin[flight_index]].append(X[(PNR, FT, cabin)] * PNR.PAX)

    print("##################################################")
    print("Debug")
    print(X_Flight_Capacity_Constraint['1000','A'])
    print(X_Flight_Capacity_Constraint['1000','F'])
    print()
    print(X_Flight_Capacity_Constraint['1001','A'])
    print(X_Flight_Capacity_Constraint['1001','F'])
    print()
    print(X_Flight_Capacity_Constraint['1002','A'])
    print(X_Flight_Capacity_Constraint['1001','F'])
    print("##################################################")
    # Constraints
    # Each PNR can be assigned to only one flight class
    for PNR in PNR_List :
        model.addConstr(sum(X_PNR_Constraint[PNR]) <= 1)
        # Penalise non assignment costs (-M(1-sigma(Xi))) - For each PNR
        Non_assignment_Cost = cost_function(PNR,None,None)
        objective+= Non_assignment_Cost - Non_assignment_Cost*sum(X_PNR_Constraint[PNR])

    # The number of assigned passengers should not exceed available seats
    for Flight, constraint_dic in X_Flight_Capacity_Constraint.items():
        for cabin, cabin_list in constraint_dic.items():
            model.addConstr(sum(cabin_list) <= Flight.cabins[cabin])


    for PNR in PNR_List:
        for FT in PNR_to_Feasible_Flights(g,all_flights,PNR):
            cabins_tuple = get_flight_cabin_mappings(FT)
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('A', 'B')
                X_coeff = cost_function(PNR, FT, cabin)
                objective += X_coeff*X[(PNR,FT,cabin)]

    # Set the objective to maximize
    model.setObjective(objective,GRB.MAXIMIZE)
    model.optimize()

    # Checking if a solution exists
    if model.status == GRB.OPTIMAL:
        # Extract the solution
        result = {'Total Cost': model.objVal, 'Assignments': [],'Non Assignments':[]}
        # set to keep track of assigned PNRs
        assigned_pnrs = set()
        not_assigned_pnrs = set()
        for PNR in PNR_List:
            for FT in PNR_to_Feasible_Flights(g,all_flights,PNR):
                cabins_tuple = get_flight_cabin_mappings(FT)
                for cabin in cabins_tuple:
                    # cabin is a tuple Eg: ('A', 'B')
                    if X[(PNR, FT, cabin)].x == 1:
                        result['Assignments'].append((PNR, FT, cabin))
                        assigned_pnrs.add(PNR.pnr_number)
        for PNR in PNR_List:
            for FT in PNR_to_Feasible_Flights(g,all_flights,PNR):
                cabins_tuple = get_flight_cabin_mappings(FT)
                for cabin in cabins_tuple:
                    # cabin is a tuple Eg: ('A', 'B')
                    if X[(PNR, FT, cabin)].x == 0:
                        if PNR.pnr_number not in assigned_pnrs and PNR.pnr_number not in not_assigned_pnrs:
                            result['Non Assignments'].append(PNR)
                            not_assigned_pnrs.add(PNR.pnr_number)

        return result
    else:
        return "The problem does not have an optimal solution."

all_flights,pnr_list,_ = init_FlightNumber_to_Flight_Object()


passenger_pnr_path = 'passenger_pnr_dataset.csv'
flight_schedule_path = 'flight_schedule_dataset.csv'


# Identify the impacted PNRs
Impacted_PNR = Get_Impacted_passengers(all_flights,pnr_list)

print("Total impacted Passengers: ",len(Impacted_PNR))
pp.pprint(Impacted_PNR)
result = optimize_flight_assignments(Impacted_PNR)
print("Total Reassigned: ",len(result['Assignments']))

pp.pprint(result['Assignments'])
print("Not Assigned PNRs: ")
pp.pprint(result['Non Assignments'])