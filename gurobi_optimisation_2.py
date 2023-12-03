import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from utils import *
from Models.Flights import Flight
from collections import defaultdict
from feasible_flights_2 import *
from cost_function import *
import time
import threading
import multiprocessing
from handle_city_pairs import *
from gurobi_optimisation import *

def optimize_flight_assignments_2(PNR_List,all_flights):
    g=create_flight_graph()
    print(PNR_List)
    """
        PNR_List = List of Impacted PNRs
        X_PNR_Constraint -> dictionary where keys are PNR objects and each value is a list of variables for that Particular PNR in its constraint
        X_Flight_Capacity_Constraint-> dictionary of dictionaries where outer keys are Flight objects and inner keys are cabins, each value is a list of variables for that Particular Flight,Cabin in its constraint
    """
    model = gp.Model()
    objective = gp.LinExpr(0)

    X_PNR_Constraint = defaultdict(list)
    #
    X_Flight_Capacity_Constraint = defaultdict(lambda: defaultdict(list))
    # Variables
    # X_ijk = 1 if the ith PNR is assigned to the jth flight's kth class
    X = {}

    # PNR_to_Feasible_Flights now returns a list of tuples of flight objects 
    # Ex. [(Flight1),(Flight1->Flight2),(Flight3)]
    # X_PNR_Constraint -> dictionary where keys are PNR objects and each value is a list of variables for that Particular PNR in its constraint
    # X_Flight_Capacity_Constraint-> dictionary of dictionaries where outer keys are Flight objects and inner keys are cabins, each value is a list of variables for that Particular Flight,Cabin in its constraint
    PNR_to_FeasibleFlights_map_2 = {}
    start=time.time()
    thread_map1={}
    thread_cnt1=0
    manager=multiprocessing.Manager()
    PNR_to_FeasibleFlights_map_2=manager.dict()

    for PNR in PNR_List:
        #print(PNR.pnr_number)
        old_arrival_city = all_flights[PNR.inv_list[-1]].arrival_city
        proposed_arrival_cities = get_city_pairs_cost(old_arrival_city)
        #print(old_arrival_city)
        for city in proposed_arrival_cities:

            thread_map1[thread_cnt1]=multiprocessing.Process(target=PNR_to_Feasible_Flights_2,args=(g,all_flights,PNR,PNR_to_FeasibleFlights_map_2,4,city[0]))
            thread_map1[thread_cnt1].start()
            thread_cnt1+=1

    for i in range(thread_cnt1):
        thread_map1[i].join()
    end = time.time()
    print("Threading time: ", end-start)
    start = time.time()
    i=0
    for PNR in PNR_List:
        for FT in PNR_to_FeasibleFlights_map_2[PNR.pnr_number]:
            cabins_tuple = list(get_flight_cabin_mappings(FT))
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('FC','PC')
                X[(PNR,FT,cabin)] = model.addVar(vtype=GRB.BINARY, name=f'X_{i}')
                i+=1
                X_PNR_Constraint[PNR].append(X[(PNR,FT,cabin)])

            for flight_index,flight in enumerate(FT): # Flight is a object
                for cabin in cabins_tuple: # cabin is a tuple Eg:  ('FC','PC') and cabins_tuple = list of cabins
                        X_Flight_Capacity_Constraint[flight][cabin[flight_index]].append(X[(PNR, FT, cabin)] * PNR.PAX)

    end = time.time()
    print("Creating variables: ", end-start)

    start = time.time()
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
            model.addConstr(sum(cabin_list) <= Flight.get_capacity(cabin))

    end = time.time()
    print("Constraints time: ", end-start)

    for PNR in PNR_List:
        for FT in PNR_to_FeasibleFlights_map_2[PNR.pnr_number]:
            cabins_tuple = get_flight_cabin_mappings(FT)
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('FC', 'PC')
                X_coeff = cost_function(PNR, FT, cabin)
                objective += X_coeff*X[(PNR,FT,cabin)]

    start = time.time()
    # Set the objective to maximize
    model.setObjective(objective,GRB.MAXIMIZE)
    model.optimize()

    # model.write("try.lp") # To Print the soln in a file

    # Checking if a solution exists
    if model.status == GRB.OPTIMAL:
        # Extract the solution
        result = {'Total Cost': model.objVal, 'Assignments': [],'Non Assignments':[]}
        # set to keep track of assigned PNRs
        assigned_pnrs = set()
        not_assigned_pnrs = set()
        for PNR in PNR_List:
            for FT in PNR_to_FeasibleFlights_map_2[PNR.pnr_number]:
                cabins_tuple = get_flight_cabin_mappings(FT)
                for cabin in cabins_tuple:
                     # cabin is a tuple Eg: ('FC', 'PC')
                    if X[(PNR, FT, cabin)].x == 1:
                        result['Assignments'].append((PNR, FT, cabin))
                        assigned_pnrs.add(PNR.pnr_number)
    
        for PNR in PNR_List:
            for FT in PNR_to_FeasibleFlights_map_2[PNR.pnr_number]:
                cabins_tuple = get_flight_cabin_mappings(FT)
                for cabin in cabins_tuple:
                    # cabin is a tuple Eg: ('A', 'B')
                    (X[(PNR, FT, cabin)].VarName,"=",X[(PNR, FT, cabin)].x)
                    if X[(PNR, FT, cabin)].x == 0:
                        if PNR.pnr_number not in assigned_pnrs and PNR.pnr_number not in not_assigned_pnrs:
                            result['Non Assignments'].append(PNR)
                            not_assigned_pnrs.add(PNR.pnr_number)
        for pnr in PNR_List:
            if pnr.pnr_number not in assigned_pnrs and pnr.pnr_number not in not_assigned_pnrs:
                result['Non Assignments'].append(pnr)
        return result
    else:
        return "The problem does not have an optimal solution."

    end = time.time()
    print("Solving time: ", end-start)
