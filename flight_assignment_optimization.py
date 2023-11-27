
import pandas as pd
from ortools.linear_solver import pywraplp
from utils import *
from Models.Flights import Flight
from feasible_flights import *
from cost_function import *
all_flights =[]
# def PNR_to_Feasible_Flights(PNR_Object, all_flights):
#     pass 

def optimize_flight_assignments(PNR_List , all_flights):
    # I = len(PNR_PAX_List)  # Number of PNRs
    # J = len(Flight_Class_Capacities)  # Number of flights, including the 'not allocated' option
    # K = len(Flight_Class_Capacities[0])  # Number of classes

    # Create the mip solver with the SCIP backend.
    solver = pywraplp.Solver.CreateSolver('SCIP')

    if not solver:
        return "No solver available."

    # Variables
    # X_ijk = 1 if the ith PNR is assigned to the jth flight's kth class
    X = {}
    for PNR in PNR_List:
        for Flight in PNR_to_Feasible_Flights(PNR):
            for cabin,cabin_capacity in Flight.cabins.items() :
                X[(PNR, Flight, cabin)] = solver.BoolVar(f'X[{PNR},{Flight},{cabin}]')

    # Constraints
    # Each PNR can be assigned to only one flight class
    for PNR in PNR_List :
        solver.Add(sum(X[PNR, Flight, cabin] for Flight in PNR_to_Feasible_Flights(PNR) for cabin,cabin_capacity in Flight.cabins.items()) == 1)

    # The number of assigned passengers should not exceed available seats
    for Flight in all_flights:  # Exclude the 'not allocated' option
        for cabin,cabin_capacity in Flight.cabins.items():
            solver.Add(sum(PNR.PAX * X.get((PNR, Flight, cabin),0) for PNR in PNR_List ) <= cabin_capacity     )

    # Objective
    # Minimize the total cost
    objective = solver.Objective()
    for PNR in PNR_List:        
        for Flight in PNR_to_Feasible_Flights(PNR):
            for cabin,cabin_capacity in Flight.cabins.items():
                objective.SetCoefficient(X[(PNR, Flight, cabin)], cost_function(PNR,Flight,cabin))
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()

    # Checking if a solution exists
    if status == pywraplp.Solver.OPTIMAL:
        # Extract the solution
        result = {'Total Cost': objective.Value(), 'Assignments': []}
        for PNR in PNR_List:
            for Flight in PNR_to_Feasible_Flights(PNR):
                for cabin,cabin_capacity in Flight.cabins.items():
                    if X[(PNR, Flight, cabin)].solution_value() > 0.5:  # If assigned
                        result['Assignments'].append((PNR, Flight, cabin))
        return result
    else:
        return "The problem does not have an optimal solution."

pnr_list = extract_PNR_from_CSV("./Dataset/passenger_pnr_dataset.csv")
all_flights = extract_Flights_from_CSV("./Dataset/flight_schedule_dataset.csv")
# Read n and b from CSV files
# def load_data(passenger_pnr_path, flight_schedule_path):
#     passenger_pnr_df = pd.read_csv(passenger_pnr_path)
#     flight_schedule_df = pd.read_csv(flight_schedule_path)

#     # Calculating n: Count of passengers for each PNR
#     n = passenger_pnr_df['PAX'].tolist()

#     # Calculating b: Remaining seats in each class for each flight
#     b = flight_schedule_df[flight_schedule_df['Status'] != 'Cancelled'][['Remaining Capacity A', 'Remaining Capacity F']].values.tolist()

#     return n, b

# Define C as needed (you may also read this from a CSV if required)
# def define_cost_matrix(I, J, K):
#     # Placeholder for the cost matrix, adjust as per your specific scenario
#     C = [[[100, 200] for _ in range(J)] for _ in range(I)]
#     return C

# Paths to the CSV files (Replace with your file paths)
passenger_pnr_path = 'passenger_pnr_dataset.csv'
flight_schedule_path = 'flight_schedule_dataset.csv'

# Load data and define cost matrix
# PNR_PAX_List, Flight_Class_Capacities = load_data(passenger_pnr_path, flight_schedule_path)
# Cost_Matrix = define_cost_matrix(len(pnr_list), len(Flight_Class_Capacities) + 1, len(Flight_Class_Capacities[0]))
print(pnr_list)
print(all_flights)
print()
print()
print()
# Call the optimization function
result = optimize_flight_assignments(pnr_list, all_flights)
print(result)
