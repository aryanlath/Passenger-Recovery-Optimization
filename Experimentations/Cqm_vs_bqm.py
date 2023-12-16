from utils import *
from collections import defaultdict
from feasible_flights import *
from cost_function import *
import time
import os
from dwave.preprocessing.presolve import Presolver
from handle_city_pairs import *
import dimod
from dwave.system import LeapHybridCQMSampler
from dwave.system import LeapHybridBQMSampler
from dotenv import load_dotenv
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



def quantum_optimize_flight_assignments_bqm(PNR_List,QSol_count=3,city_pairs = False):
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
    X_PNR_Constraint_1 = defaultdict(list)
    X_Flight_Capacity_Constraint_1 = defaultdict(lambda: defaultdict(list))
    # PNR_to_FeasibleFlights_map=manager.dict()
    #
    # X_ijk = 1 if the ith PNR is assigned to the jth flight's kth class
    # Variables
    X = {}
    
    variable_cnt=0
    PNR_to_FeasibleFlights_map={}
    my_dict = {}
    dp={}
    test_dict = {}
    start = time.time()
    if not city_pairs:
        for PNR in PNR_List:
            PNR_to_Feasible_Flights(g,all_flights,PNR,PNR_to_FeasibleFlights_map,dp)
    
    else :
        for PNR in PNR_List:
            old_arrival_city = all_flights[PNR.inv_list[-1]].arrival_city
            proposed_arrival_cities = get_city_pairs_cost(old_arrival_city)
            for city in proposed_arrival_cities:
                PNR_to_Feasible_Flights(g,all_flights,PNR,PNR_to_FeasibleFlights_map,dp,3,city[0])
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
                test_dict[(PNR,FT,cabin)] = variable_cnt
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

    CQM.set_objective(-1*CQM_obj)
    BQM , invert = dimod.cqm_to_bqm(CQM)
    # sampleset_bqm = dimod.ExactSolver().sample(BQM)
    
    # print("####################\n",invert(sampleset_bqm),"\n\n\n\n\n\n\n\n")
    cqm_file = CQM.to_file()
    # presolve = Presolver(CQM)
    # presolve.apply()
    # reduced_cqm = presolve.detach_model()
    start_api = time.time()
    sampler = LeapHybridBQMSampler(token=dwave_token)  
    end_time_api = time.time()
    print("API CALL Time " ,end_time_api - start_api)     
    # sampler = LeapHybridCQMSampler(token=dwave_token)  
    # sampler_bqm =LeapHybridBQMSampler(token=dwave_token)
    # print(sampler.properties)
    # print(sampler.properties["minimum_time_limit"]) 
    print("Sampler Min Time: ",sampler.min_time_limit(BQM))
    start_sampling_time= time.time()
    sampleset = sampler.sample(BQM).aggregate()
    end_sampling_time = time.time()
    print("Total sampling time " , end_sampling_time - start_sampling_time)
    print("\n\n\n\nQPU ACCESS TIME" ,sampleset.info["qpu_access_time"])
    # print(invert(sampleset.first.saml))
    # dwave.inspector.show(sampleset, block=dwave.inspector.Block.FOREVER)
    start_agg = time.time()
    # feasible_sampleset = sampleset.filter(lambda row: row.is_feasible) 
    feasible_sampleset = sampleset
    end_agg = time.time()
    print("TYPE OF SAMPLESET IS " , type(sampleset) )  
    # dwave.inspector.show_qmi(CQM,feasible_sampleset.first.sample)
    print("Total Filter time " , end_agg - start_agg)
    print("{} feasible solutions of {}.".format(len(feasible_sampleset), len(sampleset)))    
    best = feasible_sampleset.first.sample  
    print(invert(best))
    # print("##############################################\n\n")
    # print(best) 
    # Aggregated_sampleset = feasible_sampleset.aggregate()
    print("Total No. of Quantum Solutions are " , len(feasible_sampleset))
    solution_count= 0 
    Final_Quantum_Solutions =[]
    for idx,sample in enumerate(feasible_sampleset.truncate(QSol_count)):
        # print("NEXT SOLUTION\n") 
        sample1 = invert(sample)
        if(idx >=QSol_count):
            break
        Final_Quantum_Solutions.append(sample1)
    for idx,solution in enumerate(Final_Quantum_Solutions):

        for PNR in PNR_List:
            for FT in PNR_to_FeasibleFlights_map[PNR.pnr_number]:
                cabins_tuple = list(get_flight_cabin_mappings(FT))
                for cabin in cabins_tuple:
                    if solution[f'X_{test_dict[(PNR,FT,cabin)]}'] == 1.0 :
                        X_PNR_Constraint_1[PNR].append(1)
                    else :
                        X_PNR_Constraint_1[PNR].append(0)
                for flight_index,flight in enumerate(FT): 
                    for cabin in cabins_tuple:
                            if solution[f'X_{test_dict[(PNR,FT,cabin)]}'] ==1.0:
                                X_Flight_Capacity_Constraint_1[flight][cabin[flight_index]].append(PNR.PAX)
                            else:
                                X_Flight_Capacity_Constraint_1[flight][cabin[flight_index]].append(0)
    
        for PNR in PNR_List :
            if(len(X_PNR_Constraint_1[PNR])==0):
                continue
            if sum(X_PNR_Constraint_1[PNR]) > 1 :
                print("std:: BadAlloc \n\n\n\n core dumped segmentation fault oc dhanesh\n\n\n")
                exit()
        for Flight, constraint_dic in X_Flight_Capacity_Constraint_1.items():
            for cabin, cabin_list in constraint_dic.items():
                if sum(cabin_list) > Flight.get_capacity(cabin):
                    print("std:: BadAlloc \n\n\n\n core dumped segmentation fault oc sreehari\n\n\n")
                    exit()
    start_cost_cal = time.time()
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
                        if idx==0:
                            for index, flights in enumerate(FT):
                                if cabin[index] == 'FC':
                                    flights.fc_available_inventory-=PNR.PAX
                                elif cabin[index] == 'PC':
                                    flights.pc_available_inventory-=PNR.PAX
                                elif cabin[index] == 'EC':
                                    flights.ec_available_inventory-=PNR.PAX
                                else:
                                    flights.bc_available_inventory-= PNR.PAX
                        temp_result['Assignments'].append((PNR, FT, cabin))
                        # assigned_pnrs[idx].add(PNR.pnr_number)
                        Assigned= True
                    variable_cnt += 1
                    
            if not Assigned:
                temp_result['Non Assignments'].append(PNR)
        result.append(temp_result)
    return result