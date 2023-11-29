from utils import *
from Models.PNR import *
from Models.Flights import *
from constants import *
import networkx as nx
import matplotlib.pyplot as plt
import copy
import pprint 
pp = pprint.PrettyPrinter(indent=4)

def init_FlightNumber_to_Flight_Object():
    """
    Returns all_flights: a dictionary which maps every flight number to corrresponding flight Object
    Returns pnr_objects: a dictionary which maps every pnr number to corrresponding PNR Object
    Returns pnr_flight_mapping: a dictionery which maps every pnr to the list of associated flight 
                                objects taken by them
    """
    pnr_flight_mapping = {}
    all_flights = {}
    pnr_objects={}
    pnr_list    = extract_PNR_from_CSV(test_PNR_data_file) 
    all_flight  = extract_Flights_from_CSV(test_flight_data_file) # test data passed
    for flight in all_flight:
        all_flights[flight.flight_number] = flight
    for pnr in pnr_list:
        pnr_objects[pnr.pnr_number] = pnr
    for pnr in pnr_list:
        flight_objects=[]
        for flight in pnr.inv_list:
            flight_objects.append(all_flights[flight])
        pnr_flight_mapping[pnr.pnr_number]=flight_objects
            
    return all_flights,pnr_objects,pnr_flight_mapping
    

# def init_Flight_to_PNR_map():
#     """Returns Flight to PNR object map"""
#     Flight_to_PNR_map = defaultdict(list)
#     pnr_list    = extract_PNR_from_CSV(pnr_data_file)
#     for pnr in pnr_list:
#         Flight_to_PNR_map[pnr.flight_number].append(pnr)
#     return Flight_to_PNR_map

def Get_Impacted_passengers(all_flights,pnr_objects):
    Impacted_flights=[]
    Impacted_PNR=[]
    for key,value in all_flights.items():
        if not value.status:
            Impacted_flights.append(key)
    for key,value in pnr_objects.items():
        for flight_number in value.inv_list:
            if flight_number in Impacted_flights:
                if(value in Impacted_PNR ):
                    pass
                else:
                    Impacted_PNR.append(value)
    return Impacted_PNR
    
                


        


# def PNR_to_Feasible_Flights(PNR_Object):
#     all_flights = extract_Flights_from_CSV(flight_data_file)
#     PNR_to_Flight_Object = init_PNR_to_Flight_Object()
#     feasible_flight_list = []
#     my_flight            = PNR_to_Flight_Object[PNR_Object.pnr_number]
#     my_arrival_time      = my_flight.arrival_time
#     my_departure_time  = my_flight.departure_time
#     for flight in all_flights:
#         flight_arrival_time = flight.arrival_time
#         flight_departure_time = flight.departure_time
#         if((flight_departure_time - my_arrival_time).total_seconds() >= 0 and (flight_departure_time - my_arrival_time).total_seconds() <= ETD*60*60 and flight.status):
#             feasible_flight_list.append(flight)

#     return feasible_flight_list

def visualize_flight_graph(graph):
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
    all_flights = extract_Flights_from_CSV(test_flight_data_file)
    G = nx.MultiDiGraph()
    i = 0
    for flight in all_flights:
        # Add edge with flight object as an attribute
        if(flight.status==0):
            continue
        G.add_edge(flight.departure_city, flight.arrival_city, flight=flight)
        i = i+1
    return G

def test():
    G = nx.MultiDiGraph()
    i = 0
    all_flights = extract_Flights_from_CSV(test_flight_data_file)
    for flight in all_flights:
        # Add edge with flight object as an attribute
        #print(flight)
        if(flight.status==0):
            continue
        G.add_edge(flight.departure_city, flight.arrival_city, flight=flight)
        i = i+1
    return G



def remove_cancelled_flights(graph, cancelled_flights):
    edges_to_remove = [(u, v) for u, v, attrs in graph.edges(data=True) if attrs['flight'].flight_number in cancelled_flights]
    for edge in edges_to_remove:
        graph.remove_edge(*edge)

def custom_dfs(graph, source, destination, path, visited_edges, all_paths,k):
    if len(path) > k:  # Check if the current path length exceeds k
         return
   # print(source)
    if source == destination:
        #print("hi")
       # print(path)
        path=tuple(path)
        all_paths.append(path)
        return
    for neighbor in list(graph.neighbors(source)):
        #print(neighbor)
        for key in graph[source][neighbor]:
            #print(flight)
            edge = (graph[source][neighbor][key]["flight"])
            ##print(edge)
            if edge not in visited_edges:
                visited_edges.append(edge)
                path.append(edge)
                custom_dfs(graph, neighbor, destination, path, visited_edges, all_paths,k)
                visited_edges.remove(edge)
                path.pop()

def PNR_to_Feasible_Flights(graph,all_flights,PNR_Object,num_of_hops=10):
    """
    Find flights from departure_city to arrival_city with exactly number_of_hops.
    Input : graph , current network graph
            all_flights, a dict consisting of flight number to flight object mapping
            PNR_Object 
            max num of hops
    Returns: All possible paths consisting of at max num_of hops [(F1,F2,),] : F1,F2 are the flight objects
    """
    # print(PNR_Object)
    # print(PNR_to_Flight_Object)
    earlist_reached_city=None
    current_hops=0
    previous_city=all_flights[PNR_Object.inv_list[0]].departure_city
    arrival_time=None
    for flight in PNR_Object.inv_list:
        #print(flight)
        #print(all_flights[flight])
        if(all_flights[flight].status==0):
            #print(flight)
            earlist_reached_city=previous_city
            departure_time=all_flights[flight].departure_time
            break
        else:
            previous_city=all_flights[flight].arrival_city
            arrival_time=all_flights[flight].arrival_time
            current_hops+=1
    if(earlist_reached_city==None): 
        return None
    departure_city = earlist_reached_city
    arrival_city   =  all_flights[PNR_Object.inv_list[-1]].arrival_city
    #print(departure_city,arrival_city)
    valid_paths = []
    all_paths=[]
    visited_edges=[]
    custom_dfs(graph,departure_city,arrival_city,valid_paths,visited_edges,all_paths,num_of_hops-current_hops)
    actual_valid_paths=copy.deepcopy(all_paths)
    print("path:")
    pp.pprint(actual_valid_paths)
    for path in all_paths:
        i=0
        valid=1
        #print(path)
        for flight in path:
            if(i==0):
              ##  print(arrival_time,flight.departure_time,flight.arrival_time)
                if(arrival_time==None):
                    if((flight.departure_time.timestamp()-departure_time.timestamp())>=ETD*60*60):
                        valid=0
                        break
                elif((flight.departure_time.timestamp()-arrival_time.timestamp())<=MCT*60*60 or (flight.departure_time.timestamp()-departure_time.timestamp())>=ETD*60*60):
                    valid=0
                    break
                i+=1
                previous_arrival_time=flight.arrival_time
            else:
                #print((flight.departure_time.timestamp()-previous_arrival_time.timestamp()))
                if((flight.departure_time.timestamp()-previous_arrival_time.timestamp())<=MCT*60*60 or (flight.departure_time.timestamp()-previous_arrival_time.timestamp())>=MAXCT*60*60):
                    valid=0
                    #print("h")
                    break
                else:
                    previous_arrival_time=flight.arrival_time
        if(valid==0):
            actual_valid_paths.remove(path) 
            #print(path)
    return actual_valid_paths


# #visualize_flight_graph(G)
G=create_flight_graph()
all_flights,all_pnrs,_=init_FlightNumber_to_Flight_Object()
ans=PNR_to_Feasible_Flights(G,all_flights,all_pnrs["PNR0005"])
# pp.pprint(ans)
# # # remove_cancelled_flights(G, ['1041'])

# ans=PNR_to_Feasible_Flights(G,all_flights,all_pnrs["PNR0005"])
# print(ans)

# pp.pprint(init_FlightNumber_to_Flight_Object()[0])
# print()
# pp.pprint(init_FlightNumber_to_Flight_Object()[1])
# print()
# pp.pprint(init_FlightNumber_to_Flight_Object()[2])