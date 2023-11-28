from utils import *
from Models.PNR import *
from Models.Flights import *
from constants import *
import networkx as nx
import matplotlib.pyplot as plt
from itertools import product

def init_PNR_to_Flight_Object():
    res = {}
    all_flights = {}
    pnr_list    = extract_PNR_from_CSV(pnr_data_file)
    all_flight  = extract_Flights_from_CSV(flight_data_file)
    for flight in all_flight:
        all_flights[flight.flight_number] = flight
    for pnr in pnr_list:
        res[pnr.pnr_number] = all_flights.get(str(pnr.flight_number))
    return res

def PNR_to_Feasible_Flights(PNR_Object):
    all_flights = extract_Flights_from_CSV(flight_data_file)
    PNR_to_Flight_Object = init_PNR_to_Flight_Object()
    feasible_flight_list = []
    my_flight            = PNR_to_Flight_Object[PNR_Object.pnr_number]
    my_arrival_time      = my_flight.arrival_time
    my_departure_time  = my_flight.departure_time
    for flight in all_flights:
        flight_arrival_time = flight.arrival_time
        flight_departure_time = flight.departure_time
        if((flight_departure_time - my_arrival_time).total_seconds() >= 0 and (flight_departure_time - my_arrival_time).total_seconds() <= ETD*60*60 and flight.status):
            feasible_flight_list.append(flight)

    return feasible_flight_list

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
    all_flights = extract_Flights_from_CSV(flight_data_file)
    G = nx.MultiDiGraph()
    i = 0
    for flight in all_flights:
        # Add edge with flight object as an attribute
        if(flight.status=='Cancelled'):
            continue
        G.add_edge(flight.departure_city, flight.arrival_city, flight=flight)
        i = i+1
    return G

def remove_cancelled_flights(graph, cancelled_flights):
    edges_to_remove = [(u, v) for u, v, attrs in graph.edges(data=True) if attrs['flight'].flight_number in cancelled_flights]
    for edge in edges_to_remove:
        graph.remove_edge(*edge)

def find_flights_with_hops(graph, PNR_Object, number_of_hops):
    """
    Find flights from departure_city to arrival_city with exactly number_of_hops.

    :param graph: NetworkX MultiDiGraph representing the flight network.
    :param PNR_Object: The PNR_Object.
    :param number_of_hops: The exact number of hops (flights) required.
    :return: A list of lists, where each inner list represents a sequence of flights.
    """
    PNR_to_Flight_Object = init_PNR_to_Flight_Object()
    # print(PNR_Object)
    # print(PNR_to_Flight_Object)
    departure_city = PNR_to_Flight_Object[PNR_Object.pnr_number].departure_city
    arrival_city = PNR_to_Flight_Object[PNR_Object.pnr_number].arrival_city
    departure_time = PNR_to_Flight_Object[PNR_Object.pnr_number].departure_time
    valid_paths = []
    for path in nx.all_simple_paths(graph, source=departure_city, target=arrival_city, cutoff=number_of_hops):
        #print(path)
        if len(path)-1 <= number_of_hops:  # Check if the path length matches the number of hops
            #print(len(path)-1)
            flights_in_path = []
            for i in range(len(path)-1):
                flights_between_cities = graph.get_edge_data(path[i], path[i+1])
                if flights_between_cities:
                    flights_in_path.append([flights_between_cities[key]['flight'] for key in flights_between_cities])
            if flights_in_path:
                if(len(path)-1 == 1):
                    p = flights_in_path[0]
                    for item in p:
                        f1 = item
                        if(f1.status == 0):
                            continue
                        if(abs(f1.departure_time - departure_time).total_seconds() > ETD*60*60):
                                continue
                        valid_paths.append((item,))
                else:
                    p = list(product(flights_in_path[0],flights_in_path[1]))
                    i = 0
                    for item in p:
                        f1 = item[0]
                        f2 = item[1]
                        if(f1.status == 0 or f2.status == 0):
                            continue
                        if(i == 0):
                            if(abs(f1.departure_time - departure_time).total_seconds() > ETD*60*60):
                                continue
                        if((f2.departure_time - f1.arrival_time).total_seconds() >= MCT*60*60 and (f2.departure_time - f1.arrival_time).total_seconds() <= MAXCT*60*60):
                            valid_paths.append(tuple(item))
                        i = i+1
    return valid_paths

# G = create_flight_graph()
# # visualize_flight_graph(G)
# # # remove_cancelled_flights(G, ['1041'])
# pnr_list    = extract_PNR_from_CSV(pnr_data_file)
# for item in pnr_list:
#     if(item.flight_number == 1004):
#        print(find_flights_with_hops(G, item, 2))