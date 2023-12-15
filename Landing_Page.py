##MAIN FUNCTION CODE

import streamlit as st
from feasible_flights import *
from constants import *
from init_functions import *
from gurobi_optimisation import *
from Leap_Quantum_Main import *
import pprint
import mailer
import constants_immutable
pp = pprint.PrettyPrinter(indent=4)
from Assign_Class import *
import json
import csv
from utils import *


## Global variables(Statistics)

total_impacted = 0
total_impacted_pax = 0
total_assigned = []
total_assigned_pax = []
total_non_assigned = []
upgrade_count = []
downgrade_count = []
same_city_count = []
diff_city_count = [] 
mean_arrival_delay = []
one_multi = []
multi_one = []
multi_multi = []
one_one = []
pnr_score_assigned = []
pnr_score_non_assigned = []
hybrid_results = []


def Landing_Page():

    """
    Function that displays the landing Page and carry out all the main operations
    """


    def writeStatistics():
        f=open("stats.py","w")
        f.write("total_impacted = "+str(total_impacted)+"\n")
        write_list_to_file("total_assigned",total_assigned,f)
        write_list_to_file("total_non_assigned",total_non_assigned,f)
        write_list_to_file("upgrade_count",upgrade_count,f)
        write_list_to_file("downgrade_count",downgrade_count,f)
        write_list_to_file("same_city_count",same_city_count,f)
        write_list_to_file("diff_city_count",diff_city_count,f)
        write_list_to_file("mean_arrival_delay",mean_arrival_delay,f)
        f.write("pnr_score_assigned = [")
        for solution in range(len(pnr_score_assigned)):
            list=pnr_score_assigned[solution]
            if solution!=len(pnr_score_assigned)-1:
                f.write("[")
                for i in range(len(list)):
                    if i!=len(list)-1:
                        f.write(str(list[i])+",")
                    else:
                        f.write(str(list[i]))
                f.write("]")
                f.write(",")
            else:
                f.write("[")
                for i in range(len(list)):
                    if i!=len(list)-1:
                        f.write(str(list[i])+",")
                    else:
                        f.write(str(list[i]))
                f.write("]")
                f.write("]\n")
        f.write("pnr_score_non_assigned = [")
        for solution in range(len(pnr_score_non_assigned)):
            list=pnr_score_non_assigned[solution]
            if solution!=len(pnr_score_non_assigned)-1:
                f.write("[")
                for i in range(len(list)):
                    if i!=len(list)-1:
                        f.write(str(list[i])+",")
                    else:
                        f.write(str(list[i]))
                f.write("]")
                f.write(",")
            else:
                f.write("[")
                for i in range(len(list)):
                    if i!=len(list)-1:
                        f.write(str(list[i])+",")
                    else:
                        f.write(str(list[i]))
                f.write("]")
                f.write("]\n")                                
        f.close()

    def display_results(hybrid_results):
        """
        Display results in streamlit
        """

        if (len(hybrid_results)==2):
            col1,col2=st.columns(2)
            with col1:
                #first solution
                st.write("Solution 1")
                st.write("Total impacted PNRs are :",total_impacted)
                st.write("Reaccommodated PNRs :",total_assigned[0])
                # st.write("Unaccomadated PNRs :",total_non_assigned[0])
                st.write("Total impacted PAX are :",total_impacted_pax)   
                st.write("Reaccommodated PAX :",total_assigned_pax[0])     
                st.write("PNRs Upgraded :",upgrade_count[0])
                st.write("PNRs Downgraded :",downgrade_count[0])
                st.write("PNRs with city pairs same :",same_city_count[0])
                st.write("PNRs with city pairs different :",diff_city_count[0])
                st.write("Mean Arrival Delay(in Hours) :",mean_arrival_delay[0])
                st.write("Multi-Multi(%) :",multi_multi[0])
                
            with col2:
                #second solution
                st.write("Solution 2")
                st.write("Total impacted PNRs are :",total_impacted)
                st.write("Reaccommodated PNRs :",total_assigned[1])
                st.write("Total impacted PAX are :",total_impacted_pax)
                
                st.write("Reaccommodated PAX :",total_assigned_pax[1])
                # st.write("Unaccomadated PNRs :",total_non_assigned[1])
                st.write("PNRs Upgraded :",upgrade_count[1])
                st.write("PNRs Downgraded :",downgrade_count[1])
                st.write("PNRs with city pairs same :",same_city_count[1])
                st.write("PNRs with city pairs different :",diff_city_count[1])
                st.write("Mean Arrival Delay(in Hours) :",mean_arrival_delay[1])
                st.write("Multi-Multi(%) :",multi_multi[1])
                
        else:
            col1,col2,col3=st.columns(3)
            with col1:
                #first solution
                st.write("Solution 1")
                st.write("Total impacted PNRs are :",total_impacted)
                st.write("Reaccommodated PNRs :",total_assigned[0])
                st.write("Total impacted PAX are :",total_impacted_pax)
                
                st.write("Reaccommodated PAX :",total_assigned_pax[0])
                # st.write("Unaccomadated PNRs :",total_non_assigned[0])
                st.write("PNRs Upgraded :",upgrade_count[0])
                st.write("PNRs Downgraded :",downgrade_count[0])
                st.write("PNRs with city pairs same :",same_city_count[0])
                st.write("PNRs with city pairs different :",diff_city_count[0])
                st.write("Mean Arrival Delay(in Hours) :",mean_arrival_delay[0])
                st.write("One-One(%) :",one_one[0])
                st.write("One-Multi(%) :",one_multi[0])
                st.write("Multi-One(%) :",multi_one[0])
                st.write("Multi-Multi(%) :",multi_multi[0])
                
            with col2:
                #second solution
                st.write("Solution 2")
                st.write("Total impacted PNRs are :",total_impacted)
                st.write("Reaccommodated PNRs :",total_assigned[1])
                st.write("Total impacted PAX are :",total_impacted_pax)
                st.write("Reaccommodated PAX :",total_assigned_pax[1])
                
                # st.write("Unaccomadated PNRs :",total_non_assigned[0])
                st.write("PNRs Upgraded :",upgrade_count[1])
                st.write("PNRs Downgraded :",downgrade_count[1])
                st.write("PNRs with city pairs same :",same_city_count[1])
                st.write("PNRs with city pairs different :",diff_city_count[1])
                st.write("Mean Arrival Delay(in Hours) :",mean_arrival_delay[1])
                st.write("One-One(%) :",one_one[1])
                st.write("One-Multi(%) :",one_multi[1])
                st.write("Multi-One(%) :",multi_one[1])
                st.write("Multi-Multi(%) :",multi_multi[1])
                
            with col3:    
                #third solution
                st.write("Solution 3")
                st.write("Total impacted PNRs are :",total_impacted)
                st.write("Reaccommodated PNRs :",total_assigned[2])
                st.write("Total impacted PAX are :",total_impacted_pax)
                st.write("Reaccommodated PAX :",total_assigned_pax[2])
                
                # st.write("Unaccomadated PNRs :",total_non_assigned[2])
                st.write("PNRs Upgraded :",upgrade_count[2])
                st.write("PNRs Downgraded :",downgrade_count[2])
                st.write("PNRs with city pairs same :",same_city_count[2])
                st.write("PNRs with city pairs different :",diff_city_count[2])
                st.write("Mean Arrival Delay(in Hours) :",mean_arrival_delay[2])
                st.write("One-One(%) :",one_one[2])
                st.write("One-Multi(%) :",one_multi[2])
                st.write("Multi-One(%) :",multi_one[2])
                st.write("Multi-Multi(%) :",multi_multi[2])
                  
    def Main_function():
        """
        Main Function that would run the code
        """
        global total_impacted
        global total_impacted_pax
        global total_assigned
        global total_assigned_pax
        global total_non_assigned
        global upgrade_count 
        global downgrade_count
        global diff_city_count  
        global same_city_count
        global mean_arrival_delay 
        global one_multi
        global one_one
        global multi_multi
        global multi_one
        global pnr_score_assigned
        global pnr_score_non_assigned
        global hybrid_results
        
        # Dont call this anywhere else
        constants_immutable.all_flights, constants_immutable.pnr_objects, constants_immutable.pnr_flight_mapping, constants_immutable.pnr_to_s2 = Get_All_Maps()

        init_normalize_factors()
        
        # Identify the impacted PNRs
        from timings import timings_dict
        Impacted_PNR = Get_Impacted_passengers(constants_immutable.all_flights, constants_immutable.pnr_objects)


        print("Total impacted Passengers: ",len(Impacted_PNR))
        total_impacted = len(Impacted_PNR)
        # pp.pprint(Impacted_PNR)
        timings_dict["Impacted_PNR"] = total_impacted
        # #Classical part
        # start = time.time()
        # result = optimize_flight_assignments(Impacted_PNR,False)
        # end = time.time()
        # print("Total Classical Time:" , end-start)
        # print()
        # # print("Total Reassigned: ",len(result['Assignments']))
        # #print("Classical Optimal Cost",result['Total Cost'])
        # # pp.pprint(result['Assignments'])
        # print("Not Assigned PNRs: ")
        # #pp.pprint(result['Non Assignments'])
        # #print("#"*100)
        # print()


    # Quantum Pipeline
        start = time.time()
        quantum_result =quantum_optimize_flight_assignments(Impacted_PNR,QSol_count=3)
        end = time.time()
        print("Total Quantum Time:", end-start)
        print()
        print("Total Reassigned: ",len(quantum_result[0]['Assignments']))
        print()

        for i in range(len(quantum_result)):
            hybrid_results.append([])
            pnr_score_assigned.append([])
            pnr_score_non_assigned.append([])
        
        # Network flow pipeline
        for i in range(len(quantum_result)):
            start=time.time()
            final_result = Cabin_to_Class(quantum_result[i]["Assignments"])

            # Statistics
            total_assigned.append(len(quantum_result[i]["Assignments"]))
            total_impacted_pax = GetTotalPAX(quantum_result[i]["Assignments"], 1)
            total_assigned_pax.append(total_impacted_pax)
            total_impacted_pax += GetTotalPAX(quantum_result[i]["Non Assignments"], 0)
            same_city_count.append(len((quantum_result[i]["Assignments"])))
            total_non_assigned.append(total_impacted-len(quantum_result[i]["Assignments"]))

            for pnr_flight_tuple in quantum_result[i]["Assignments"]:
                pnr_score_assigned[i].append(pnr_flight_tuple[0].get_pnr_score())
            
            json_final = AssignmentsToJSON(final_result)

            with open(f'result_quantum_{i}.json', 'w') as f:
                f.write(json_final)

            hybrid_results[i].append(f'result_quantum_{i}.json')
            end=time.time()

            print(f"Network Flow time - {i} :",end-start)
            print()

    
            # Delays
            temp1, temp2, temp3 = up_dn_arr_delay(json_final)
            upgrade_count.append(temp1)
            downgrade_count.append(temp2)
            mean_arrival_delay.append(temp3)

            temp1, temp2, temp3, temp4 = count_one_multi(json_final)
            one_one.append(temp1)
            one_multi.append(temp2)
            multi_one.append(temp3)
            multi_multi.append(temp4)
        

        # City Pairs Handling
        if constants_immutable.city_pairs_reqd:
            for i in range(len(quantum_result)):
                start=time.time()
                city_pairs_result = optimize_flight_assignments(quantum_result[i]['Non Assignments'],True)
                end=time.time()
                print(f"Exception Handling time - {i}: ",end-start)
                print()
                print("Total Assignments with different City-Pairs: ", len(city_pairs_result['Assignments']))

                ##Stats
                total_assigned[i]+=len(city_pairs_result['Assignments'])
                total_assigned_pax[i] += GetTotalPAX(city_pairs_result["Assignments"], 1)
                total_non_assigned[i]-=len(city_pairs_result['Assignments'])
                diff_city_count.append(len(city_pairs_result['Assignments']))
                for pnr_flight_tuple in city_pairs_result["Assignments"]:
                    pnr_score_assigned[i].append(pnr_flight_tuple[0].get_pnr_score())
                

                start=time.time()
                final_result = Cabin_to_Class(city_pairs_result["Assignments"])
                end=time.time()
                print("Network Flow time :",end-start)
                print()
                print("Final Assignments")
                json_final = AssignmentsToJSON(final_result)
                with open(f'exception_list_{i}.json', 'w') as f:
                    f.write(json_final)
                hybrid_results[i].append(f'exception_list_{i}.json')

                
                ##Stats

                temp1, temp2, temp3 = up_dn_arr_delay(json_final)
                upgrade_count[i]+=temp1
                downgrade_count[i]+=temp2
                mean_arrival_delay[i]+=temp3
                mean_arrival_delay[i]/=total_assigned[i]
                mean_arrival_delay[i] = round(mean_arrival_delay[i], 3)

                temp1, temp2, temp3, temp4 = count_one_multi(json_final)
                one_one[i]+=temp1
                one_one[i]=(one_one[i]*100)/total_assigned[i]
                one_multi[i]+=temp2
                one_multi[i]=(one_multi[i]*100)/total_assigned[i]
                multi_one[i]+=temp3
                multi_one[i]=(multi_one[i]*100)/total_assigned[i]
                multi_multi[i]+=temp4
                multi_multi[i]=(multi_multi[i]*100)/total_assigned[i]

                ##Stats
                
                
                final_non_assignments = set()  # Use a set to store unique pnr_number values

                for j in range(len(city_pairs_result['Non Assignments'])):
                    pnr_number = city_pairs_result['Non Assignments'][j].pnr_number
                    pnr_score_non_assigned[i].append(city_pairs_result['Non Assignments'][j].get_pnr_score())
                    
                    if "#" in pnr_number:
                        some_number = pnr_number.split("#")[0]
                    else:
                        some_number = pnr_number
                    
                    final_non_assignments.add(some_number)
            
                # Convert the set to a newline-separated string
                final_non_assignments_str = "\n".join(final_non_assignments)
                with open(f'non_assignments_{i}.json', 'w') as f:
                    f.write(final_non_assignments_str)
                hybrid_results[i].append(f'non_assignments_{i}.json')          

        else:
            for i in range(len(quantum_result)):

                mean_arrival_delay[i]/=total_assigned[i]
                mean_arrival_delay[i] = round(mean_arrival_delay[i], 3)
                one_one[i]=(one_one[i]*100)/total_assigned[i]
                one_multi[i]=(one_multi[i]*100)/total_assigned[i]
                multi_one[i]=(multi_one[i]*100)/total_assigned[i]
                multi_multi[i]=(multi_multi[i]*100)/total_assigned[i]

                diff_city_count.append(0)
                final_non_assignments = set()  # Use a set to store unique pnr_number values

                for j in range(len(quantum_result[i]['Non Assignments'])):
                    pnr_number = quantum_result[i]['Non Assignments'][j].pnr_number
                    pnr_score_non_assigned[i].append(quantum_result[i]['Non Assignments'][j].get_pnr_score())
                    
                    if "#" in pnr_number:
                        some_number = pnr_number.split("#")[0]
                    else:
                        some_number = pnr_number
                    
                    final_non_assignments.add(some_number)
            
                # Convert the set to a newline-separated string
                final_non_assignments_str = "\n".join(final_non_assignments)
                with open(f'non_assignments_{i}.json', 'w') as f:
                    f.write(final_non_assignments_str)
                hybrid_results[i].append(f'non_assignments_{i}.json')         

        timings_dict["Name"]=test_PNR_data_file


        #To print statistics on landing page
        csv_file_path = "timings_data.csv"

        # Check if the CSV file exists and write data
        file_exists = os.path.exists(csv_file_path)

        # Uncomment to print the timings
        # with open(csv_file_path, mode='a', newline='') as csv_file:
        #     fieldnames = timings_dict.keys()
        #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
        #     # If the file doesn't exist, write the header row
        #     if not file_exists:
        #         writer.writeheader()
            
        #     # Write the data
        #     writer.writerow(timings_dict)

        display_results(hybrid_results)

        #To write current statistics in a file 
        writeStatistics()


    
    #Title
    st.title("🧳 Passenger Reaccomodation and Business Rule Engine")
    st.write("This GUI allows you to modify scores for different business rules and customize your solution. Please proceed to the next three pages to do so.")
    st.write("Click the below button after you have made all required modifications")
    st.write()

    constants_immutable.city_pairs_reqd=st.toggle("Different City-Pairs",value=True)
    if st.button("Generate Solution Files"):
            # To clear out the json files
        with open('result_quantum_0.json', 'w') as file:
            json.dump({},file)

        with open('result_quantum_1.json', 'w') as file:
            json.dump({},file)

        with open('result_quantum_2.json', 'w') as file:
            json.dump({},file)

        with open('exception_list_0.json', 'w') as file:
            json.dump({},file)

        with open('exception_list_1.json', 'w') as file:
            json.dump({},file)

        with open('exception_list_2.json', 'w') as file:
            json.dump({},file)

        Main_function()
    st.write("Click the below button to send E-mails to all affected PNRs to notify them about their re-accomodation")
    _,_,col3,_,_=st.columns(5)
    with col3:
        if st.button("Send Email"):
            mailer.send_mail('result_quantum_0.json','result_quantum_1.json','result_quantum_2.json')


if __name__=="__main__":
    Landing_Page()

