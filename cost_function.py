from utils import *
from Models.Flights import Flight
import feasible_flights 
from constants import *
def Arrival_Delay(pnr,flight_tuple):
    res=feasible_flights.init_PNR_to_Flight_Object()
    actual_time=res[pnr.pnr_number].arrival_time
    new_time=flight_tuple[-1].arrival_time
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
        return -1
    
def Departure_Delay(pnr,flight_tuple):
    res=feasible_flights.init_PNR_to_Flight_Object()
    actual_time=res[pnr.pnr_number].departure_time
    new_time=flight_tuple[0].departure_time
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
        return -1
    

def Calculate_PNR_Score(pnr):
    ans=0
    if(pnr.special_requirements==1):
        ans+=200
    cabin_score={}
    cabin_score["A"]=1000
    cabin_score["F"]=750
    ans+=cabin_score[pnr.flight_cabin]
    if(pnr.passenger_loyalty=='1'):
        ans+=2000
    return ans
    
def calculate_cabin_score(pnr,Cabin_list):
    intial_cabin=pnr.flight_cabin
    final_Cabin_avg=0
    Cabin_score={}
    Cabin_score["A"]=5
    Cabin_score["F"]=3
    for Cabin in Cabin_list:
        final_Cabin_avg+=Cabin_score[Cabin]
    final_Cabin_avg/=len(Cabin_list)
    #cabin_score["Y"]=1
    return final_Cabin_avg-Cabin_score[intial_cabin]



def helper_cost_function(ArrivalDelay,DepartureDelay,pnr_score,class_score):
    return (ArrivalDelay+DepartureDelay)*pnr_score*(class_score + 3)## Log2(product)


def cost_function(PNR,flight,Cabin):
    pnr_score=Calculate_PNR_Score(PNR)
    if(flight==None):
        return -M*pnr_score
    ArrivalDelay=Arrival_Delay(PNR,flight)
    DepartureDelay=Departure_Delay(PNR,flight)
    class_score=calculate_cabin_score(PNR,Cabin)
    return helper_cost_function(ArrivalDelay,DepartureDelay,pnr_score,class_score)




