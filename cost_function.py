from utils import *
from Models.Flights import Flight
import feasible_flights 
from constants import *
import math
from flightScores import *
import constants_immutable

## Customizable
def cabin_to_class_cost(PNR,Curr_Subclass):
    """
    Returns the class to class mapping cost inside a cabin.
    Input: PNR Object,Current Subclass
    Returns: Cost (configurable)
    """
    subclass_list=PNR.sub_class_list
    costs={}
    curr_cost=0
    for letter_code in range(ord('A'), ord('Z')+1):
        letter = chr(letter_code)
        costs[letter]=curr_cost
        curr_cost+=1
    avg_cost=0
    for subclass in subclass_list:
        avg_cost+=costs[subclass]
    avg_cost/=len(subclass_list)
    new_cost=costs[Curr_Subclass]
    return new_cost-avg_cost



def cost_function(PNR,flight_tuple, cabin_tuple):
    """
    Calculates the cost function for each PNR to flight mapping.
    Calculation done as follows: cost = a*log(s1) + b*log(s2) + c*log(s3)
    where, s1 = flight quality score
           s2 = PNR score
           s3 = class difference score
    """
    if(flight_tuple is None):
        return -NON_ASSIGNMENT_COST*PNR_Score(PNR)
    s1 = flight_quality_score(PNR, flight_tuple)
    s2 = PNR_Score(PNR)/pnr_normalize_factor
    s3 = class_difference_score(PNR,cabin_tuple)
    if(s3==0):
        return - 100*NON_ASSIGNMENT_COST*PNR_Score(PNR)
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
    # _,_,pnr_flight_mapping,_= feasible_flights.Get_All_Maps()
    first_flight = constants_immutable.pnr_flight_mapping[PNR.pnr_number][0]
    last_flight = constants_immutable.pnr_flight_mapping[PNR.pnr_number][-1]
    Arrival_Delay_inHours = abs((last_flight.arrival_time - flight_tuple[-1].arrival_time).total_seconds())/3600
    # Departure_Delay_inHours = abs((first_flight.departure_time - flight_tuple[0].departure_time).total_seconds())/3600

    DelayScore = 0

    # Treating preponing and postponing differently for departure
    Departure_Delay_inHours = (first_flight.departure_time - flight_tuple[0].departure_time).total_seconds()/3600
    if (Departure_Delay_inHours <= -6):
        DelayScore += 0.00000001
    elif(Departure_Delay_inHours < 0):
        DelayScore += 10
    elif (Departure_Delay_inHours <= 6):
        DelayScore += STD6h
    elif (Departure_Delay_inHours <= 12):
        DelayScore += STD12h
    elif (Departure_Delay_inHours <= 24):
        DelayScore += STD24h
    elif (Departure_Delay_inHours <= 48):
        DelayScore += STD48h
    else:
        DelayScore += 0.00000001

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

    # if(Departure_Delay_inHours <= 6):
    #     DelayScore += STD6h
    # elif(Departure_Delay_inHours <= 12):
    #     DelayScore += STD12h
    # elif(Departure_Delay_inHours <= 24):
    #     DelayScore += STD24h
    # elif(Departure_Delay_inHours <= 48):
    #     DelayScore += STD48h
    # else:
    #     DelayScore += 0.00000001
    
    # ConnectionScore -> If proposed flight solutions's length increases, score decreases   
                        # If proposed original flight solutions's length decreases, score increases
    ConnectionScore = constants_immutable.connection_constant - len(flight_tuple) + len(constants_immutable.pnr_flight_mapping[PNR.pnr_number])
    min_DelayScore = 0.00000002
    max_DelayScore = STD6h + arrDelay6h
    max_ConnectionScore = constants_immutable.connection_constant + 3
    min_ConnectionScore = constants_immutable.connection_constant - 3
    return ((DelayScore-min_DelayScore)/(max_DelayScore - min_DelayScore)) * ((ConnectionScore-min_ConnectionScore)/(max_ConnectionScore-min_ConnectionScore))*10

def class_difference_score(PNR, cabin_Tuple):
    """
    Calculates the class difference score for each PNR to flight mapping.
    """
    Cabin_Cost = {
        # Based on Empirical Cost values of flight tickets of these classes
        "EC": 1,
        "PC": 1.5,
        "BC": 3,
        "FC": 6
    }
    # Downgrades are penalized more than upgrades are rewarded
    # Score returned is 1 ( log(1) == 0 )
    upgrade_multiplier = 1.3
    downgrade_multiplier = 1.0/1.5
    sug_sum = 0
    pre_sum = 0
    for i in range(len(cabin_Tuple)):
        sug_sum += Cabin_Cost[cabin_Tuple[i]]
    for i in range(len(PNR.sub_class_list)):
        pre_sum += Cabin_Cost[PNR.get_cabin(PNR.sub_class_list[i])]
    sug_sum /= len(cabin_Tuple)
    pre_sum /= len(PNR.sub_class_list)
    ratio = sug_sum/pre_sum
    if(ratio > 1 and upgrade):
        return upgrade_multiplier*ratio
    elif(ratio > 1 and not upgrade):
        return 0.0
    elif ratio==1:
        return 1
    elif(ratio < 1 and downgrade):
        return downgrade_multiplier*ratio
    elif(ratio < 1 and not downgrade):
        return 0.0
