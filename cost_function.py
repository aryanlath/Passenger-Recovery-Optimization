from utils import *
from Models.Flights import Flight
import feasible_flights 
from constants import *

def cost_function(PNR,flight,Cabin):
    """
    Calculates the cost function for each PNR to flight mapping.
    Calculation done as follows: cost = a*log(s1) + b*log(s2) + c*log(s3)
    where, s1 = flight quality score
           s2 = PNR score
           s3 = class difference score
    """
    s1 = flight_quality_score(PNR, flight)
    s2 = PNR_score(PNR)/pnr_normalize_factor
    s3 = class_difference_score(PNR,flight,Cabin)
    cost = weight_flight_map*log(s1) + weight_pnr_map*log(s2) + weight_cabin_map*log(s3)
    return None 
    

def PNR_Score(PNR):

    final_pnr_score = 0
    PNR_PAX_score = PNR.PAX * PNR_pax 
    PNR_Loyalty_score = Loyalty_CM
    PNR_SSR_Score = 











