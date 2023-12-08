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
from dwave.preprocessing.presolve import Presolver
from handle_city_pairs import *
import multiprocessing
import dimod
from dwave.system import LeapHybridCQMSampler
# import dwave.inspector
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

def quantum_optimize_flight_assignments(PNR_List,QSol_count=3,city_pairs = False):
    g=create_flight_graph()
    all_flights, _,_ ,_= Get_All_Maps()
    """
        input: List of Impacted PNR objects, optional: city_pairs bool to tell if we have to include city pairs or not
        returns: list of result dictionaries containing Assignments, Non assignments and costs
    """
    # Creating CQM model from dimod
    CQM=dimod.ConstrainedQuadraticModel()
    CQM_obj = 0
    X_PNR_Constraint = defaultdict(list)
    X_Flight_Capacity_Constraint = defaultdict(lambda: defaultdict(list))

    # PNR_to_FeasibleFlights_map=manager.dict()
    #
    # X_ijk = 1 if the ith PNR is assigned to the jth flight's kth class
    # Variables
    X = {}
    
    variable_cnt=0
    PNR_to_FeasibleFlights_map={}
    my_dict = {}
    dp={}
    start = time.time()
    if not city_pairs:
        for PNR in PNR_List:
            PNR_to_Feasible_Flights(g,all_flights,PNR,PNR_to_FeasibleFlights_map,dp)
    
    else :
        for PNR in PNR_List:
            old_arrival_city = all_flights[PNR.inv_list[-1]].arrival_city
            proposed_arrival_cities = get_city_pairs_cost(old_arrival_city)
            for city in proposed_arrival_cities:
                PNR_to_Feasible_Flights(g,all_flights,PNR,PNR_to_FeasibleFlights_map,dp,4,city[0])
    end = time.time()
    print("Feasible Flights Time: ", end-start)

    start = time.time()
    for PNR in PNR_List:
        for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
            cabins_tuple = list(get_flight_cabin_mappings(FT))
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('FC','PC')
                X[(PNR,FT,cabin)] = dimod.Binary(f'X_{variable_cnt}')
                my_dict[f'X_{variable_cnt}'] = (PNR,FT,cabin)
                # X[(PNR,FT,cabin)] = model.addVar(vtype=GRB.BINARY, name=f'X_{i}')
                variable_cnt+=1
                X_PNR_Constraint[PNR].append(X[(PNR,FT,cabin)])

            for flight_index,flight in enumerate(FT): # Flight is a object
                for cabin in cabins_tuple: # cabin is a tuple Eg:  ('FC','PC') and cabins_tuple = list of cabins
                        X_Flight_Capacity_Constraint[flight][cabin[flight_index]].append(X[(PNR, FT, cabin)] * PNR.PAX)

    end = time.time()
    print("Variables creation time: ", end-start)

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
            CQM.add_constraint(sum(cabin_list) <= Flight.get_capacity(cabin))

    end = time.time()
    print("Adding Constraints time: ", end-start)

    for PNR in PNR_List:
        for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
            cabins_tuple = get_flight_cabin_mappings(FT)
            for cabin in cabins_tuple:
                # cabin is a tuple Eg: ('FC', 'PC')
                X_coeff = cost_function(PNR, FT, cabin)
                CQM_obj += X_coeff*X[(PNR,FT,cabin)]

    start = time.time()
    CQM.set_objective(-1*CQM_obj)
    presolve = Presolver(CQM)
    presolve.apply()
    reduced_cqm = presolve.detach_model()
    sampler = LeapHybridCQMSampler(token=dwave_token)    
    sampleset = sampler.sample_cqm(reduced_cqm).aggregate()
    end_time_sampling = time.time()
    print("API CALL Time " ,end_time_sampling - start)     
    start_agg = time.time()
    feasible_sampleset = sampleset.filter(lambda row: row.is_feasible) 
    end_agg = time.time()
    print("TYPE OF SAMPLESET IS " , type(sampleset) )  
    # dwave.inspector.show_qmi(CQM,feasible_sampleset.first.sample)
    print("Total Filter time " , end_agg - start_agg)
    print("{} feasible solutions of {}.".format(len(feasible_sampleset), len(sampleset)))    
    best = feasible_sampleset.first.sample   
    # Aggregated_sampleset = feasible_sampleset.aggregate()
    print("Total No. of Quantum Solutions are " , len(feasible_sampleset))
    solution_count= 0 
    Final_Quantum_Solutions =[]
    for idx,sample in enumerate(feasible_sampleset.truncate(QSol_count)):
        # print("NEXT SOLUTION\n") 
        if(idx >=QSol_count):
            break
        Final_Quantum_Solutions.append(sample)
    start_cost_cal = time.time()
    print("Total sampling time " , start_cost_cal - start)
    Objective_Value_List =[0]*QSol_count
    variable_cnt=0
    for PNR in PNR_List:
        is_PNR_assigned = [False]*QSol_count
        for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
            cabins_tuple = get_flight_cabin_mappings(FT)
            for cabin in cabins_tuple:
                for idx,solution in enumerate(Final_Quantum_Solutions):
                    if solution[f'X_{variable_cnt}'] == 1.0:
                        X_coeff = cost_function(PNR, FT, cabin)
                        Objective_Value_List[idx] += X_coeff
                        is_PNR_assigned[idx] = True
                variable_cnt += 1
        for idx,check_assigned in enumerate(is_PNR_assigned):
            if not is_PNR_assigned[idx]:
                Non_assignment_Cost = cost_function(PNR, None, None)
                Objective_Value_List[idx] += Non_assignment_Cost 
    end_cost_cal = time.time()
    print("Total Obj Function calculation time" , end_cost_cal - start_cost_cal)
    print(f"Objective Value List of top {QSol_count} quantum solutions is: \n", Objective_Value_List)    
    result = []
    print("RESULT LENGTH " ,len(result))
    # set to keep track of assigned PNRs
    for idx,solution in enumerate(Final_Quantum_Solutions):
        variable_cnt=0
        temp_result = {'Assignments':[] , 'Non Assignments':[]}
        for PNR in PNR_List:
            Assigned = False
            for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
                cabins_tuple = get_flight_cabin_mappings(FT)
                for cabin in cabins_tuple:
                    if solution[f'X_{variable_cnt}'] == 1.0:
                        # print("THIS IS IDX " , idx)
                        # print(len(result[idx]['Assignments']))
                        temp_result['Assignments'].append((PNR, FT, cabin))
                        # assigned_pnrs[idx].add(PNR.pnr_number)
                        Assigned= True
                    variable_cnt += 1
                    
            if not Assigned:
                temp_result['Non Assignments'].append(PNR)
        result.append(temp_result)
    return result
    # for idx,solution in enumerate(Final_Quantum_Solutions):
    #     variable_cnt=0
    #     for PNR in PNR_List:
    #         for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
    #             cabins_tuple = get_flight_cabin_mappings(FT)
    #             for cabin in cabins_tuple:         
    #                 if solution[f'X_{variable_cnt}'] == 0.0:
    #                     if PNR.pnr_number not in assigned_pnrs[idx] and PNR.pnr_number not in not_assigned_pnrs[idx]:
    #                         result[idx]['Non Assignments'].append(PNR)
    #                         not_assigned_pnrs[idx].add(PNR.pnr_number)
    #                 variable_cnt += 1

    # for idx,solution in enumerate(Final_Quantum_Solutions):
    #     for PNR in PNR_List:
    #         if PNR.pnr_number not in assigned_pnrs[idx] and PNR.pnr_number not in not_assigned_pnrs[idx]:
    #             result[idx]['Non Assignments'].append(PNR)
                
    # for idx, solution in enumerate(Final_Top3_Quantum_Solutions):
    #     df_assignments = pd.DataFrame(result[idx]['Assignments'], columns=['PNR_Number', 'PNR_Email','Flight', 'Cabin'])
    #     df_non_assignments = pd.DataFrame(result[idx]['Non Assignments'], columns=['PNR'])
    
    #     df_assignments.to_csv(f"Results/assignments_{idx}.csv")
    #     df_non_assignments.to_csv(f"Results/non_assignments_{idx}.csv")
    # else:
        # return "The problem does not have an optimal solution."

    end = time.time()
    print("Solving time: ", end-start)
# all_flights,pnr_list,, = Get_All_Maps()


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
