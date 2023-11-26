from utils import *
from Models.Flights import Flight

# Get the flights and passenger ranking
passengers = PNR_ranking()
flights = []
n=10

class Assignment:
    def __init__(self,PNR,Flight,cost):
        self.pnr = PNR
        self.flight = Flight
        self.cost = cost

# for i in range(n):
#     flights.append(Flight(i+1,2,3,"A","B",i+100,True))

cost = 0

def assign_passengers_to_flights(passengers, flights):
    """
    Assuming flights are ranked and passengers are ranked in decreasing order
    """

    assignments = []
    not_assigned = []

    for passenger in passengers:
        assigned = False
        pax_flight_map = Flight_score(passenger,flights)
        sorted_objects = sorted(pax_flight_map, key=lambda x: x.score, reverse=True)

        for flight in sorted_objects:
            if flight.remaining_capacity>=passenger.PAX:
                assignment = Assignment(passenger,flight.flight,flight.score)
                assignments.append(assignment)
                cost+=assignment.cost
                flight.remaining_capacity -= passenger.PAX
                assigned = True
                if(flight.remaining_capacity==0):
                    flights.pop(flights.index(flight))
                break

        if(not assigned):
            not_assigned.append(passenger)

    return assignments,not_assigned

assignments,not_assigned = assign_passengers_to_flights(passengers, flights)

# Display assignments
print("Passenger Assignments:")
for assignment in assignments:
    print(f"{assignment[0].pnr.pnr_number} -> {assignment[1].flight.flight_number}")
    print(f"Cost is: {cost}")

if(len(not_assigned)==0):
    print("All passengers are assigned.")

else:
    print("Not assigned ones are as follows")
    for assignment in not_assigned:
        print(assignment.pnr_number)
    