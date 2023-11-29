class PNR:
    def __init__(self, pnr_number, flight_cabin, flight_number, special_requirements, is_checkin,passenger_loyalty,PAX):
        self.pnr_number = pnr_number
        self.flight_cabin  = flight_cabin
        self.flight_number = str(flight_number)
        self.special_requirements = special_requirements == "True"
        self.is_checkin = is_checkin == "true"
        self.passenger_loyalty = passenger_loyalty
        self.PAX = int(PAX)

    def __hash__(self) -> int:
        return hash(self.pnr_number)
    
    def __eq__(self, other):
        return isinstance(other, PNR) and self.pnr_number == other.pnr_number
    
    def __repr__(self):
        return f"'{self.pnr_number}', '{self.flight_cabin}', '{self.PAX}'"
    
    def get_pnr_score(self):
        return 10*self.PAX
