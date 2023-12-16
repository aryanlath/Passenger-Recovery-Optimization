from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import smtplib
import constants_immutable
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
   
    # constants_immutable.all_flights,_,_,_ = Get_All_Maps()
    # Connect to the Gmail SMTP server
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(email,pwd)
    print('Connected to Gmail SMTP server of ', email)
    for passenger,pnr in enumerate(assigned_pnr_set):
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
                arrival_city = constants_immutable.all_flights[inventory_id].arrival_city
                departure_city = constants_immutable.all_flights[inventory_id].departure_city
                flight_number = constants_immutable.all_flights[inventory_id].flight_number
                departure_time = str(constants_immutable.all_flights[inventory_id].departure_time)
                arrival_time = str(constants_immutable.all_flights[inventory_id].arrival_time)
                
                cancelled_flight_string = cancelled_flight_string + 'Flight Number : ' + flight_number + '\n'
                # cancelled_flight_string += 'Inventory ID : ' + inventory_id + '\n' 
                cancelled_flight_string += 'Cabin : ' + cabin + '\n'
                cancelled_flight_string += 'Class : ' + pnr_class_string + '\n'
                cancelled_flight_string += 'Arrival Airport : ' + arrival_city + '\n'
                cancelled_flight_string += 'Departure Airport : ' + departure_city + '\n'
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
                arrival_city =constants_immutable.all_flights[inventory_id].arrival_city
                departure_city =constants_immutable.all_flights[inventory_id].departure_city
                flight_number = constants_immutable.all_flights[inventory_id].flight_number
                departure_time = str(constants_immutable.all_flights[inventory_id].departure_time)
                arrival_time = str(constants_immutable.all_flights[inventory_id].arrival_time)
                
                cancelled_flight_string = cancelled_flight_string + 'Flight Number : ' + flight_number + '\n'
                # cancelled_flight_string += 'Inventory ID : ' + inventory_id + '\n' 
                cancelled_flight_string += 'Cabin : ' + cabin + '\n'
                cancelled_flight_string += 'Class : ' + pnr_class_string + '\n'
                cancelled_flight_string += 'Arrival Airport : ' + arrival_city + '\n'
                cancelled_flight_string += 'Departure Airport : ' + departure_city + '\n'
                cancelled_flight_string += 'Arrival Time : ' + arrival_time + '\n'
                cancelled_flight_string += 'Departure Time : ' + departure_time
                cancelled_flight_string += '\n\n'
        else :
            for ind in schema3[pnr]['Cancelled']:
                x = schema3[pnr]['Original'][ind]
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class = x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city =constants_immutable.all_flights[inventory_id].arrival_city
                departure_city = constants_immutable.all_flights[inventory_id].departure_city
                flight_number = constants_immutable.all_flights[inventory_id].flight_number
                departure_time = str(constants_immutable.all_flights[inventory_id].departure_time)
                arrival_time = str(constants_immutable.all_flights[inventory_id].arrival_time)             
                
                cancelled_flight_string = cancelled_flight_string + 'Flight Number : ' + flight_number + '\n'
                # cancelled_flight_string += 'Inventory ID : ' + inventory_id + '\n' 
                cancelled_flight_string += 'Cabin : ' + cabin + '\n'
                cancelled_flight_string += 'Class : ' + pnr_class_string + '\n'
                cancelled_flight_string += 'Arrival Airport : ' + arrival_city + '\n'
                cancelled_flight_string += 'Departure Airport : ' + departure_city + '\n'
                cancelled_flight_string += 'Arrival Time : ' + arrival_time + '\n'
                cancelled_flight_string += 'Departure Time : ' + departure_time
                cancelled_flight_string += '\n\n'
                                                                
        
        
        
        
        alt_flight0_string = ''
        if pnr in schema1:
            alt_flight0_string = alt_flight0_string + 'Alternate Flight Choice \n'
            for x in schema1[pnr]['Proposed']:
                inventory_id = str(x[0])
                cabin = str(x[1])
                pnr_class = x[2]
                pnr_class_string = ', '.join(pnr_class)
                arrival_city = constants_immutable.all_flights[inventory_id].arrival_city
                departure_city =constants_immutable.all_flights[inventory_id].departure_city
                flight_number =constants_immutable.all_flights[inventory_id].flight_number
                departure_time = str(constants_immutable.all_flights[inventory_id].departure_time)
                arrival_time = str(constants_immutable.all_flights[inventory_id].arrival_time)
                
                
                #alt_flight0_string = alt_flight0_string + 'Inventory ID : ' + inventory_id + '\n' 
                
                alt_flight0_string += 'Flight Number : ' + str(flight_number) + '\n'
                alt_flight0_string += 'Cabin : ' + cabin + '\n'
                alt_flight0_string += 'Class : ' + pnr_class_string + '\n'
                alt_flight0_string += 'Arrival City : ' + arrival_city + '\n'
                alt_flight0_string += 'Departure City : ' + departure_city + '\n'
                # alt_flight0_string += 'Flight Number : ' + str(flight_number) + '\n'
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
                arrival_city = constants_immutable.all_flights[inventory_id].arrival_city
                departure_city = constants_immutable.all_flights[inventory_id].departure_city
                flight_number = constants_immutable.all_flights[inventory_id].flight_number
                departure_time = str(constants_immutable.all_flights[inventory_id].departure_time)
                arrival_time = str(constants_immutable.all_flights[inventory_id].arrival_time)
                
                alt_flight1_string += 'Flight Number : ' + str(flight_number) + '\n' 
                alt_flight1_string += 'Cabin : ' + cabin + '\n'
                alt_flight1_string += 'Class : ' + pnr_class_string + '\n'
                alt_flight1_string += 'Arrival City : ' + arrival_city + '\n'
                alt_flight1_string += 'Departure City : ' + departure_city + '\n'
                # alt_flight1_string += 'Flight Number : ' + str(flight_number) + '\n'
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
                arrival_city = constants_immutable.all_flights[inventory_id].arrival_city
                departure_city = constants_immutable.all_flights[inventory_id].departure_city
                flight_number = constants_immutable.all_flights[inventory_id].flight_number
                departure_time = str(constants_immutable.all_flights[inventory_id].departure_time)
                arrival_time = str(constants_immutable.all_flights[inventory_id].arrival_time)
                
                alt_flight2_string += 'Flight Number : ' + str(flight_number) + '\n'
                alt_flight2_string += 'Cabin : ' + cabin + '\n'
                alt_flight2_string += 'Class : ' + pnr_class_string + '\n'
                alt_flight2_string += 'Arrival City : ' + arrival_city + '\n'
                alt_flight2_string += 'Departure City : ' + departure_city + '\n'
                # alt_flight2_string += 'Flight Number : ' + str(flight_number) + '\n'
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
        if passenger==5:
            break
        time.sleep(2)

    server.quit()