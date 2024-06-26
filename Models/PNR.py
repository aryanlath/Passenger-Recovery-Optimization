
# If needed 
from constants import PNR_pax,PNR_SSR,loyalty

class PNR:
    def __init__(self, pnr_number,inv_list, sub_class_list, special_requirements,PAX, passenger_loyalty,email_id,next_leg=None):

        # inv_list -> list of inventory ids for this pnr (all the connecting flights)
        # sub_class_list -> list of all the subclasses this PNR is travelling in for each leg of journey
        self.pnr_number = pnr_number
        self.inv_list = inv_list
        self.sub_class_list  = sub_class_list
        self.special_requirements = special_requirements 
        self.PAX = int(PAX)
        self.passenger_loyalty = passenger_loyalty
        self.email_id = email_id
        self.next_leg=next_leg

    def __hash__(self) -> int:
        return hash(self.pnr_number)
    
    def __eq__(self, other):
        return isinstance(other, PNR) and self.pnr_number == other.pnr_number
    
    def __repr__(self):
        return f"PNR('{self.pnr_number}', {self.inv_list}, {self.sub_class_list}, {self.PAX},{self.next_leg})"
    
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
        return loyalty[self.passenger_loyalty]

    def get_ssr_score(self):
        """
            Returns the score associated with this SSR string (ex. WCHR , DEAF )
            
        """
        if(self.special_requirements == "Grade1"):
            return PNR_SSR["grade1"]
        elif (self.special_requirements=="Grade2"):
            return PNR_SSR["grade2"]

    def min_max_ssr_score(self):
        """
            Returns the maximum and minimum score associated with the SSR string
        """
        
        return min(PNR_SSR.values()),max(PNR_SSR.values())
    
    def min_max_loyalty_score(self):
        """
            Returns the maximum and minimum score associated with the loyalty string
        """
        
        return min(loyalty.values()),max(loyalty.values())
    
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
        min_s1, max_s1 = self.min_max_ssr_score()
        min_s2, max_s2 = self.min_max_loyalty_score()
        min_s3 = self.PAX
        max_s3 = self.PAX*9
        s1 = (s1-min_s1)/(max_s1-min_s1)
        s2 = (s2-min_s2)/(max_s2-min_s2)
        s3 = (s3-min_s3)/(max_s3-min_s3)
        s4 = s1+s2
        s4 = s4/2
        return s3 + s4
