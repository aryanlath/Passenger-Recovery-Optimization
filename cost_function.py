from utils import *
from Models.Flights import Flight
import feasible_flights 
from constants import *
import math
from flightScores import *

def cost_function(PNR,flight_tuple, cabin_tuple):
    """
    Calculates the cost function for each PNR to flight mapping.
    Calculation done as follows: cost = a*log(s1) + b*log(s2) + c*log(s3)
    where, s1 = flight quality score
           s2 = PNR score
           s3 = class difference score
    """
    s1 = flight_quality_score(PNR, flight_tuple)
    s2 = PNR_Score(PNR)/pnr_normalize_factor
    s3 = class_difference_score(PNR, flight_tuple, cabin_tuple)
    cost = weight_flight_map*math.log(s1) + weight_pnr_map*math.log(s2) + weight_cabin_map*math.log(s3)
    return cost

def PNR_Score(PNR):
    """
    Calculates the PNR score for each PNR.
    Calculation done as follows: score = a*s1 + b*s2 + c*s3
    where, s1 = PNR_SSR
           s2 = PNR_loyalty
           s3 = PNR_pax
    """
    return PNR.get_pnr_score()

def flight_quality_score(PNR, flight_tuple):
    """
    Calculates the flight quality score for each PNR to flight mapping.
    """
    # Dictionary that maps each PNR.pnr_numer to list of all flights taken by that PNR
    # TODO: kNN
    first_flight = pnr_flight_mapping[PNR.pnr_number][0]
    last_flight = pnr_flight_mapping[PNR.pnr_number][-1]
    Arrival_Delay_inHours = (last_flight.arrival_time - flight_tuple[-1].arrival_time).total_seconds()/3600
    Departure_Delay_inHours = (first_flight.arrival_time - flight_tuple[0].arrival_time).total_seconds()/3600
    DelayScore = 0 
    
    if(Arrival_Delay_inHours <= 6):
        DelayScore += arrDelay6h
    elif(Arrival_Delay_inHours <= 12):
        DelayScore += arrDelay12h
    elif(Arrival_Delay_inHours <= 24):
        DelayScore += arrDelay24h
    elif(Arrival_Delay_inHours <= 48):
        DelayScore += arrDelay48h
    else:
        DelayScore += 0.00000001

    if(Departure_Delay_inHours <= 6):
        DelayScore += STD6h
    elif(Departure_Delay_inHours <= 12):
        DelayScore += STD12h
    elif(Departure_Delay_inHours <= 24):
        DelayScore += STD24h
    elif(Departure_Delay_inHours <= 48):
        DelayScore += STD48h
    else:
        DelayScore += 0.00000001
    
    ConnectionScore = connection_constant - len(flight_tuple) + len(pnr_flight_mapping[PNR.pnr_number])
    
    return DelayScore + ConnectionScore*10

def class_difference_score(PNR, cabin_Tuple):
    """
    Calculates the class difference score for each PNR to flight mapping.
    """
    Cabin_Cost = {
        "EC": 1,
        "PC": 1.5,
        "BC": 3,
        "FC": 6
    }
    upgrade_multiplier = 1.1
    downgrade_multiplier = 1.5
    sug_sum = 0
    pre_sum = 0
    for i in range(len(cabin_Tuple)):
        sug_sum += Cabin_Cost[cabin_Tuple[i]]
    for i in range(len(PNR.sub_class_list)):
        pre_sum += Cabin_Cost[PNR.sub_class_list[i]]
    sug_sum /= len(cabin_Tuple)
    pre_sum /= len(PNR.sub_class_list)
    ratio = sug_sum/pre_sum
    if(ratio > 1):
        return upgrade_multiplier*ratio
    else:
        return downgrade_multiplier*ratio