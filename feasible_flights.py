from utils import *
from Models.PNR import *
from Models.Flights import *
from constants import *
from utils import *
import networkx as nx
import matplotlib.pyplot as plt
import copy
import pprint
import time

pp = pprint.PrettyPrinter(indent=4)


def Get_All_Maps():
    """
    Returns all_flights: a dictionary which maps every flight number to corrresponding flight Object
    Returns pnr_objects: a dictionary which maps every pnr number to corrresponding PNR Object
    Returns pnr_flight_mapping: a dictionery which maps every pnr to the list of associated flight 
                                objects taken by them
    """
    pnr_flight_mapping = {}
    all_flights = {}
    pnr_objects={}
    pnr_to_s2 = {}
    pnr_list,_    = extract_PNR_from_CSV(test_PNR_data_file) 
    all_flight  = extract_Flights_from_CSV(test_flight_data_file) # test data passed
    for flight in all_flight:
        all_flights[flight.inventory_id] = flight
    for pnr in pnr_list:
        pnr_objects[pnr.pnr_number] = pnr
        pnr_to_s2[pnr.pnr_number] = pnr.get_pnr_score() #  Uncomment this
    for pnr in pnr_list:
        flight_objects=[]
        for flight in pnr.inv_list:
            flight_objects.append(all_flights[flight])
        pnr_flight_mapping[pnr.pnr_number]=flight_objects
            
    return all_flights,pnr_objects,pnr_flight_mapping,pnr_to_s2

def Get_Impacted_passengers(all_flights,pnr_objects):
    """
    Function which returns the list of impacted PNR objects:
    Input Parameters: map of :- flight numbers and flight objects(all_flights), pnr numbers and pnr objects(pnr_objects)
    Returns :- List of Impacted Parameters

    """
    
    Impacted_flights=[]
    Impacted_PNR=[]
    for key,value in all_flights.items():
        if value.status=="cancelled":
            Impacted_flights.append(key)
    for key,value in pnr_objects.items():
        for flight_number in value.inv_list:
            if flight_number in Impacted_flights:
                if(value in Impacted_PNR ):
                    pass
                else:
                    Impacted_PNR.append(value)
    return Impacted_PNR


def visualize_flight_graph(graph):
    """
    Function used to visualize the graph. Input:- Networkx graph

    """

    plt.figure(figsize=(12, 8))  # Set the size of the plot
    pos = nx.spring_layout(graph)  # Positions for all nodes

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color='lightblue')

    # Draw edges
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), edge_color='gray')

    # Draw node labels
    nx.draw_networkx_labels(graph, pos, font_size=12, font_family='sans-serif')

    # Draw edge labels (optional, uncomment if needed)
    # edge_labels = nx.get_edge_attributes(graph, 'flight')
    # nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.title("Flight Network Graph")
    plt.axis('off')  # Turn off the axis
    plt.show()

def create_flight_graph():
    """
    Function for creating the networkx graph

    """
    all_flights = extract_Flights_from_CSV(test_flight_data_file)
    G = nx.MultiDiGraph()
    i = 0
    for flight in all_flights:
        # Add edge with flight object as an attribute
        if(flight.status=="cancelled"):
            continue
        G.add_edge(flight.departure_city, flight.arrival_city, flight=flight)
        i = i+1
    return G


def test():
    """
    Function for testing
    """

    G = nx.MultiDiGraph()
    i = 0
    all_flights = extract_Flights_from_CSV(test_flight_data_file)
    for flight in all_flights:
        if(flight.status=="cancelled"):
            continue
        G.add_edge(flight.departure_city, flight.arrival_city, flight=flight)
        i = i+1
    return G



def remove_cancelled_flights(graph, cancelled_flights):

    """
    Function which removes the cancelled flights from the graph. 
    Input:- Networkx graph, list of flight_numbers of cancelled flights
    """
    edges_to_remove = [(u, v) for u, v, attrs in graph.edges(data=True) if attrs['flight'].flight_number in cancelled_flights]
    for edge in edges_to_remove:
        graph.remove_edge(*edge)

def custom_dfs(graph, source, destination, path, visited_edges, all_paths,k):
    """
    DFS :- for finding all possible paths
    Input:- Networkx graph, source, destination , list for path storing(paths), list of visited edges,
            list of all possible paths , max_number of hops (k)
    """
    if len(path) > k:  # Check if the current path length exceeds k
         return
    if source == destination and len(path)>0:
        path=tuple(path)
        all_paths.append(path)
        return
    for neighbor in list(graph.neighbors(source)):
        for key in graph[source][neighbor]:
            edge = (graph[source][neighbor][key]["flight"])
            if edge not in visited_edges:
                visited_edges.append(edge)
                path.append(edge)
                custom_dfs(graph, neighbor, destination, path, visited_edges, all_paths,k)
                visited_edges.remove(edge)
                path.pop()


def custom_dfs_iterative(graph, source, destination, k,dp):
    """
    Iterative DFS for finding all possible paths composed of distinct edges
    Input: Networkx graph, source, destination, max_number of hops (k)
    Output: List of all possible paths composed of distinct edges
    """
    stack = [(source, [], set())]
    all_paths = []
    if((source,destination,k) in dp):
        return dp[(source,destination,k)] #memoisation to reduce time

    while stack:
        current_node, path_edges, visited_nodes = stack.pop()

        if len(path_edges) > k:  # Checking the number of edges in the path
            continue

        if current_node == destination and len(path_edges) > 0:
            all_paths.append(tuple(path_edges.copy()))
            continue

        neighbors = list(graph.neighbors(current_node))
        for neighbor in neighbors:
            for key in graph[current_node][neighbor]:
                edge = (graph[current_node][neighbor][key]["flight"])
                if neighbor not in visited_nodes:
                    new_path_edges = path_edges + [edge]
                    new_visited_nodes = visited_nodes.copy()
                    new_visited_nodes.add(neighbor)
                    stack.append((neighbor, new_path_edges, new_visited_nodes))
    dp[(source,destination,k)]=all_paths
    return dp[(source,destination,k)]


def PNR_to_Feasible_Flights(graph,all_flights,PNR_Object,PNR_to_FeasibleFlights_map,dp,num_of_hops=4,new_arrival_city=None):
    """
    Find flights from departure_city to arrival_city with exactly number_of_hops.
    Input : graph , current network graph
            all_flights, a dict consisting of flight number to flight object mapping
            PNR_Object 
            max num of hops
            new_arrival_city: to handle city pairs
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
    all_paths=custom_dfs_iterative(graph,departure_city,arrival_city,num_of_hops-current_hops,dp)
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

    if new_arrival_city is None:
        PNR_to_FeasibleFlights_map[PNR_Object.pnr_number] =actual_valid_paths

    else:
        if(PNR_Object.pnr_number not in PNR_to_FeasibleFlights_map):
                PNR_to_FeasibleFlights_map[PNR_Object.pnr_number]=actual_valid_paths
        else:
                PNR_to_FeasibleFlights_map[PNR_Object.pnr_number].extend(actual_valid_paths)

