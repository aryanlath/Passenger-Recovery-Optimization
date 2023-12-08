import numpy as np
from collections import defaultdict
import threading
from cost_function import *
from ortools.graph.python import min_cost_flow

import pprint
pp = pprint.PrettyPrinter(indent=4)

assignments=defaultdict(list)
lock=threading.Lock() 
total_cost=0

def Flow(PNR_list,flight_cabin_tuple):
    """
    Assigns passengers from a Passenger Name Record (PNR) list to available flight classes based on their preferences.
    It constructs a minimum-cost flow graph using the SimpleMinCostFlow class and assigns passengers accordingly.
    Input:
    - PNR_list (list): A list of Passenger Name Record objects.
    - flight_cabin_tuple (tuple): A tuple containing flight object, cabin type.
    Returns: None
    """
    global total_cost
    Flow = min_cost_flow.SimpleMinCostFlow()
    flight_object = flight_cabin_tuple[0]
    Cabin=flight_cabin_tuple[1]
    order=flight_cabin_tuple[2]
    PNR_to_OR_map={}
    OR_to_PNR_map={}
    c1=0
    for PNR in PNR_list:
        PNR_to_OR_map[PNR.pnr_number]=int(c1)
        OR_to_PNR_map[int(c1)]=PNR
        c1+=1
    total_avl=0
    Class_map={}
    Class_map_inv={}
    total_supply=0
    if(Cabin=="FC"):
        for key,value in flight_object.fc_class_dict.items():
                Class_map[key]=int(c1)
                Class_map_inv[c1]=key
                c1+=1
        for PNR in PNR_list:
            for key,value in flight_object.fc_class_dict.items():
                Flow.add_arc_with_capacity_and_unit_cost(int(PNR_to_OR_map[PNR.pnr_number]),int(Class_map[key]),int(1000),int(cabin_to_class_cost(PNR,key)))
    
        for PNR in PNR_list:
            Flow.set_node_supply(PNR_to_OR_map[PNR.pnr_number], PNR.PAX)
            total_supply+=PNR.PAX
        for key,value in flight_object.fc_class_dict.items():
            Flow.add_arc_with_capacity_and_unit_cost(Class_map[key],c1,value,0)
            total_avl+=value
        # Solve the problem and print the solution
    elif(Cabin=="BC"):
        for key,value in flight_object.bc_class_dict.items():
                Class_map[key]=int(c1)
                Class_map_inv[c1]=key
                c1+=1
        for PNR in PNR_list:
            for key,value in flight_object.bc_class_dict.items():
                Flow.add_arc_with_capacity_and_unit_cost(PNR_to_OR_map[PNR.pnr_number],Class_map[key],1000,cabin_to_class_cost(PNR,key))
    
        for PNR in PNR_list:
            Flow.set_node_supply(PNR_to_OR_map[PNR.pnr_number], PNR.PAX)
            total_supply+=PNR.PAX
        for key,value in flight_object.bc_class_dict.items():
            Flow.add_arc_with_capacity_and_unit_cost(Class_map[key],c1,value,0)
            total_avl+=value
        # Solve the problem and print the solution
    elif(Cabin=="PC"):
        for key,value in flight_object.pc_class_dict.items():
                Class_map[key]=int(c1)
                Class_map_inv[c1]=key
                c1+=1
        for PNR in PNR_list:
            for key,value in flight_object.pc_class_dict.items():
                Flow.add_arc_with_capacity_and_unit_cost(PNR_to_OR_map[PNR.pnr_number],Class_map[key],1000,cabin_to_class_cost(PNR,key))
    
        for PNR in PNR_list:
            Flow.set_node_supply(PNR_to_OR_map[PNR.pnr_number], PNR.PAX)
            total_supply+=PNR.PAX
        for key,value in flight_object.pc_class_dict.items():
            Flow.add_arc_with_capacity_and_unit_cost(Class_map[key],c1,value,0)
            total_avl+=value

        # Solve the problem and print the solution
    else:
        for key,value in flight_object.ec_class_dict.items():
                Class_map[key]=int(c1)
                Class_map_inv[c1]=key
                c1+=1
        for PNR in PNR_list:
            for key,value in flight_object.ec_class_dict.items():
                Flow.add_arc_with_capacity_and_unit_cost(PNR_to_OR_map[PNR.pnr_number],Class_map[key],1000,cabin_to_class_cost(PNR,key))
    
        for PNR in PNR_list:
            Flow.set_node_supply(PNR_to_OR_map[PNR.pnr_number], PNR.PAX)
            total_supply+=PNR.PAX
        for key,value in flight_object.ec_class_dict.items():
            Flow.add_arc_with_capacity_and_unit_cost(Class_map[key],c1,value,0)
            total_avl+=value
       
    Flow.set_node_supply(c1,-total_supply)
    status = Flow.solve()
    if status == Flow.OPTIMAL:
        # Handle optimal solution
        num_acc={} ## Number of passengers accomodated in each PNR
        for pnr in PNR_list:
            num_acc[pnr.pnr_number]=0
        for i in range(Flow.num_arcs()):
            cost = Flow.flow(i) * Flow.unit_cost(i)
            with lock:
                total_cost+=cost
            if(Flow.tail(i)>=len(PNR_list)):continue
            if(Flow.flow(i)==0):continue
            pnr_object=OR_to_PNR_map[Flow.tail(i)]
            Class=Class_map_inv[Flow.head(i)]
            flow_val=copy.deepcopy(Flow.flow(i))
            while(flow_val>0):
                final_tuple=(pnr_object,flight_object,Cabin,Class,num_acc[pnr_object.pnr_number]+1)
                num_acc[pnr_object.pnr_number]+=1
                flow_val-=1
                with lock:
                    assignments[pnr_object.pnr_number].append([final_tuple,order])
            
    elif status == Flow.INFEASIBLE:
    
      print("The problem is infeasible.")
    elif status == Flow.UNBALANCED:
        print("The problem is unbalanced.")
    else:
        print("There was an issue with the flow graph input.")



    


def Cabin_to_Class(Assignment_list):
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
    thread_map={}
    thread_cnt=0
    #pp.pprint(m)
    for flight_cabin_tuple,PNR_object in flow_map.items():
           thread_map[thread_cnt]=threading.Thread(target=Flow,args=(PNR_object,flight_cabin_tuple)) 
           thread_map[thread_cnt].start()
           thread_cnt+=1
    for thread in range(thread_cnt):
        thread_map[thread].join()
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


    
           
    
    

