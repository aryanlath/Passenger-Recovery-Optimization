# Flight Number	Remaining Capacity A	Remaining Capacity F	Departure City	Departure Time	Arrival City	Arrival Time	Status
from datetime import datetime

def convert_to_datetime(time):
    #date_format = "%Y-%m-%d %H:%M"
    date_format = "%Y-%m-%d %H:%M:%S" 
    return datetime.strptime(time, date_format)


class Flight:
    
    def __init__(self,inventory_id,schedule_id,flight_number,aircraft_type,departure_city,arrival_city,total_capacity,total_inventory,booked_inventory,oversold,remaining_inventory,fc_capacity,bc_capacity,pc_capacity,ec_capacity,fc_total_inventory,fc_booked_inventory,fc_oversold,fc_available_inventory,bc_total_inventory,bc_booked_inventory,bc_oversold,bc_available_inventory,pc_total_inventory,pc_booked_inventory,pc_oversold,pc_available_inventory,ec_total_inventory,ec_booked_inventory,ec_oversold,ec_available_inventory,fc_class_dict,bc_class_dict,pc_class_dict,ec_class_dict, departure_time,arrival_time,status):

        """
            *class_dict is a dictionary with each subclass capacities in a cabin
            status is a string converted to lowercase 
        """
        self.inventory_id = inventory_id
        self.schedule_id = schedule_id
        self.flight_number = str(flight_number)
        #self.aircraft_type = aircraft_type #no need
        self.departure_city = departure_city
        self.arrival_city = arrival_city
        #self.total_capacity = total_capacity #no need
        #self.total_inventory = total_inventory # no need
        #self.booked_inventory = booked_inventory#remaining
        #self.oversold = oversold #no need
        self.remaining_inventory = int(remaining_inventory) 
        #self.first_class = first_class
        #self.business_class = business_class
        #self.premium_economy_class = premium_economy_class
        #self.economy_class = economy_class
        #self.fc_total_inventory = fc_total_inventory
        #self.fc_booked_inventory = fc_booked_inventory
        #self.fc_oversold = fc_oversold
        self.fc_available_inventory = int(fc_available_inventory) #only this
        #self.bc_total_inventory = bc_total_inventory
        #self.bc_booked_inventory = bc_booked_inventory
        #self.bc_oversold = bc_oversold
        self.bc_available_inventory = int(bc_available_inventory) #only this
        #self.pc_total_inventory = pc_total_inventory
        #self.pc_booked_inventory = pc_booked_inventory
        #self.pc_oversold = pc_oversold
        self.pc_available_inventory = int(pc_available_inventory)
        #self.ec_total_inventory = ec_total_inventory
        #self.ec_booked_inventory = ec_booked_inventory
        #self.ec_oversold = ec_oversold
        self.ec_available_inventory = int(ec_available_inventory)
        self.fc_class_dict = fc_class_dict
        self.bc_class_dict = bc_class_dict
        self.pc_class_dict = pc_class_dict
        self.ec_class_dict = ec_class_dict
        self.departure_time = convert_to_datetime(departure_time)
        self.arrival_time = convert_to_datetime(arrival_time)
        self.status = status.lower()
        self.cabins = ['FC','BC','PC','EC']

    def __hash__(self) -> int:
        return hash(self.inventory_id)
    
    def __eq__(self, other):
        return isinstance(other, Flight) and self.inventory_id == other.inventory_id
    
    def get_capacity(self, cabin):
        """Get the capacity given the cabin"""
        cabin_capacities={'FC':self.fc_available_inventory, 'BC':self.bc_available_inventory, 'EC':self.ec_available_inventory,'PC':self.pc_available_inventory}
        return cabin_capacities[cabin]

    def __repr__(self):
        return (
            f"Flight('Inventory ID: {self.inventory_id}, FC: {self.fc_class_dict}, BC: {self.bc_class_dict}, PC: {self.pc_class_dict}, EC: {self.ec_class_dict}, Flight Number: {self.flight_number}, Departure City: {self.departure_city}, Arrival City: {self.arrival_city} "
        )
    

