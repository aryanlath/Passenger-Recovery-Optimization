# Flight Number	Remaining Capacity A	Remaining Capacity F	Departure City	Departure Time	Arrival City	Arrival Time	Status
from datetime import datetime

def convert_to_datetime(time):
        #date_format = "%Y-%m-%d %H:%M"
        date_format = "%Y-%m-%d %H:%M:%S" 
        return datetime.strptime(time, date_format)


class Flight:
    
    def _init_(self,inventory_id,schedule_id,flight_number,aircraft_type,departure_city,arrival_city,total_capacity,total_inventory,booked_inventory,oversold,remaining_inventory,first_class,business_class,premium_economy_class,economy_class,fc_total_inventory,fc_booked_inventory,fc_oversold,fc_available_inventory,bc_total_inventory,bc_booked_inventory,bc_oversold,bc_available_inventory,pc_total_inventory,pc_booked_inventory,pc_oversold,pc_available_inventory,ec_total_inventory,ec_booked_inventory,ec_oversold,ec_available_inventory,fc_cd,bc_cd,pc_cd,ec_cd, departure_time,arrival_time,status):
        #self.flight_number = str(flight_number)
        #self.cabins = cabins
        #self.departure_city = departure_city
        #self.arrival_city = arrival_city
        #self.arrival_time = convert_to_datetime(arrival_time)
        #self.departure_time = convert_to_datetime(departure_time)
        #self.status = status.lower()=="on time"
        
        self.inventory_id = inventory_id
        self.schedule_id = schedule_id
        self.flight_number = str(flight_number)
        #self.aircraft_type = aircraft_type #no need
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        #self.total_capacity = total_capacity #no need
        #self.total_inventory = total_inventory # no need
        #self.booked_inventory = booked_inventory#remaining
        #self.oversold = oversold#no need
        self.remaining_inventory = remaining_inventory 
        #self.first_class = first_class
        #self.business_class = business_class
        #self.premium_economy_class = premium_economy_class
        #self.economy_class = economy_class
        #self.fc_total_inventory = fc_total_inventory
        #self.fc_booked_inventory = fc_booked_inventory
        #self.fc_oversold = fc_oversold
        self.fc_available_inventory = fc_available_inventory #only this
        #self.bc_total_inventory = bc_total_inventory
        #self.bc_booked_inventory = bc_booked_inventory
        #self.bc_oversold = bc_oversold
        self.bc_available_inventory = bc_available_inventory #only this
        #self.pc_total_inventory = pc_total_inventory
        #self.pc_booked_inventory = pc_booked_inventory
        #self.pc_oversold = pc_oversold
        self.pc_available_inventory = pc_available_inventory
        #self.ec_total_inventory = ec_total_inventory
        #self.ec_booked_inventory = ec_booked_inventory
        #self.ec_oversold = ec_oversold
        self.ec_available_inventory = ec_available_inventory
        self.fc_cd = fc_cd
        self.bc_cd = bc_cd
        self.pc_cd = pc_cd
        self.ec_cd = ec_cd
        self.departure_time = convert_to_datetime(departure_time)
        self.arrival_time = convert_to_datetime(arrival_time)
        self.status = status.lower()


        


    def _hash_(self) -> int:
        return hash(self.flight_number)
    
    def _eq_(self, other):
        return isinstance(other, Flight) and self.flight_number == other.flight_number

    def _repr_(self):
        return (
            f"Flight("
            f"Inventory ID: {self.inventory_id}, "
            #f"Schedule ID: {self.schedule_id}, "
            #f"Flight Number: {self.flight_number}, "
            f"Departure City: {self.departure_city}, "
            f"Arrival City: {self.arrival_city}, "
            f"Remaining Inventory: {self.remaining_inventory}, "
            f"FC: {self.fc_available_inventory}, "
            f"BC: {self.bc_available_inventory}, "
            f"PEC: {self.pc_available_inventory}, "
            f"EC: {self.ec_available_inventory}, "
            #f"First Class CD: {self.fc_cd}, "
            #f"Business Class CD: {self.bc_cd}, "
            #f"Premium Economy Class CD: {self.pc_cd}, "
            #f"Economy Class CD: {self.ec_cd}, "
            f"Depart Time: {self.departure_time}, "
            f"Arrival Time: {self.arrival_time}, "
            f"Status: {self.status})"
        )
    

