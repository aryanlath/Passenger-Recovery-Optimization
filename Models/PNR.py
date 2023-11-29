class PNR:
    def __init__(self, pnr_number,inv_list, cabin_list, special_requirements,PAX, passenger_loyalty,is_checkin):
        self.pnr_number = pnr_number
        self.inv_list = inv_list
        self.cabin_list  = cabin_list
        self.special_requirements = special_requirements == "True"
        self.is_checkin = is_checkin == "true"
        self.PAX = PAX
        self.passenger_loyalty = passenger_loyalty
        

    def __hash__(self) -> int:
        return hash(self.pnr_number)
    
    def __eq__(self, other):
        return isinstance(other, PNR) and self.pnr_number == other.pnr_number
    
    def __repr__(self):
        return f"PNR('{self.pnr_number}', {self.inv_list}, {self.cabin_list}, {self.PAX})"
    
    def get_pnr_score(self):
        return 10*self.PAX
