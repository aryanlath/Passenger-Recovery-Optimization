
import constants_immutable

loyalty_dict = {}

def init_normalize_factors():
    """
    Initializes the normalization factors
    """
    for pnr in constants_immutable.pnr_to_s2:
        constants_immutable.pnr_normalize_factor = max(constants_immutable.pnr_normalize_factor, constants_immutable.pnr_to_s2[pnr])
    constants_immutable.flight_normalize_factor = 100
    constants_immutable.cabin_normalize_factor = 100

# def init_loyalty_dictionary():
#     """
#     Initialize the loyalty dictionary
#     """
#     global loyalty_dict
#     loyalty_dict["CM"] = Loyalty_CM
#     loyalty_dict["Platinum"] = Loyalty_platinum
#     loyalty_dict["Gold"] = Loyalty_gold
#     loyalty_dict["Silver"] = Loyalty_silver