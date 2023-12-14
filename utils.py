import pandas as pd
from constants import *
from Models.PNR import *
from Models.Flights import *
from collections import defaultdict
import constants_immutable 
import copy
import pprint
import json
from datetime import datetime
pp = pprint.PrettyPrinter(indent=4)

def string_to_dict(string_dict):
    # Remove curly braces and split by commas
    pairs = string_dict[1:-1].split(', ')

    # Create a dictionary from key-value pairs
    actual_dict = {}
    for pair in pairs:
        key, value = pair.split(': ')
        actual_dict[key.strip("'")] = int(value)

    return actual_dict

def get_all_airports(file_name):
    df = pd.read_csv(file_name)
    airports = set()
    for _, row in df.iterrows():
        departure_city = row['DepartureAirport']
        arrival_city = row['ArrivalAirport']
        airports.add(departure_city)
        airports.add(arrival_city)
    return airports


def extract_Flights_from_CSV(file_name):
    flights = []
    df = pd.read_csv(file_name)

    for _, row in df.iterrows():
        inventory_id = row['InventoryId']
        schedule_id = row['ScheduleId']
        flight_number = row['FlightNumber']
        aircraft_type = row['AircraftType']
        departure_city = row['DepartureAirport']
        arrival_city = row['ArrivalAirport']
        total_capacity = row['TotalCapacity']
        total_inventory = row['TotalInventory']
        booked_inventory = row['BookedInventory']
        oversold = row['Oversold']
        available_inventory = row['AvailableInventory']
        first_class = row['FirstClass']
        business_class = row['BusinessClass']
        premium_economy_class = row['PremiumEconomyClass']
        economy_class = row['EconomyClass']
        fc_total_inventory = row['FC_TotalInventory']
        fc_booked_inventory = row['FC_BookedInventory']
        fc_oversold = row['FC_Oversold']
        fc_available_inventory = row['FC_AvailableInventory']
        bc_total_inventory = row['BC_TotalInventory']
        bc_booked_inventory = row['BC_BookedInventory']
        bc_oversold = row['BC_Oversold']
        bc_available_inventory = row['BC_AvailableInventory']
        pc_total_inventory = row['PC_TotalInventory']
        pc_booked_inventory = row['PC_BookedInventory']
        pc_oversold = row['PC_Oversold']
        pc_available_inventory = row['PC_AvailableInventory']
        ec_total_inventory = row['EC_TotalInventory']
        ec_booked_inventory = row['EC_BookedInventory']
        ec_oversold = row['EC_Oversold']
        ec_available_inventory = row['EC_AvailableInventory']
        fc_cd = string_to_dict(str(row['FC_CD']))
        bc_cd = string_to_dict(str(row['BC_CD']))
        pc_cd = string_to_dict(str(row['PC_CD']))
        ec_cd = string_to_dict(str(row['EC_CD']))
        departure_time = row['DepartureDatetime']
        arrival_time = row['ArrivalDatetime']
        status = row['Status']
        flight = Flight(
            inventory_id, schedule_id, flight_number, aircraft_type, departure_city, arrival_city,
            total_capacity, total_inventory, booked_inventory, oversold, available_inventory,
            first_class, business_class, premium_economy_class, economy_class,
            fc_total_inventory, fc_booked_inventory, fc_oversold, fc_available_inventory,
            bc_total_inventory, bc_booked_inventory, bc_oversold, bc_available_inventory,
            pc_total_inventory, pc_booked_inventory, pc_oversold, pc_available_inventory,
            ec_total_inventory, ec_booked_inventory, ec_oversold, ec_available_inventory,
            fc_cd, bc_cd, pc_cd, ec_cd, departure_time, arrival_time, status
        )
        flights.append(flight)

    return flights


def Get_Flight_Map():
    all_flights = {}
    all_flight  = extract_Flights_from_CSV(test_flight_data_file)
    for flight in all_flight:
        all_flights[flight.inventory_id] = flight
    return all_flights


def sort_and_remove_number(strings):
    # Sort the strings based on the numeric value after '#' and return the splitted string list
    sorted_strings = sorted(strings, key=lambda s: int(s.split('#')[1]))

    return [s.split('#')[0] for s in sorted_strings]


def extract_PNR_from_CSV(file_path):
    """
    We split the inv_list of a PNR as soon as we see a flight that is >=72 hrs to handle round trip aand multi-city booking cases
    returns the list of PNR_objects, map of originalPNR_number to split PNR_Numbers eg: {"PNR001": ["PNR001#0", "PNR001#1"]}
    """
    pnr_dict = {}
    df = pd.read_csv(file_path)
    for _,row in df.iterrows():
        pnr_number = row['RECLOC']
        subclass = row['COS_CD']
        seg_seq = int(row['SEG_SEQ'])
        pax = row['PAX_CNT']
        inv_id = row.get('INV_ID', None)
        passenger_loyalty = row.get('LOYALTY', 'CM')
        special_requirements = row.get('SSR', "Grade2")
        email_id = row.get('CONTACT_EMAIL', "g-s01@outlook.com")

        # To get the Legs of flight ordered by seq_number

        if(pnr_dict.get(pnr_number) is None):
            pnr_dict[pnr_number] = PNR(pnr_number,[inv_id+"#"+str(seg_seq)],[subclass+"#"+str(seg_seq)],special_requirements,pax,passenger_loyalty,email_id)
        else:
            pnr_dict[pnr_number].inv_list.append(inv_id+"#"+str(seg_seq),)
            pnr_dict[pnr_number].sub_class_list.append(subclass+"#"+str(seg_seq))

    # Cleaning up the # and sorting according to the seg_seq
    for key,value in pnr_dict.items():
        value.inv_list = sort_and_remove_number(value.inv_list)
        value.sub_class_list = sort_and_remove_number(value.sub_class_list)
    pnr_objects=[]
    pnr_to_split_pnrs=defaultdict(list)
    all_flights=Get_Flight_Map()
    pnr_dict_cpy=copy.deepcopy(pnr_dict)
    next_time=[]
    for key,pnr_object in pnr_dict_cpy.items():
        start=0
        partitions=[]
        prev_arrival_time=None
        for flight in pnr_object.inv_list:
            if(start==0):
                prev_arrival_time=all_flights[flight].arrival_time
                start+=1
            else:
                if(abs(all_flights[flight].departure_time.timestamp()-prev_arrival_time.timestamp())>MAXCT*60*60):
                    partitions.append(start)
                    next_time.append(all_flights[flight].departure_time)
                prev_arrival_time=all_flights[flight].arrival_time
                start+=1
        if(len(partitions)==0):
            continue
        curr_len=0
        curr_list=[]
        curr_subclass=[]
        num_of_partitions=0

        while(curr_len<len(pnr_object.inv_list)):
            if(curr_len in partitions):
                pnr_to_split_pnrs[key].append(key+"#"+str(num_of_partitions))
                temp=copy.deepcopy(curr_list)
                temp1=copy.deepcopy(curr_subclass)
                pnr_dict[key+"#"+str(num_of_partitions)]=PNR(key+"#"+str(num_of_partitions),temp,temp1,special_requirements,pax,passenger_loyalty,email_id,next_time[num_of_partitions])
                curr_list.clear()
                curr_subclass.clear()
                curr_list.append(pnr_object.inv_list[curr_len])
                curr_subclass.append(pnr_object.sub_class_list[curr_len])
                curr_len+=1
                num_of_partitions+=1
            else:
                curr_list.append(pnr_object.inv_list[curr_len])
                curr_subclass.append(pnr_object.sub_class_list[curr_len])
                curr_len+=1
        if(len(curr_list)>0):
            pnr_to_split_pnrs[key].append(key+"#"+str(num_of_partitions))
            pnr_dict[key+"#"+str(num_of_partitions)]=PNR(key+"#"+str(num_of_partitions),curr_list,curr_subclass,special_requirements,pax,passenger_loyalty,email_id)
 
        del pnr_dict[pnr_object.pnr_number]
    
    for key,pnr_object in pnr_dict.items():
        pnr_objects.append(pnr_object)
    
    return pnr_objects,pnr_to_split_pnrs

def convert_result_to_csv(result):
    dataframe = pd.DataFrame()
    PNR = []
    Flight = []
    Cabin = []
    ArrivalCity= []
    DepartureCity = []
    ArrivalTime = []
    DepartureTime = []
    

    
    for result_entry in result['Assignments']:
        PNR.append(result_entry[0].pnr_number)
        Flight.append(result_entry[1].flight_number)
        Cabin.append(result_entry[2])
        ArrivalCity.append(result_entry[1].arrival_city)
        DepartureCity.append(result_entry[1].departure_city)
        ArrivalTime.append(result_entry[1].arrival_time)
        DepartureTime.append(result_entry[1].departure_time)
    dataframe['PNR'] = PNR
    dataframe['Flight'] = Flight 
    dataframe['Cabin'] = Cabin
    dataframe['Arrival City'] = ArrivalCity
    dataframe['Departure City'] = DepartureCity
    dataframe['Arrival Time'] = ArrivalTime
    dataframe['Departure Time'] = DepartureTime
    dataframe.to_csv('result.csv',index = False)


# pnr_object=parse_pnr_file(test_PNR_data_file)
# print(pnr_object)

def find_airport_location(airport_code):
    """
    This function creates a dictionary of airport codes and their corresponding locations in the form of (longitude, latitude).
    Usage: (longitude, latitude) = find_airport_location(airport_code)
    Example: (longitude, latitude) = find_airport_location('BOM')
    """
    df = pd.read_csv(airport_code_location_data_file)
    for _, row in df.iterrows():
        if row['iata'] == airport_code and row['latitude'] is not None and row['longitude'] is not None:
            return row['latitude'], row['longitude']
    # return None, None



def sort_solution_schemes(schemes_list, exceptions_handled):
    """
        Inputs:
            schemes_list: List of schemes taken input from Leap_Quantum2.py/main
                          each element of list is a dictionary of the form { 'Assignments' : [ (PNR,Flight,Cabin)] , 'Non Assignments' : [PNR]}
        Outputs:
            List of scores of every scheme based on the 4 metrics given in the solution ranking file;
                1) No. of Unassigned Passengers
                2) No. of PNRs handled in exception list
                3) Mean Arrival Delay
                4) 1-Multi
    """
    final_score = []
    for idx,scheme in enumerate(schemes_list):
        
        score_1 = len(scheme['Non Assignments']) - exceptions_handled[idx]
        score_2 = len(scheme['Non Assignments'])
        score_3  = 0 
        score_4 = 0
        total_assigned = len(scheme['Assignments'])
        

        for assignment in scheme['Assignments']:
            # Each assignment is of the form (PNR , Flight_Tuple , Cabin_Tuple)
            initial_arrival_time = constants_immutable.all_flights[assignment[0].inv_list[-1]].arrival_time 
            final_arrvial_time = assignment[1][-1].arrival_time
            arr_delay = (abs((final_arrvial_time - initial_arrival_time)).total_seconds())/3600
            score_3+=arr_delay

            initial_count_flights = len(assignment[0].inv_list)
            final_count_flights = len(assignment[1])
            if(final_count_flights > initial_count_flights) :
                score_4+=1 
            elif(final_count_flights < initial_count_flights):
                score_4-=1
            
        score_3/=total_assigned

        final_score.append((score_1, score_2, score_3, score_4))

    return final_score

                
def AssignmentsToJSON( Cabin_Class_Assignments) :
    """ 
        Output : Returns JSON of this structure;
            Structure->

                { "PNR Number" : {
                            "Original" : {
                                [
                                    [
                                        INV_ID_1 , CABIN_1 , [Sub_Class List_1]
                                    ],
                                    [
                                        INV_ID_2 , CABIN_2 , [Sub_Class List_2]
                                    ],
                                    ...
                                ]
                            }
                            "Proposed" :{
                                similar to original
                            }
                    }
                }
    """
    final_ans = {}
    for pnr_number , val in  Cabin_Class_Assignments.items():
        final_ans[pnr_number]={} 
        final_ans[pnr_number]["Original"] =[]
        final_ans[pnr_number]["Proposed"]=[]
        My_Pnr_obj = constants_immutable.pnr_objects[pnr_number]
        final_ans[pnr_number]["Email"] = My_Pnr_obj.email_id
        Orig_inv_list=  My_Pnr_obj.inv_list
        Orig_subclass_list = My_Pnr_obj.sub_class_list
        for idx, val1 in enumerate(Orig_inv_list):
            temp_list =[]
            temp_list.append(val1)
            temp_list.append(constants_immutable.pnr_objects[pnr_number].get_cabin(Orig_subclass_list[0]))
            temp_list_2 = [Orig_subclass_list[idx]]*(My_Pnr_obj.PAX)
            temp_list.append(temp_list_2)
            temp_list.append(str(constants_immutable.all_flights[val1].departure_time))
            temp_list.append(str(constants_immutable.all_flights[val1].arrival_time))
            final_ans[pnr_number]["Original"].append(temp_list)
        
        num_of_proposed_flights = int(len(val)/My_Pnr_obj.PAX)
        
        for i in range(num_of_proposed_flights):
            temp_sub_class_list = []
            temp_list=[val[i*My_Pnr_obj.PAX][1].inventory_id , val[i*My_Pnr_obj.PAX][2]]
            for j in range(i*My_Pnr_obj.PAX, (i+1)*My_Pnr_obj.PAX):
                temp_sub_class_list.append(val[j][3])
            temp_list.append(temp_sub_class_list)
            temp_list.append(str(constants_immutable.all_flights[val[i*My_Pnr_obj.PAX][1].inventory_id].departure_time))
            temp_list.append(str(constants_immutable.all_flights[val[i*My_Pnr_obj.PAX][1].inventory_id].arrival_time))
            final_ans[pnr_number]["Proposed"].append(temp_list)
                
    return json.dumps(final_ans,indent=4)


def up_dn_arr_delay(json_final):
     ## Stats
    dict_final = json.loads(json_final)
    up_cnt = 0
    dn_cnt = 0
    arr_del = 0
    cabin_cost = {
        # Based on Empirical Cost values of flight tickets of these classes
        "EC": 1,
        "PC": 2,
        "BC": 3,
        "FC": 4
    }
    for pnr_num, value in dict_final.items():
        class_score_init = 0
        class_score_fin = 0
        for i in range(len(value['Original'])):
            class_score_init += cabin_cost[value['Original'][i][1]]
        for i in range(len(value['Proposed'])):
            class_score_fin += cabin_cost[value['Proposed'][i][1]]
        class_score_init/=len(value['Original'])
        class_score_fin/=len(value['Proposed'])
        if class_score_init>class_score_fin:
            dn_cnt+=1
        elif class_score_init<class_score_fin:
            up_cnt+=1
        
        init_arr_time = datetime.strptime(value['Original'][-1][-1], "%Y-%m-%d %H:%M:%S")
        fin_arr_time = datetime.strptime(value['Proposed'][-1][-1], "%Y-%m-%d %H:%M:%S")
        arr_del += abs((fin_arr_time - init_arr_time).total_seconds() / 3600)

    ## Stats
    return up_cnt, dn_cnt, arr_del


def count_one_multi(json_final):

    dict_final = json.loads(json_final)
    one_one_temp = 0
    one_multi_temp = 0
    multi_one_temp = 0
    multi_multi_temp = 0

    for pnr_num, value in dict_final.items():
        if len(value['Original'])==1 and len(value['Proposed'])==1:
            one_one_temp+=1
        elif len(value['Original'])<len(value['Proposed']):
            one_multi_temp+=1
        elif len(value['Original'])>len(value['Proposed']):
            multi_one_temp+=1
        else:
            multi_multi_temp+=1
    
    return one_one_temp, one_multi_temp, multi_one_temp, multi_multi_temp



def write_list_to_file(listname,list,file):
    file.write(str(listname)+" = [")
    for i in range(len(list)):
        if i!=len(list)-1:
            file.write(str(list[i])+",")
        else:
            file.write(str(list[i])+"]\n")
        





def GetTotalPAX( result,isAssignments):
    """
        result : list of tuples of the form (PNR,FT,CABIN) of each assignment, or list of PNR objects
        in the case of non assignment list.
        Pass quantumresult[i]['Assignments']/['Non Assignments] in this function
        isAssignments : boolean indicating whether this is Assignment list or non assignment list 
    """
    Total_PAX_Count = 0 
    for tup in result:
        # currPNR = tup
        if(isAssignments) :
            currPNR = tup[0]
            Total_PAX_Count+= currPNR.PAX
        else :
            currPNR = tup 
            Total_PAX_Count+= currPNR.PAX
    return Total_PAX_Count