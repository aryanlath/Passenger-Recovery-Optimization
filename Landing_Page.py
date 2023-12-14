##MAIN FUNCTION CODE

import streamlit as st
from feasible_flights import *
from constants import *
from init_functions import *
from gurobi_optimisation import *
from Leap_Quantum_Main import *
import pprint
import constants_immutable
pp = pprint.PrettyPrinter(indent=4)
from Assign_Class import *
import json
from utils import *


## Global variables(Statistics)

total_impacted = 0
total_assigned = []
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
    f.close()


#to display result
def display_results(hybrid_results):
    #display json in streamlit

    if (len(hybrid_results)==2):
        col1,col2=st.columns(2)
        with col1:
            #first solution
            st.write("Solution 1")
            st.write("Total impacted PNRs are :",total_impacted)
            st.write("Reaccommodated PNRs :",total_assigned[0])
            st.write("Unaccomadated PNRs :",total_non_assigned[0])
            st.write("PNRs Upgraded :",upgrade_count[0])
            st.write("PNRs Downgraded :",downgrade_count[0])
            st.write("PNRs with city pairs same :",same_city_count[0])
            st.write("PNRs with city pairs different :",diff_city_count[0])
            st.write("Mean Arrival Delay(in Hours) :",mean_arrival_delay[0])
            st.write("Multi-Multi(%) :",multi_multi[0])
            file=open(hybrid_results[0][0],'r')
            jsonfile=json.load(file)
            st.json(jsonfile,expanded=False)
        with col2:
            #second solution
            st.write("Solution 2")
            st.write("Total impacted PNRs are :",total_impacted)
            st.write("Reaccommodated PNRs :",total_assigned[1])
            st.write("Unaccomadated PNRs :",total_non_assigned[1])
            st.write("PNRs Upgraded :",upgrade_count[1])
            st.write("PNRs Downgraded :",downgrade_count[1])
            st.write("PNRs with city pairs same :",same_city_count[1])
            st.write("PNRs with city pairs different :",diff_city_count[1])
            st.write("Mean Arrival Delay(in Hours) :",mean_arrival_delay[1])
            st.write("Multi-Multi(%) :",multi_multi[1])
            file=open(hybrid_results[1][0],'r')
            jsonfile=json.load(file)
            st.json(jsonfile,expanded=False)
    else:
        col1,col2,col3=st.columns(3)
        with col1:
            #first solution
            st.write("Solution 1")
            st.write("Total impacted PNRs are :",total_impacted)
            st.write("Reaccommodated PNRs :",total_assigned[0])
            st.write("Unaccomadated PNRs :",total_non_assigned[0])
            st.write("PNRs Upgraded :",upgrade_count[0])
            st.write("PNRs Downgraded :",downgrade_count[0])
            st.write("PNRs with city pairs same :",same_city_count[0])
            st.write("PNRs with city pairs different :",diff_city_count[0])
            st.write("Mean Arrival Delay(in Hours) :",mean_arrival_delay[0])
            st.write("One-One(%) :",one_one[0])
            st.write("One-Multi(%) :",one_multi[0])
            st.write("Multi-One(%) :",multi_one[0])
            st.write("Multi-Multi(%) :",multi_multi[0])
            file=open(hybrid_results[0][0],'r')
            jsonfile=json.load(file)
            st.json(jsonfile,expanded=False)
        with col2:
            #second solution
            st.write("Solution 2")
            st.write("Total impacted PNRs are :",total_impacted)
            st.write("Reaccommodated PNRs :",total_assigned[1])
            st.write("Unaccomadated PNRs :",total_non_assigned[0])
            st.write("PNRs Upgraded :",upgrade_count[1])
            st.write("PNRs Downgraded :",downgrade_count[1])
            st.write("PNRs with city pairs same :",same_city_count[1])
            st.write("PNRs with city pairs different :",diff_city_count[1])
            st.write("Mean Arrival Delay(in Hours) :",mean_arrival_delay[1])
            st.write("One-One(%) :",one_one[1])
            st.write("One-Multi(%) :",one_multi[1])
            st.write("Multi-One(%) :",multi_one[1])
            st.write("Multi-Multi(%) :",multi_multi[1])
            file=open(hybrid_results[1][0],'r')
            jsonfile=json.load(file)
            st.json(jsonfile,expanded=False)
        with col3:    
            #third solution
            st.write("Solution 3")
            st.write("Total impacted PNRs are :",total_impacted)
            st.write("Reaccommodated PNRs :",total_assigned[2])
            st.write("Unaccomadated PNRs :",total_non_assigned[2])
            st.write("PNRs Upgraded :",upgrade_count[2])
            st.write("PNRs Downgraded :",downgrade_count[2])
            st.write("PNRs with city pairs same :",same_city_count[2])
            st.write("PNRs with city pairs different :",diff_city_count[2])
            st.write("Mean Arrival Delay(in Hours) :",mean_arrival_delay[2])
            st.write("One-One(%) :",one_one[2])
            st.write("One-Multi(%) :",one_multi[2])
            st.write("Multi-One(%) :",multi_one[2])
            st.write("Multi-Multi(%) :",multi_multi[2])
            file=open(hybrid_results[2][0],'r')
            jsonfile=json.load(file)
            st.json(jsonfile,expanded=False)


def Main_function():

    #refer to global variable
    global total_impacted
    global total_assigned
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
    
    #store names of files containing results
    hybrid_results = []
    
    
    
    # initializes the loyalty scores for the passengers
    # init_loyalty_dictionary()

    # global all_flights, pnr_objects,  pnr_flight_mapping, pnr_to_s2
    constants_immutable.all_flights, constants_immutable.pnr_objects, constants_immutable.pnr_flight_mapping, constants_immutable.pnr_to_s2 = Get_All_Maps()
    # finds the normalization factors for the cost function
    init_normalize_factors()
    


    # Identify the impacted PNRs
    Impacted_PNR = Get_Impacted_passengers(constants_immutable.all_flights, constants_immutable.pnr_objects)


    print("Total impacted Passengers: ",len(Impacted_PNR))
    total_impacted = len(Impacted_PNR)
    pp.pprint(Impacted_PNR)

    # Classical part
    start = time.time()
    result = optimize_flight_assignments(Impacted_PNR,False)
    end = time.time()
    print("Total Classical Time:" , end-start)
    print()
    print("Total Reassigned: ",len(result['Assignments']))
    print("Classical Optimal Cost",result['Total Cost'])
    # pp.pprint(result['Assignments'])
    print("Not Assigned PNRs: ")
    pp.pprint(result['Non Assignments'])
    print("#"*100)
    print()
    with open('result_classical.json', 'w') as f:
        f.write(AssignmentsToJSON(Cabin_to_Class(result['Assignments'])))
    #total_assigned.append(len(result['Assignments']))
    #hybrid_results.append('result_classical.json')
    #same_city_count.append(result['Assignments'])
    # print(AssignmentsToJSON(Cabin_to_Class(result["Assignments"])))
   # Quantum Pipeline
    start = time.time()
    quantum_result =quantum_optimize_flight_assignments(Impacted_PNR,QSol_count=4)
    end = time.time()
    print("Total Quantum Time:", end-start)
    print()
    print("Total Reassigned: ",len(quantum_result[0]['Assignments']))
    pp.pprint(quantum_result[0]['Assignments'])
    print("Not Assigned PNRs: ")
    pp.pprint(quantum_result[0]['Non Assignments'])
    print("#"*100)
    print()

    for i in range(len(quantum_result)):
        hybrid_results.append([])
        
    
    # Network flow pipeline
    for i in range(len(quantum_result)):
        start=time.time()
        final_result = Cabin_to_Class(quantum_result[i]["Assignments"])

        ##Stats
        total_assigned.append(len(quantum_result[i]["Assignments"]))
        same_city_count.append(len((quantum_result[i]["Assignments"])))
        total_non_assigned.append(total_impacted-len(quantum_result[i]["Assignments"]))
        ##Stats
        
        # print(final_result)
        json_final = AssignmentsToJSON(final_result)

        with open(f'result_quantum_{i}.json', 'w') as f:
            f.write(json_final)
        hybrid_results[i].append(f'result_quantum_{i}.json')
        end=time.time()
        print("Network Flow time :",end-start)
        print()
    # pp.pprint(final_result)
        print("#"*100)
        print()

        ##Stats

        temp1, temp2, temp3 = up_dn_arr_delay(json_final)
        upgrade_count.append(temp1)
        downgrade_count.append(temp2)
        mean_arrival_delay.append(temp3)

        temp1, temp2, temp3, temp4 = count_one_multi(json_final)
        one_one.append(temp1)
        one_multi.append(temp2)
        multi_one.append(temp3)
        multi_multi.append(temp4)
        ##Stats
       

    # Exception List Handling
    for i in range(len(quantum_result)):
        start=time.time()
        city_pairs_result = optimize_flight_assignments(quantum_result[i]['Non Assignments'],True)
        end=time.time()
        print("Exception Handling time: ",end-start)
        print()
        print("Total Assignments with different City-Pairs: ", len(city_pairs_result['Assignments']))

        ##Stats
        total_assigned[i]+=len(city_pairs_result['Assignments'])
        total_non_assigned[i]-=len(city_pairs_result['Assignments'])
        diff_city_count.append(len(city_pairs_result['Assignments']))
        ##Stats

        # pp.pprint(city_pairs_result['Assignments'])
        print("Not Assigned PNRs: ")
        # pp.pprint(city_pairs_result['Non Assignments'])
        print("#"*100)
        print()

        start=time.time()
        final_result = Cabin_to_Class(city_pairs_result["Assignments"])
        end=time.time()
        print("Network Flow time :",end-start)
        print()
        print("Final Assignments")
        # pp.pprint(final_result)
        json_final = AssignmentsToJSON(final_result)
        with open(f'exception_list_{i}.json', 'w') as f:
            f.write(json_final)
        hybrid_results[i].append(f'exception_list_{i}.json')
        print("#"*100)
        print()
        
        ##Stats

        temp1, temp2, temp3 = up_dn_arr_delay(json_final)
        upgrade_count[i]+=temp1
        downgrade_count[i]+=temp2
        mean_arrival_delay[i]+=temp3
        mean_arrival_delay[i]/=total_impacted
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
        
        

        print("Final Non Assignments")
        print(city_pairs_result['Non Assignments'])
    
    
    final_non_assignments = set()  # Use a set to store unique pnr_number values

    for j in range(len(city_pairs_result['Non Assignments'])):
        pnr_number = city_pairs_result['Non Assignments'][j].pnr_number
        
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

    global code_been_run
    code_been_run=1
    #print(hybrid_results)
    #To print statistics on landing page
    display_results(hybrid_results)

    #To write current statistics in a file 
    writeStatistics();


    
    # Network flow pipeline
    # start=time.time()
    # final_result = Cabin_to_Class(city_pairs_result["Assignments"])
    # end=time.time()
    # print("Network Flow time :",end-start)
    # print()
    # print("Final Assignments")
    # pp.pprint(final_result)
    # print("#"*100)
    # print()

    # TODO: Integrate email sending and mockup simulation of choosing of a scheme

    # send emails
    # send_mail("Results/assignments.csv")


##MAILER CODE

# mail the PNRs from assignments.csv to the respective passengers
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
import time
from string import Template
from feasible_flights import Get_All_Maps
from dotenv import load_dotenv
import os
import json

load_dotenv()

def read_template(filename):

    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

# create a function for sending emails
def send_mail(assignment_0,assignment_1,assignment_2):
    '''
    This function sends an email to the passengers whose flight has been cancelled.
    '''
    # Define the content of the email
    Airlines_Name = "Mock Airlines"
    email = os.getenv('flight_mail')
    pwd = os.getenv('flight_mail_password')
    
    schema_0_link = 'https://forms.gle/8wZmJ5e9szYm37r48'
    schema_1_link = 'https://forms.gle/q3QrqN8fSHPnkRcq6'
    schema_2_link = 'https://forms.gle/bAot7r4sMkporCvt9'
    cancellation_link = 'https://forms.gle/1c94gcb9sMeDU4v96'
    


    # Read the JSON file
    with open(assignment_0, 'r') as file:
        schema1 = json.load(file)
        

    with open(assignment_1, 'r') as file:
        schema2 = json.load(file)
        


    with open(assignment_2, 'r') as file:
        schema3 = json.load(file)




    # Read the template txt file
    message_template = read_template('message.txt')


    
        
    assigned_pnr_set = set()
    for pnr in schema1:
        assigned_pnr_set.add(pnr)
    for pnr in schema2:
        assigned_pnr_set.add(pnr)
    for pnr in schema3:
        assigned_pnr_set.add(pnr)
   
    all_flights,_,_,_ = Get_All_Maps()
    # Connect to the Gmail SMTP server
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(email,pwd)
    print('Connected to Gmail SMTP server of ', email)
    for pnr in assigned_pnr_set:
        index = -1
        if pnr in schema1:
            email_pnr = schema1[pnr]['Email']
            index = 1
        if pnr in schema2:
            email_pnr = schema2[pnr]['Email']
            index = 2
        if pnr in schema3:
            email_pnr = schema3[pnr]['Email']
            index = 3

        
 
        
        cancelled_flight_string = 'Cancelled Flight Details - \n'
        if index == 1:
            for ind in schema1[pnr]['Cancelled']:
                x = schema1[pnr]['Original'][ind]
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class = x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city = all_flights[inventory_id].arrival_city
                departure_city = all_flights[inventory_id].departure_city
                flight_number = all_flights[inventory_id].flight_number
                departure_time = str(all_flights[inventory_id].departure_time)
                arrival_time = str(all_flights[inventory_id].arrival_time)
                
                cancelled_flight_string = cancelled_flight_string +  'Inventory ID : ' + inventory_id + '\n' 
                cancelled_flight_string += 'Cabin : ' + cabin + '\n'
                cancelled_flight_string += 'Class : ' + pnr_class_string + '\n'
                cancelled_flight_string += 'Arrival City : ' + arrival_city + '\n'
                cancelled_flight_string += 'Departure City : ' + departure_city + '\n'
                cancelled_flight_string += 'Flight Number : ' + flight_number + '\n'
                cancelled_flight_string += 'Arrival Time : ' + arrival_time + '\n'
                cancelled_flight_string += 'Departure Time : ' + departure_time
                cancelled_flight_string += '\n\n'
        elif index == 2:
            for ind in schema2[pnr]['Cancelled']:
                x = schema2[pnr]['Original'][ind]
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class =x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city =all_flights[inventory_id].arrival_city
                departure_city =all_flights[inventory_id].departure_city
                flight_number = all_flights[inventory_id].flight_number
                departure_time = str(all_flights[inventory_id].departure_time)
                arrival_time = str(all_flights[inventory_id].arrival_time)
                
                cancelled_flight_string  = cancelled_flight_string + 'Inventory ID : ' + inventory_id + '\n' 
                cancelled_flight_string += 'Cabin : ' + cabin + '\n'
                cancelled_flight_string += 'Class : ' + pnr_class_string + '\n'
                cancelled_flight_string += 'Arrival City : ' + arrival_city + '\n'
                cancelled_flight_string += 'Departure City : ' + departure_city + '\n'
                cancelled_flight_string += 'Flight Number : ' + flight_number + '\n'
                cancelled_flight_string += 'Arrival Time : ' + arrival_time + '\n'
                cancelled_flight_string += 'Departure Time : ' + departure_time
                cancelled_flight_string += '\n' + '\n'
        else :
            for ind in schema3[pnr]['Cancelled']:
                x = schema3[pnr]['Original'][ind]
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class = x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city =all_flights[inventory_id].arrival_city
                departure_city = all_flights[inventory_id].departure_city
                flight_number = all_flights[inventory_id].flight_number
                departure_time = str(all_flights[inventory_id].departure_time)
                arrival_time = str(all_flights[inventory_id].arrival_time)             
                cancelled_flight_string =  cancelled_flight_string +  'Inventory ID : ' + inventory_id + '\n' 
                cancelled_flight_string += 'Cabin : ' + cabin + '\n'
                cancelled_flight_string += 'Class : ' + pnr_class_string + '\n'
                cancelled_flight_string += 'Arrival City : ' + arrival_city + '\n'
                cancelled_flight_string += 'Departure City : ' + departure_city + '\n'
                cancelled_flight_string += 'Flight Number : ' + str(flight_number) + '\n'
                cancelled_flight_string += 'Arrival Time : ' + arrival_time + '\n'
                cancelled_flight_string += 'Departure Time : ' + departure_time
                cancelled_flight_string += '\n' + '\n'
                                                                
        
        
        
        
        alt_flight0_string = ''
        if pnr in schema1:
            alt_flight0_string = alt_flight0_string + 'Alternate Flight Choice \n'
            for x in schema1[pnr]['Proposed']:
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class = x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city = all_flights[inventory_id].arrival_city
                departure_city =all_flights[inventory_id].departure_city
                flight_number =all_flights[inventory_id].flight_number
                departure_time = str(all_flights[inventory_id].departure_time)
                arrival_time = str(all_flights[inventory_id].arrival_time)
                
                
                alt_flight0_string = alt_flight0_string + 'Inventory ID : ' + inventory_id + '\n' 
                alt_flight0_string += 'Cabin : ' + cabin + '\n'
                alt_flight0_string += 'Class : ' + pnr_class_string + '\n'
                alt_flight0_string += 'Arrival City : ' + arrival_city + '\n'
                alt_flight0_string += 'Departure City : ' + departure_city + '\n'
                alt_flight0_string += 'Flight Number : ' + str(flight_number) + '\n'
                alt_flight0_string += 'Arrival Time : ' + arrival_time + '\n'
                alt_flight0_string += 'Departure Time : ' + departure_time + '\n'
                alt_flight0_string += '\n'   
            alt_flight0_string += 'Please click the link given below to choose this flight -\n'
            alt_flight0_string += schema_0_link 


                                       
                
                
        alt_flight1_string = ''
        if pnr in schema2:
            alt_flight1_string = alt_flight1_string + 'Alternate Flight Choice \n'
            for x in schema2[pnr]['Proposed']:
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class = x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city = all_flights[inventory_id].arrival_city
                departure_city = all_flights[inventory_id].departure_city
                flight_number = all_flights[inventory_id].flight_number
                departure_time = str(all_flights[inventory_id].departure_time)
                arrival_time = str(all_flights[inventory_id].arrival_time)
                
                alt_flight1_string = alt_flight1_string + 'Inventory ID : ' + inventory_id + '\n' 
                alt_flight1_string += 'Cabin : ' + cabin + '\n'
                alt_flight1_string += 'Class : ' + pnr_class_string + '\n'
                alt_flight1_string += 'Arrival City : ' + arrival_city + '\n'
                alt_flight1_string += 'Departure City : ' + departure_city + '\n'
                alt_flight1_string += 'Flight Number : ' + str(flight_number) + '\n'
                alt_flight1_string += 'Arrival Time : ' + arrival_time + '\n'
                alt_flight1_string += 'Departure Time : ' + departure_time + '\n'
                alt_flight1_string += '\n'   
            alt_flight1_string += 'Please click the link given below to choose this flight -\n'
            alt_flight1_string += schema_1_link 

        
        
        alt_flight2_string = ''
        if pnr in schema3:
            alt_flight2_string = alt_flight2_string + 'Alternate Flight Choice \n'
            for x in schema3[pnr]['Proposed']:
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class = x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city = all_flights[inventory_id].arrival_city
                departure_city = all_flights[inventory_id].departure_city
                flight_number = all_flights[inventory_id].flight_number
                departure_time = str(all_flights[inventory_id].departure_time)
                arrival_time = str(all_flights[inventory_id].arrival_time)
                
                alt_flight2_string = alt_flight2_string + 'Inventory ID : ' + inventory_id + '\n' 
                alt_flight2_string += 'Cabin : ' + cabin + '\n'
                alt_flight2_string += 'Class : ' + pnr_class_string + '\n'
                alt_flight2_string += 'Arrival City : ' + arrival_city + '\n'
                alt_flight2_string += 'Departure City : ' + departure_city + '\n'
                alt_flight2_string += 'Flight Number : ' + str(flight_number) + '\n'
                alt_flight2_string += 'Arrival Time : ' + arrival_time + '\n'
                alt_flight2_string += 'Departure Time : ' + departure_time + '\n'
                alt_flight2_string += '\n'   
            alt_flight2_string += 'Please click the link given below to choose this flight -\n'
            alt_flight2_string += schema_2_link 

            
            
        
        pnr_string = pnr
        cancelled_flight_string = cancelled_flight_string.replace('\n', '<br>')
        alt_flight0_string = alt_flight0_string.replace('\n','<br>')
        alt_flight1_string = alt_flight1_string.replace('\n','<br>')
        alt_flight2_string = alt_flight2_string.replace('\n','<br>')

        msg = message_template.substitute(PNR_Number=pnr_string,
                                          Airlines_Name=Airlines_Name,
                                          Cancelled_Flight = cancelled_flight_string,
                                          Cancellation_link =cancellation_link,
                                          Schema_0 = alt_flight0_string,
                                          Schema_1 = alt_flight1_string,
                                          Schema_2 = alt_flight2_string
                                          
                                          )

        email_message = MIMEMultipart()
        email_message['From'] = Airlines_Name
        email_message['To'] = email_pnr
        email_message['Subject'] = f"Alternate Flight Options - {pnr_string}"

        # Attach the message template defined earlier, as a MIMEText html content type to the MIME message
        email_message.attach(MIMEText(msg, "html"))
        email_string = email_message.as_string()

        server.sendmail(email, email_pnr, email_string)

        print("Mail sent to ",email_pnr)
        time.sleep(2)

    server.quit()
    

#heading

st.title("Business Rules Modification Engine")
st.write("This GUI allows you to modify scores for different business rules and customize your solution. Please proceed to the next three pages to do so.")
st.write("Click the below button after you have made all required modifications")
st.write()



#To see if code has been run
code_been_run=0


# col1,col2,col3,col4,col5=st.columns(5)
# with col3:
if st.button("Run Code"):
    Main_function()
st.write("Click the below button to send E-mails to all affected passengers to notify them about their re-accomadation")
col1,col2,col3,col4,col5=st.columns(5)
with col3:
    if st.button("Send Email"):
        send_mail('result_quantum_0.json','result_quantum_1.json','result_quantum_2.json')

            