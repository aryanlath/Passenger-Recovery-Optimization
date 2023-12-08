import numpy as np
from collections import defaultdict
import threading
from cost_function import *
import pandas as pd
from utils import *
from Models.Flights import Flight
from feasible_flights import *
import time
import os
from handle_city_pairs import *
import dimod
from dwave.system import LeapHybridCQMSampler
# import dwave.inspector
from dimod import ConstrainedQuadraticModel, BinaryQuadraticModel, QuadraticModel
from dimod import Real
from dotenv import load_dotenv
import pprint
pp = pprint.PrettyPrinter(indent=4)

assignments=defaultdict(list)
lock=threading.Lock() 
total_cost=0

# Load the .env file
load_dotenv()

# Access the API key
dwave_token = os.getenv('DWAVE_TOKEN')

def Flow(PNR_list,flight_cabin_tuple,sampler):
    CQM=dimod.ConstrainedQuadraticModel()
    CQM_obj = 0
    X_PNR_Constraint = defaultdict(list)
    X_Flight_Capacity_Constraint = defaultdict(list)
    X = {}  
    variable_cnt=0
    flight_object = flight_cabin_tuple[0]
    Cabin=flight_cabin_tuple[1]
    order=flight_cabin_tuple[2]
    my_dict={}
    if(Cabin=='FC'):
        for PNR in PNR_list:
            for key,value in flight_object.fc_class_dict.items():
                X[(PNR,key)]=dimod.Integer(f'X_{variable_cnt}')
                my_dict[f'X_{variable_cnt}'] = (PNR,key)
                X_PNR_Constraint[PNR].append(X[(PNR,key)])
                X_Flight_Capacity_Constraint[key].append(X[((PNR,key))])
                variable_cnt+=1

        # for flight_index,flight in enumerate(FT): # Flight is a object
        #         for cabin in cabins_tuple: # cabin is a tuple Eg:  ('FC','PC') and cabins_tuple = list of cabins
        #                 X_Flight_Capacity_Constraint[flight][cabin[flight_index]].append(X[(PNR, FT, cabin)] * PNR.PAX)

        for PNR in PNR_list :
            if(len(X_PNR_Constraint[PNR])==0):
                continue
            CQM.add_constraint(sum(X_PNR_Constraint[PNR]) == PNR.PAX)
        
        for key,value in flight_object.fc_class_dict.items():
            CQM.add_constraint(sum(X_Flight_Capacity_Constraint[key]) <= value)
        
    elif(Cabin=="BC"):
        for PNR in PNR_list:
            for key,value in flight_object.bc_class_dict.items():
                X[(PNR,key)]=dimod.Integer(f'X_{variable_cnt}')
                my_dict[f'X_{variable_cnt}'] = (PNR,key)
                X_PNR_Constraint[PNR].append(X[(PNR,key)])
                X_Flight_Capacity_Constraint[key].append(X[((PNR,key))])
                variable_cnt+=1

        # for flight_index,flight in enumerate(FT): # Flight is a object
        #         for cabin in cabins_tuple: # cabin is a tuple Eg:  ('FC','PC') and cabins_tuple = list of cabins
        #                 X_Flight_Capacity_Constraint[flight][cabin[flight_index]].append(X[(PNR, FT, cabin)] * PNR.PAX)

        for PNR in PNR_list :
            if(len(X_PNR_Constraint[PNR])==0):
                continue
            CQM.add_constraint(sum(X_PNR_Constraint[PNR]) == PNR.PAX)
        
        for key,value in flight_object.bc_class_dict.items():
            CQM.add_constraint(sum(X_Flight_Capacity_Constraint[key]) <= value)
    elif(Cabin=="PC"):
        for PNR in PNR_list:
            for key,value in flight_object.pc_class_dict.items():
                X[(PNR,key)]=dimod.Integer(f'X_{variable_cnt}')
                my_dict[f'X_{variable_cnt}'] = (PNR,key)
                X_PNR_Constraint[PNR].append(X[(PNR,key)])
                X_Flight_Capacity_Constraint[key].append(X[((PNR,key))])
                variable_cnt+=1

        # for flight_index,flight in enumerate(FT): # Flight is a object
        #         for cabin in cabins_tuple: # cabin is a tuple Eg:  ('FC','PC') and cabins_tuple = list of cabins
        #                 X_Flight_Capacity_Constraint[flight][cabin[flight_index]].append(X[(PNR, FT, cabin)] * PNR.PAX)

        for PNR in PNR_list :
            if(len(X_PNR_Constraint[PNR])==0):
                continue
            CQM.add_constraint(sum(X_PNR_Constraint[PNR]) == PNR.PAX)
        
        for key,value in flight_object.pc_class_dict.items():
            CQM.add_constraint(sum(X_Flight_Capacity_Constraint[key]) <= value)
    else:
        for PNR in PNR_list:
            for key,value in flight_object.ec_class_dict.items():
                X[(PNR,key)]=dimod.Integer(f'X_{variable_cnt}')
                my_dict[f'X_{variable_cnt}'] = (PNR,key)
                X_PNR_Constraint[PNR].append(X[(PNR,key)])
                X_Flight_Capacity_Constraint[key].append(X[((PNR,key))])
                variable_cnt+=1

        # for flight_index,flight in enumerate(FT): # Flight is a object
        #         for cabin in cabins_tuple: # cabin is a tuple Eg:  ('FC','PC') and cabins_tuple = list of cabins
        #                 X_Flight_Capacity_Constraint[flight][cabin[flight_index]].append(X[(PNR, FT, cabin)] * PNR.PAX)

        for PNR in PNR_list :
            if(len(X_PNR_Constraint[PNR])==0):
                continue
            CQM.add_constraint(sum(X_PNR_Constraint[PNR]) == PNR.PAX)
        
        for key,value in flight_object.ec_class_dict.items():
            CQM.add_constraint(sum(X_Flight_Capacity_Constraint[key]) <= value)
    
    for key,value in X.items():
        Cost=cabin_to_class_cost(key[0],key[1])
        CQM_obj+=(value*Cost)
        
    
    start=time.time()
    CQM.set_objective(-1*CQM_obj)
    sampleset = sampler.sample_cqm(CQM).aggregate()
    end_time_sampling = time.time()
    start_agg = time.time()
    feasible_sampleset = sampleset.filter(lambda row: row.is_feasible) 
    end_agg = time.time()
    print("TYPE OF SAMPLESET IS " , type(sampleset) ) 
    print("Total Filter time " , end_agg - start_agg)
    print("{} feasible solutions of {}.".format(len(feasible_sampleset), len(sampleset)))    
    best = feasible_sampleset.first.sample    
    print("Total No. of Quantum Solutions are " , len(feasible_sampleset))
    solution_count= 0 
    Final_Quantum_Solutions =[]
    QSol_count=1
    for idx,sample in enumerate(feasible_sampleset.truncate(QSol_count)):
        # print("NEXT SOLUTION\n") 
        if(idx >=QSol_count):
            break
        Final_Quantum_Solutions.append(sample)  

    start_cost_cal = time.time()
    print("Total sampling time " , start_cost_cal - start)
    Sol=Final_Quantum_Solutions[0]
    num_acc={}
    for pnr in PNR_list:
            num_acc[pnr.pnr_number]=0
    for key,value in Sol.items():
        while(value):
            final_tuple=(my_dict[key][0],flight_object,Cabin,my_dict[key][1],int(num_acc[my_dict[key][0].pnr_number])+1)
            assignments[my_dict[key][0].pnr_number].append([final_tuple,order])
            num_acc[my_dict[key][0].pnr_number]+=1
            value-=1
    
    
    
    








    


def Cabin_to_Class_1(Assignment_list):
    """
    Input: Assignment_list is the list of (PNR,Flight_tuple,Cabin_tuple)
    Returns: A dictionery , in which keys are PNR numbers and the values are list of  (PNR_Object,Flight_object,Cabin,Class, Passenger number)
    and the list contains all possible flights of the PNR in order.
    """
    flow_map=defaultdict(list)
    for assignment in Assignment_list:
       i=0
       while(i<len(assignment[1])):
           flow_map[(assignment[1][i],assignment[2][i],i)].append(assignment[0])
           i+=1
    # thread_map={}
    # thread_cnt=0
    # #pp.pprint(m)
    # for flight_cabin_tuple,PNR_object in flow_map.items():
    #        thread_map[thread_cnt]=threading.Thread(target=Flow,args=(PNR_object,flight_cabin_tuple)) 
    #        thread_map[thread_cnt].start()
    #        thread_cnt+=1
    # for thread in range(thread_cnt):
    #     thread_map[thread].join()
    sampler = LeapHybridCQMSampler(token=dwave_token)
    for flight_cabin_tuple,PNR_Object in flow_map.items():
        Flow(PNR_Object,flight_cabin_tuple,sampler)
    
    final_assignments=[]
    for key1, value_list in assignments.items():
        assignments[key1] = sorted(value_list, key=lambda x: x[1])
        # temp=[]
        # for flights in assignments[key1]:
        #     temp.append(flights[0])
        # assignments[key1]=temp

    # for key,value in assignments.items():
    #     temp=[]
    #     for flights in value:
    #         temp.append(flights[0])
    #     final_assignments.append(temp)
    #     # pp.pprint(value)
    for key1, value_list in assignments.items():
        temp=[]
        for flights in value_list:
            temp.append(flights[0])
        assignments[key1]=temp

        
    #pp.pprint(assignments)
    return assignments


    
           
    
    

