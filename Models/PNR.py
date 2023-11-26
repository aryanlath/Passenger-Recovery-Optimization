class PNR:
    def __init__(self, pnr_number, flight_cabin, flight_number, special_requirements, is_checkin,passenger_loyalty,PAX):
        self.pnr_number = pnr_number
        self.flight_cabin  = flight_cabin
        self.flight_number = flight_number
        self.special_requirements = special_requirements
        self.is_checkin = is_checkin
        self.passenger_loyalty = passenger_loyalty
        self.PAX = PAX
        
    def get_pnr_score(self):
        return 10*self.PAX
