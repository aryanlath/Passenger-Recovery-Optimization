from utils import *
from Models.PNR import *
from Models.Flights import *
from constants import *
from utils import *
import networkx as nx
import matplotlib.pyplot as plt
import copy
import pprint
import multiprocessing
from feasible_flights import *

pp = pprint.PrettyPrinter(indent=4)
lock=multiprocessing.Lock()

def PNR_to_Feasible_Flights_2(graph,all_flights,PNR_Object,PNR_to_feasible_flights_map_2,num_of_hops=4,new_arrival_city=None):
    """
    Find flights from departure_city to arrival_city with exactly number_of_hops.
    Input : graph , current network graph
            all_flights, a dict consisting of flight number to flight object mapping
            PNR_Object 
            max num of hops
    Returns: All possible paths consisting of at max num_of hops [(F1,F2,),] : F1,F2 are the flight objects
    """
    earliest_reached_city=None
    current_hops=0
    previous_city=all_flights[PNR_Object.inv_list[0]].departure_city
    arrival_time=None
    for flight in PNR_Object.inv_list:
        if(all_flights[flight].status=="cancelled"):
            earliest_reached_city=previous_city
            departure_time=all_flights[flight].departure_time
            break

        else:
            previous_city=all_flights[flight].arrival_city
            arrival_time=all_flights[flight].arrival_time
            current_hops+=1
    
    if(earliest_reached_city==None): 
        return None

    departure_city = earliest_reached_city

    arrival_city   =  all_flights[PNR_Object.inv_list[-1]].arrival_city

    all_paths=[]

    
    curr_location=copy.deepcopy(current_hops)+1
    while(curr_location<len(PNR_Object.inv_list)):
        cabin = PNR_Object.get_cabin(PNR_Object.sub_class_list[curr_location])
        sub_class = PNR_Object.sub_class_list[curr_location]

        if cabin=='FC':
            all_flights[PNR_Object.inv_list[curr_location]].fc_available_inventory+=int(PNR_Object.PAX)
            all_flights[PNR_Object.inv_list[curr_location]].fc_class_dict[sub_class]+=int(PNR_Object.PAX)
        elif cabin=='BC':
            all_flights[PNR_Object.inv_list[curr_location]].bc_available_inventory+=int(PNR_Object.PAX)
            all_flights[PNR_Object.inv_list[curr_location]].bc_class_dict[sub_class]+=int(PNR_Object.PAX)
        elif cabin=='PC':
            all_flights[PNR_Object.inv_list[curr_location]].pc_available_inventory+=int(PNR_Object.PAX)
            all_flights[PNR_Object.inv_list[curr_location]].pc_class_dict[sub_class]+=int(PNR_Object.PAX)
        else:
            all_flights[PNR_Object.inv_list[curr_location]].ec_available_inventory+=int(PNR_Object.PAX)
            all_flights[PNR_Object.inv_list[curr_location]].ec_class_dict[sub_class]+=int(PNR_Object.PAX)

        curr_location+=1
    
    if(new_arrival_city!=None):
        arrival_city=new_arrival_city
    
    all_paths=custom_dfs_iterative(graph,departure_city,arrival_city,num_of_hops-current_hops)
    actual_valid_paths=copy.deepcopy(all_paths)

    for path in all_paths:
        isFirst=True
        valid= True

        for flight in path:
            if isFirst:
                if(arrival_time==None):
                    if(abs(flight.departure_time.timestamp()-departure_time.timestamp())>=ETD*60*60):
                        valid=False
                        break
                elif((flight.departure_time.timestamp()-arrival_time.timestamp())<=MCT*60*60 or (flight.departure_time.timestamp()-departure_time.timestamp())>=ETD*60*60):
                    valid=False
                    break
                isFirst = False
                previous_arrival_time=flight.arrival_time
            else:

                if((flight.departure_time.timestamp()-previous_arrival_time.timestamp())<=MCT*60*60 or (flight.departure_time.timestamp()-previous_arrival_time.timestamp())>=MAXCT*60*60):
                    valid=False
                    break
                else:
                    previous_arrival_time=flight.arrival_time

        if not valid:
            actual_valid_paths.remove(path) 
    with lock:
        if(PNR_Object.pnr_number not in PNR_to_feasible_flights_map_2):
                PNR_to_feasible_flights_map_2[PNR_Object.pnr_number]=actual_valid_paths
        else:
                PNR_to_feasible_flights_map_2[PNR_Object.pnr_number].extend(actual_valid_paths)


# G=create_flight_graph()
# visualize_flight_graph(G)
# all_flights,all_pnrs,_,_=Get_All_Maps()
# ans=PNR_to_Feasible_Flights(G,all_flights,all_pnrs["PNR001#1"])
# pp.pprint(ans)

