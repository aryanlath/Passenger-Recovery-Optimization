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

    print("Do you want to send emails to the passengers whose flight has been cancelled? (y/n)")
    choice = input()
    if choice == 'n':
        return
    
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
            for x in schema1[pnr]['Original']:
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class = x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city = all_flights(inventory_id).arrival_city
                departure_city = all_flights(inventory_id).departure_city
                flight_number = all_flights(inventory_id).flight_number
                
                cancelled_flight_string = cancelled_flight_string +  'Inventory ID : ' + inventory_id + '\n' 
                cancelled_flight_string += 'Cabin : ' + cabin + '\n'
                cancelled_flight_string += 'Classes : ' + pnr_class_string + '\n'
                cancelled_flight_string += 'Arrival City : ' + arrival_city + '\n'
                cancelled_flight_string += 'Departure City : ' + departure_city + '\n'
                cancelled_flight_string += 'Flight Number : ' + flight_number + '\n'
                cancelled_flight_string += '\n\n'
        elif index == 2:
            for x in schema2[pnr]['Original']:
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class =x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city =all_flights(inventory_id).arrival_city
                departure_city =all_flights(inventory_id).departure_city
                flight_number = all_flights(inventory_id).flight_number
                
                cancelled_flight_string  = cancelled_flight_string + 'Inventory ID : ' + inventory_id + '\n' 
                cancelled_flight_string += 'Cabin : ' + cabin + '\n'
                cancelled_flight_string += 'Classes : ' + pnr_class_string + '\n'
                cancelled_flight_string += 'Arrival City : ' + arrival_city + '\n'
                cancelled_flight_string += 'Departure City : ' + departure_city + '\n'
                cancelled_flight_string += 'Flight Number : ' + flight_number + '\n'
                cancelled_flight_string += '\n' + '\n'
        else :
            for x in schema3[pnr]['Original']:
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class = x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city =all_flights(inventory_id).arrival_city
                departure_city = all_flights(inventory_id).departure_city
                flight_number = all_flights(inventory_id).flight_number
                
                cancelled_flight_string =  cancelled_flight_string +  'Inventory ID : ' + inventory_id + '\n' 
                cancelled_flight_string += 'Cabin : ' + cabin + '\n'
                cancelled_flight_string += 'Classes : ' + pnr_class_string + '\n'
                cancelled_flight_string += 'Arrival City : ' + arrival_city + '\n'
                cancelled_flight_string += 'Departure City : ' + departure_city + '\n'
                cancelled_flight_string += 'Flight Number : ' + str(flight_number)
                                                                
        
        
        
        
        alt_flight0_string = ''
        if pnr in schema1:
            alt_flight0_string = alt_flight0_string + 'Alternate Flight Choice \n'
            for x in schema1[pnr]['Proposed']:
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class = x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city = all_flights(inventory_id).arrival_city
                departure_city =all_flights(inventory_id).departure_city
                flight_number =all_flights(inventory_id).flight_number
                
                alt_flight0_string = alt_flight0_string + 'Inventory ID : ' + inventory_id + '\n' 
                alt_flight0_string += 'Cabin : ' + cabin + '\n'
                alt_flight0_string += 'Classes : ' + pnr_class_string + '\n'
                alt_flight0_string += 'Arrival City : ' + arrival_city + '\n'
                alt_flight0_string += 'Departure City : ' + departure_city + '\n'
                alt_flight0_string += 'Flight Number : ' + str(flight_number) + '\n'
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
                arrival_city = all_flights(inventory_id).arrival_city
                departure_city = all_flights(inventory_id).departure_city
                flight_number = all_flights(inventory_id).flight_number
                
                alt_flight1_string = alt_flight1_string + 'Inventory ID : ' + inventory_id + '\n' 
                alt_flight1_string += 'Cabin : ' + cabin + '\n'
                alt_flight1_string += 'Classes : ' + pnr_class_string + '\n'
                alt_flight1_string += 'Arrival City : ' + arrival_city + '\n'
                alt_flight1_string += 'Departure City : ' + departure_city + '\n'
                alt_flight1_string += 'Flight Number : ' + str(flight_number) + '\n'
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
                arrival_city = all_flights(inventory_id).arrival_city
                departure_city = all_flights(inventory_id).departure_city
                flight_number = all_flights(inventory_id).flight_number
                
                alt_flight2_string = alt_flight2_string + 'Inventory ID : ' + inventory_id + '\n' 
                alt_flight2_string += 'Cabin : ' + cabin + '\n'
                alt_flight2_string += 'Classes : ' + pnr_class_string + '\n'
                alt_flight2_string += 'Arrival City : ' + arrival_city + '\n'
                alt_flight2_string += 'Departure City : ' + departure_city + '\n'
                alt_flight2_string += 'Flight Number : ' + str(flight_number) + '\n'
                alt_flight2_string += '\n'   
            alt_flight2_string += 'Please click the link given below to choose this flight -\n'
            alt_flight2_string += schema_2_link 

            
            
        
        
        msg = message_template.substitute(PNR_Number=pnr,
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
        email_message['Subject'] = f"Flight Cancellation - {pnr}"

        # Attach the message template defined earlier, as a MIMEText html content type to the MIME message
        email_message.attach(MIMEText(msg, "plain"))
        email_string = email_message.as_string()

        server.sendmail(email, email_pnr, email_string)

        print("Mail sent to ",email_pnr)
        time.sleep(2)

    server.quit()
    


#send_mail('result1.json','result2.json','result3.json')








