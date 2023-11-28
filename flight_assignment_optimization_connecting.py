
import pandas as pd
from ortools.linear_solver import pywraplp
from utils import *
from Models.Flights import Flight
from collections import defaultdict
from feasible_flights import *
from cost_function import *
all_flights =[]
# def PNR_to_Feasible_Flights(PNR_Object, all_flights):
#     pass 

def optimize_flight_assignments(PNR_List , all_flights):
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
    
    # PNR_to_Feasible_Flights now returns a list of tuples of flight objects 
    # Ex. [(Flight1),(Flight1->Flight2),(Flight3)]
    for PNR in PNR_List:
        for Flight_Tuple in PNR_to_Feasible_Flights(PNR):
            if(len(Flight_Tuple)==1):
                for cabin,cabin_capacity in Flight_Tuple[0].cabins.items():
                    X[(PNR,Flight_Tuple,cabin)] = solver.BoolVar(f'X[{PNR},{Flight_Tuple},{cabin}]')
                    X_PNR_Constraint[PNR].append(X[(PNR,Flight_Tuple,cabin)])
                    X_Flight_Capacity_Constraint[Flight_Tuple[0]][cabin].append(X[(PNR,Flight_Tuple,cabin)]*PNR.PAX)
            else:
                for cabin1,cabin_capacity1 in Flight_Tuple[0].cabins.items() :
                    for cabin2,cabin_capacity2 in Flight_Tuple[1].cabins.items():
                        X[(PNR, Flight_Tuple, cabin1,cabin2)] = solver.BoolVar(f'X[{PNR},{Flight_Tuple},{cabin1},{cabin2}]')
                        X_PNR_Constraint[PNR].append(X[(PNR,Flight_Tuple,cabin1,cabin2)])
                        X_Flight_Capacity_Constraint[Flight_Tuple[0]][cabin1].append(X[(PNR,Flight_Tuple,cabin1,cabin2)]*PNR.PAX)
                        X_Flight_Capacity_Constraint[Flight_Tuple[1]][cabin2].append(X[(PNR,Flight_Tuple,cabin1,cabin2)]*PNR.PAX)
          
    # Constraints
    # Each PNR can be assigned to only one flight class
    for PNR in PNR_List :
        solver.Add(sum(X_PNR_Constraint[PNR]) <= 1)
        # solver.Add(sum(X[PNR, Flight, cabin] for Flight in PNR_to_Feasible_Flights(PNR) for cabin,cabin_capacity in Flight.cabins.items()) == 1)

    # The number of assigned passengers should not exceed available seats
    for Flight, constraint_dic in X_Flight_Capacity_Constraint.items():
        for cabin, cabin_list in constraint_dic.items():
            solver.Add(sum(cabin_list) <= Flight.cabins[cabin])
    # Objective
    # Minimize the total cost
    objective = solver.Objective()

        
    for PNR in PNR_List:
        for Flight_Tuple in PNR_to_Feasible_Flights(PNR):
            if(len(Flight_Tuple)==1):
                for cabin,cabin_capacity in Flight_Tuple[0].cabins.items():
                    objective.SetCoefficient(X[(PNR,Flight_Tuple,cabin)],cost_function(PNR,Flight_Tuple,cabin,None))
            else:
                for cabin1,cabin_capacity1 in Flight_Tuple[0].cabins.items() :
                    for cabin2,cabin_capacity2 in Flight_Tuple[1].cabins.items():
                        objective.SetCoefficient(X[((PNR,Flight_Tuple,cabin1,cabin2))],cost_function(PNR,Flight_Tuple,cabin1,cabin2))
                        X[(PNR, Flight_Tuple, cabin1,cabin2)] = solver.BoolVar(f'X[{PNR},{Flight_Tuple},{cabin1},{cabin2}]')

    objective.SetMaximization()

    # Solve the problem
    status = solver.Solve()

    # Checking if a solution exists
    if status == pywraplp.Solver.OPTIMAL:
        # Extract the solution
        result = {'Total Cost': objective.Value(), 'Assignments': []}
        for PNR in PNR_List:
            for Flight_Tuple in PNR_to_Feasible_Flights(PNR):
                if(len(Flight_Tuple)==1):
                    for cabin,cabin_capacity in Flight.cabins.items():
                        if X[(PNR, Flight_Tuple, cabin)].solution_value() > 0.5:  # If assigned
                            result['Assignments'].append((PNR, Flight_Tuple, cabin))
                else:
                    for cabin1,cabin_capacity1 in Flight_Tuple[0].cabins.items():
                        for cabin2,cabin_capacity2 in Flight_Tuple[1].cabins.items():
                            if(X[(PNR,Flight_Tuple,cabin1,cabin2)].solution_value()>0.5):
                                result['Assignments'].append((PNR,Flight_Tuple,cabin1,cabin2))
        return result
    else:
        return "The problem does not have an optimal solution."

pnr_list = extract_PNR_from_CSV("./Dataset/passenger_pnr_dataset.csv")
all_flights = extract_Flights_from_CSV("./Dataset/flight_schedule_dataset.csv")

passenger_pnr_path = 'passenger_pnr_dataset.csv'
flight_schedule_path = 'flight_schedule_dataset.csv'

print(pnr_list)
print(all_flights)
print()
print()
print()
# Call the optimization function
result = optimize_flight_assignments(pnr_list, all_flights)

print(result)
