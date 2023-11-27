from utils import *
from Models.Flights import Flight
import feasible_flights 
def Arrival_Delay(pnr,flight):
    res=feasible_flights.init_PNR_to_Flight_Object()
    actual_time=res[pnr.pnr_number].arrival_time
    new_time=(flight.arrival_time)
    delay=(new_time-actual_time).seconds
    if(delay<=6):
        return 72
    elif(delay>6 and delay<=12):
        return 50
    elif(delay>12 and delay<=24):
        return 40
    elif(delay<=48):
        return 30
    else:
        return -100
    
def Departure_Delay(pnr,flight):
    res=feasible_flights.init_PNR_to_Flight_Object()
    actual_time=res[pnr.pnr_number].departure_time
    new_time=flight.departure_time
    delay=(new_time-actual_time).seconds
    if(delay<=6):
        return 72
    elif(delay>6 and delay<=12):
        return 50
    elif(delay>12 and delay<=24):
        return 40
    elif(delay<=48):
        return 30
    else:
        return -100
    

def Calculate_PNR_Score(pnr):
    ans=0
    if(pnr.special_requirements==1):
        ans+=200
    cabin_score={}
    cabin_score["A"]=1000
    cabin_score["F"]=750
    ans+=cabin_score[pnr.flight_cabin]
    if(pnr.passenger_loyality=='1'):
        ans+=2000
    return ans
    
def calculate_cabin_score(pnr,Cabin):
    intial_cabin=pnr.flight_cabin
    final_cabin=Cabin
    cabin_score={}
    cabin_score["A"]=5
    cabin_score["F"]=3
    #cabin_score["Y"]=1
    return cabin_score[Cabin]-cabin_score[intial_cabin]



def helper_cost_function(ArrivalDelay,DepartureDelay,pnr_score,class_score):
    return (ArrivalDelay+DepartureDelay)*pnr_score*class_score ## Log2(product)


def cost_function(PNR,flight,Class):
    ArrivalDelay=Arrival_Delay(PNR,flight)
    DepartureDelay=Departure_Delay(PNR,flight)
    pnr_score=Calculate_PNR_Score(PNR)
    class_score=calculate_cabin_score(PNR,Class)
    
    return helper_cost_function(ArrivalDelay,DepartureDelay,pnr_score,class_score)




