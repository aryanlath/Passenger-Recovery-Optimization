
# If needed import constants.py

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
        pass

    def get_ssr_score(self):
        """
            Returns the score associated with this SSR string (ex. WCHR , DEAF )

        """
        pass
    def get_pnr_score(self):
        """
            Returns the Total PNR score of this object
        """

        pass