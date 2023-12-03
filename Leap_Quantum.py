import pandas as pd
import gurobipy as gp
from gurobipy import GRB
from utils import *
from Models.Flights import Flight
from collections import defaultdict
from feasible_flights import *
from cost_function import *
import time
import os
import threading
import multiprocessing
import dimod
from dwave.system import LeapHybridCQMSampler
from dimod import ConstrainedQuadraticModel, BinaryQuadraticModel, QuadraticModel
from dimod import Real
all_flights =[]
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the API key
dwave_token = os.getenv('DWAVE_TOKEN')

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
        current_mapping.append((flight.inventory_id, cabin))
        yield from get_flight_cabin_mappings(flights, current_mapping, flight_index + 1)
        current_mapping.pop()

def quantum_optimize_flight_assignments(PNR_List):
    g=create_flight_graph()
    all_flights, pnr_objects,_ ,_= Get_All_Maps()
    """
        PNR_List = List of Impacted PNRs
        X_PNR_Constraint -> dictionary where keys are PNR objects and each value is a list of variables for that Particular PNR in its constraint
        X_Flight_Capacity_Constraint-> dictionary of dictionaries where outer keys are Flight objects and inner keys are cabins, each value is a list of variables for that Particular Flight,Cabin in its constraint
    """
    # model = gp.Model()
    # objective = gp.LinExpr(0)
    CQM=dimod.ConstrainedQuadraticModel()
    CQM_obj = 0
    X_PNR_Constraint = defaultdict(list)
    #
    X_Flight_Capacity_Constraint = defaultdict(lambda: defaultdict(list))
    # Variables
    # X_ijk = 1 if the ith PNR is assigned to the jth flight's kth class
    X = {}
    my_dict = {}
    # PNR_to_Feasible_Flights now returns a list of tuples of flight objects 
    # Ex. [(Flight1),(Flight1->Flight2),(Flight3)]
    # X_PNR_Constraint -> dictionary where keys are PNR objects and each value is a list of variables for that Particular PNR in its constraint
    # X_Flight_Capacity_Constraint-> dictionary of dictionaries where outer keys are Flight objects and inner keys are cabins, each value is a list of variables for that Particular Flight,Cabin in its constraint
    i=0
    thread_map={}
    thread_cnt=0
    manager=multiprocessing.Manager()
    PNR_to_FeasibleFlights_map=manager.dict()
    start = time.time()
    for PNR in PNR_List:
        thread_map[thread_cnt]=multiprocessing.Process(target=PNR_to_Feasible_Flights,args=(g,all_flights,PNR,PNR_to_FeasibleFlights_map))
        thread_map[thread_cnt].start()
        thread_cnt+=1
        # PNR_to_Feasible_Flights(g,all_flights,PNR,PNR_to_FeasibleFlights_map)
    for cnt in range(thread_cnt):
        thread_map[cnt].join()
    pp.pprint(PNR_to_FeasibleFlights_map)
    
    end = time.time()
    print("Without Threading time: ", end-start)

    start = time.time()
    for PNR in PNR_List:
        for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
            cabins_tuple = list(get_flight_cabin_mappings(FT))
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('FC','PC')
                X[(PNR,FT,cabin)] = dimod.Binary(f'X_{i}')
                my_dict[f'X_{i}'] = (PNR,FT,cabin)
                # X[(PNR,FT,cabin)] = model.addVar(vtype=GRB.BINARY, name=f'X_{i}')
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
        if(len(X_PNR_Constraint[PNR])==0):
            continue
        CQM.add_constraint(sum(X_PNR_Constraint[PNR]) <= 1)
        # model.addConstr(sum(X_PNR_Constraint[PNR]) <= 1)
        # Penalise non assignment costs (-M(1-sigma(Xi))) - For each PNR
        Non_assignment_Cost = cost_function(PNR,None,None)
        CQM_obj += Non_assignment_Cost - Non_assignment_Cost*sum(X_PNR_Constraint[PNR])

    # The number of assigned passengers should not exceed available seats
    for Flight, constraint_dic in X_Flight_Capacity_Constraint.items():
        for cabin, cabin_list in constraint_dic.items():
            # model.addConstr(sum(cabin_list) <= Flight.get_capacity(cabin))
            CQM.add_constraint(sum(cabin_list) <= Flight.get_capacity(cabin))

    end = time.time()
    print("Constraints time: ", end-start)

    for PNR in PNR_List:
        for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
            cabins_tuple = get_flight_cabin_mappings(FT)
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('FC', 'PC')
                X_coeff = cost_function(PNR, FT, cabin)
                CQM_obj += X_coeff*X[(PNR,FT,cabin)]

    start = time.time()
    # Set the objective to maximize
    # model.setObjective(objective,GRB.MAXIMIZE)
    # model.optimize()
    CQM.set_objective(-1*CQM_obj)
    sampler = LeapHybridCQMSampler(token=dwave_token)    
    sampleset = sampler.sample_cqm(CQM)       
    feasible_sampleset = sampleset.filter(lambda row: row.is_feasible) 
    print("{} feasible solutions of {}.".format(len(feasible_sampleset), len(sampleset)))    
    best = feasible_sampleset.first.sample   
    # best = feasible_sampleset.first.sample  
    Aggregated_sampleset = feasible_sampleset.aggregate()
    print("Total No. of Quantum Solutions are " , len(Aggregated_sampleset))
    for sample in Aggregated_sampleset.samples():
        print("NEXT SOLUTION\n") 
        for key,val in sample.items():
            if(val==1.0):
                print(key," = ", val ,my_dict[key])
    
    objective_value = 0
    i=0
    for PNR in PNR_List:
        is_PNR_assigned = False
        for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
            cabins_tuple = get_flight_cabin_mappings(FT)
            for cabin in cabins_tuple:
                X_coeff = cost_function(PNR, FT, cabin)
                if best[f'X_{i}'] == 1.0:
                    objective_value += X_coeff
                    is_PNR_assigned = True
                i += 1
        if not is_PNR_assigned:
          Non_assignment_Cost = cost_function(PNR, None, None)
          objective_value += Non_assignment_Cost - Non_assignment_Cost * sum(X_PNR_Constraint[PNR])
    # Print or return the objective value
    print("Objective Value: \n", objective_value)    
    # best = feasible_sampleset.first.sample
    # model.write("try.lp") # To Print the soln in a file

    # Checking if a solution exists
    # if model.status == GRB.OPTIMAL:
        # Extract the solution
    result = {'Assignments': [],'Non Assignments':[]}
    # set to keep track of assigned PNRs
    assigned_pnrs = set()
    not_assigned_pnrs = set()
    i=0
    for PNR in PNR_List:
        for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
            cabins_tuple = get_flight_cabin_mappings(FT)
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('FC', 'PC')
                if best[f'X_{i}'] == 1:
                    result['Assignments'].append((PNR.pnr_number,PNR.email_id, FT, cabin))
                    assigned_pnrs.add(PNR.pnr_number)
                i+=1
    i=0
    for PNR in PNR_List:
        for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
            cabins_tuple = get_flight_cabin_mappings(FT)
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('A', 'B')
                # print(X[(PNR, FT, cabin)].VarName,"=",X[(PNR, FT, cabin)].x)
                if best[f'X_{i}'] == 0:
                    if PNR.pnr_number not in assigned_pnrs and PNR.pnr_number not in not_assigned_pnrs:
                        result['Non Assignments'].append(PNR)
                        not_assigned_pnrs.add(PNR.pnr_number)
                i+=1
    for pnr in PNR_List:
        if pnr.pnr_number not in assigned_pnrs and pnr.pnr_number not in not_assigned_pnrs:
            result['Non Assignments'].append(pnr.pnr_number)
    df_assignments = pd.DataFrame(result['Assignments'], columns=['PNR_Number', 'PNR_Email','Flight', 'Cabin'])
    df_non_assignments = pd.DataFrame(result['Non Assignments'], columns=['PNR'])
    # with pd.ExcelWriter(output_file) as writer:
    df_assignments.to_csv("assignments.csv")
    df_non_assignments.to_csv("non_assignments.csv")
    return result
    # else:
        # return "The problem does not have an optimal solution."

    end = time.time()
    print("Solving time: ", end-start)
# all_flights,pnr_list,_,_ = Get_All_Maps()


# passenger_pnr_path = 'passenger_pnr_dataset.csv'
# flight_schedule_path = 'flight_schedule_dataset.csv'


# # Identify the impacted PNRs
# Impacted_PNR = Get_Impacted_passengers(all_flights,pnr_list)
# print("Total impacted Passengers: ",len(Impacted_PNR))
# pp.pprint(Impacted_PNR)
# result = optimize_flight_assignments(Impacted_PNR)
# print("Total Reassigned: ",len(result['Assignments']))

# pp.pprint(result['Assignments'])
# print("Not Assigned PNRs: ")
# pp.pprint(result['Non Assignments'])