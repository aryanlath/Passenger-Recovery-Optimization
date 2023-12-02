
# If needed 
<<<<<<< HEAD
from constants import *
loyalty_dict = {}

def init_normalize_factors(all_flights,pnr_objects,pnr_flight_mapping,pnr_to_s2):
    global pnr_normalize_factor
    for pnr in pnr_to_s2:
        pnr_normalize_factor = max(pnr_normalize_factor,pnr_to_s2[pnr])
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
=======
from init_functions import loyalty_dict
from constants import PNR_pax,PNR_SSR
>>>>>>> 9461a07c42f71c23d79e98119de277f84ac2672b

class PNR:
    def __init__(self, pnr_number,inv_list, sub_class_list, special_requirements,PAX, passenger_loyalty,email_id):

        # inv_list -> list of inventory ids for this pnr (all the connecting flights)
        # sub_class_list -> list of all the subclasses this PNR is travelling in for each leg of journey
        self.pnr_number = pnr_number
        self.inv_list = inv_list
        self.sub_class_list  = sub_class_list
        self.special_requirements = special_requirements 
        self.PAX = int(PAX)
        self.passenger_loyalty = passenger_loyalty
        self.email_id = email_id

    def __hash__(self) -> int:
        return hash(self.pnr_number)
    
    def __eq__(self, other):
        return isinstance(other, PNR) and self.pnr_number == other.pnr_number
    
    def __repr__(self):
        return f"PNR('{self.pnr_number}', {self.inv_list}, {self.sub_class_list}, {self.PAX})"
    
    def get_cabin(self,sub_class):
        """
        Returns the cabin of this PNR given the sub_class
        """
        subclass_to_class_mapping = {
        'F': 'FC', 'P': 'FC',   # First Class
        'C': 'BC', 'J': 'BC', 'Z': 'BC',  # Business Class
        'Q': 'PC', 'R': 'PC', 'S': 'PC', 'T': 'PC', 'H': 'PC', 'M': 'PC',  # Premium Class
        'Y': 'EC', 'A': 'EC', 'B': 'EC', 'D': 'EC', 'E': 'EC', 'G': 'EC', 'I': 'EC', 'K': 'EC', 'L': 'EC', 'N': 'EC', 'O': 'EC', 'U': 'EC', 'V': 'EC', 'W': 'EC', 'X': 'EC'  # Economy Class
        }
        return subclass_to_class_mapping[sub_class]
    
    def get_loyalty_score(self):
        """
            Returns the score associated with the loyalty string (ex. Gold Silver Platinum)
        """
        # Assuming that constants.py has a dictionary where key is string(loyalty_class) and value is score for that loyalty
        return loyalty_dict[self.passenger_loyalty]

    def get_ssr_score(self):
        """
            Returns the score associated with this SSR string (ex. WCHR , DEAF )
            
        """
        if(self.special_requirements == "Grade1"):
            return PNR_SSR
        elif (self.special_requirements=="Grade2"):
            return PNR_SSR/2
    
    def get_pnr_score(self):
        """
        Calculates the PNR score for each PNR.
        Calculation done as follows: score = a*s1 + b*s2 + c*s3
        where,  s1 = PNR_SSR
                s2 = PNR_loyalty
                s3 = PNR_pax
        """
        #TODO normalize s1 , s2 ,s3 if required 
        s1 = self.get_ssr_score()
        s2 = self.get_loyalty_score()
        s3 = self.PAX * PNR_pax
        return s1 + s2 + s3