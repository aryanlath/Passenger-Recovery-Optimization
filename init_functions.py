from constants import Loyalty_CM,Loyalty_platinum,Loyalty_gold,Loyalty_silver,pnr_normalize_factor,flight_normalize_factor,cabin_normalize_factor
import constants_immutable

loyalty_dict = {}

def init_normalize_factors():
    global pnr_normalize_factor
    for pnr in constants_immutable.pnr_to_s2:
        pnr_normalize_factor = max(pnr_normalize_factor, constants_immutable.pnr_to_s2[pnr])
    global flight_normalize_factor
    flight_normalize_factor = 100
    global cabin_normalize_factor
    cabin_normalize_factor = 100

def init_loyalty_dictionary():
    """
    Initialize the loyalty dictionary
    """
    global loyalty_dict
    loyalty_dict["CM"] = Loyalty_CM
    loyalty_dict["Platinum"] = Loyalty_platinum
    loyalty_dict["Gold"] = Loyalty_gold
    loyalty_dict["Silver"] = Loyalty_silver