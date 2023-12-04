# mail the PNRs from assignments.csv to the respective passengers

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import pandas as pd
import smtplib
import time
from string import Template
from collections import defaultdict
from feasible_flights import Get_All_Maps
from dotenv import load_dotenv
import os

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

    # Read the template txt file
    message_template = read_template('message.txt')

    # Read the csv file
    pd_assignment_0 = pd.read_csv(assignment_0)
    pd_assignment_1 = pd.read_csv(assignment_1)
    pd_assignment_2 = pd.read_csv(assignment_2)
    
    assignment_0_dict = defaultdict(list)
    assignment_1_dict = defaultdict(list)
    assignment_2_dict = defaultdict(list)

    for _,row in pd_assignment_0.iterrows():
        assignment_list = [row['PNR_Email'],row['Flight'],row['Cabin'],row['Class'],row['Cancelled Flights']]
        assignment_0_dict[row['PNR_Number']] = assignment_list 
    
    for _,row in pd_assignment_1.iterrows():
        assignment_list = [row['PNR_Email'],row['Flight'],row['Cabin'],row['Class'],row['Cancelled Flights']]
        assignment_1_dict[row['PNR_Number']] = assignment_list 
        
    for _,row in pd_assignment_2.iterrows():
        assignment_list = [row['PNR_Email'],row['Flight'],row['Cabin'],row['Class'],row['Cancelled Flights']]
        assignment_2_dict[row['PNR_Number']] = assignment_list 
        
        
    assigned_pnr_set = set()
    assigned_pnr_set.update(list(assignment_0_dict.keys()))
    assigned_pnr_set.update(list(assignment_1_dict.keys()))
    assigned_pnr_set.update(list(assignment_2_dict.keys()))
    all_flights,_,_,_ = Get_All_Maps()
    # Connect to the Gmail SMTP server
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(email,pwd)
    print('Connected to Gmail SMTP server of ', email)
    for pnr in assigned_pnr_set:
    #     msg = """
    # <html>
    # <body>
    # <div>

    # <p>Dear Sir/Ma'am,</p>
    # <p>Thank you for choosing """+name+""".</p>
    # <br>
    # <p>Unfortunately, your flight has been cancelled, please find alternate flight details below.</p>
    # <br>
    # <p>Flight Details:</p>
    # <p>Your PNR is """+data['PNR_Number'][i]+""".</p>
    # <p>Your rescheduled flight is \n"""+data['Flight'][i]+""".</p>
    # <p>Your cabin is """+data['Cabin'][i]+""".</p>
    # <br>
    # <p>Have a safe journey.</p>
    # <br>
    # <p>Regards,</p>
    # <p>"""+name+"""</p>

    # </div>
    # </body>
    # </html>
    #     """.format(data['PNR_Number'][i],data['Flight'][i],data['Cabin'][i],name)

        # Add in the actual person name to the message template
        
        if len(assignment_0_dict[pnr]) != 0:
            email_pnr = assignment_0_dict[pnr][0]
        if len(assignment_1_dict[pnr]) != 0:
            email_pnr = assignment_1_dict[pnr][0]
        if len(assignment_2_dict[pnr]) != 0:
            email_pnr = assignment_2_dict[pnr][0]
        
        cancelled_flight_string = 'Cancelled Flight Details - \n'
        if assignment_0_dict[pnr]:
            temp_var = (assignment_0_dict[pnr][4].split(','))
        if assignment_1_dict[pnr]:
            temp_var = (assignment_1_dict[pnr][4].split(','))
        if assignment_2_dict[pnr]:
            temp_var = (assignment_2_dict[pnr][4].split(','))
        inventory_id = temp_var[0].split(':')[1].strip()
        flight_number = all_flights[inventory_id].flight_number
        cancelled_flight_string += temp_var[0][9:] + '\n' + temp_var[1].strip() + '\n' + temp_var[2].strip()[:-1] +'\n'
        cancelled_flight_string += 'Flight Number: ' + str(flight_number) + '\n'
        alt_flight0_string = ''
        if assignment_0_dict[pnr]:
            assignment_list = assignment_0_dict[pnr]
            temp_var = assignment_list[1].split(',')
            inventory_id = temp_var[0][8:].split(':')[1].strip()
            flight_number = all_flights[inventory_id].flight_number
            alt_flight0_string += 'Alternate Flight Choice - \n'
            alt_flight0_string += (temp_var[0][8:] + '\n'+  temp_var[1].strip() + '\n' + temp_var[2].strip() + '\n')
            alt_flight0_string += 'Flight Number: ' + str(flight_number) + '\n'
            alt_flight0_string += ('Cabin : ' + assignment_list[2] + '\n' )
            alt_flight0_string += ('Class : ' + assignment_list[3] + '\n' )
            alt_flight0_string += 'Please click the link given below to choose this flight -\n'
            alt_flight0_string += schema_0_link
            
            
        alt_flight1_string = ''
        if assignment_1_dict[pnr]:
            assignment_list = assignment_1_dict[pnr]
            temp_var = assignment_list[1].split(',')
            inventory_id = temp_var[0][8:].split(':')[1].strip()
            flight_number = all_flights[inventory_id].flight_number
            alt_flight1_string += 'Alternate Flight Choice - \n'
            alt_flight1_string +=  (temp_var[0][8:] + '\n' + temp_var[1].strip() + '\n' + temp_var[2].strip() + '\n')
            alt_flight1_string += 'Flight Number: ' + str(flight_number) + '\n'
            alt_flight1_string += ('Cabin : ' + assignment_list[2] + '\n' )
            alt_flight1_string += ('Class : ' + assignment_list[3] + '\n' )
            alt_flight1_string += 'Please click the link given below to choose this flight -\n'
            alt_flight1_string += schema_1_link
        
        
        alt_flight2_string = ''
        if assignment_2_dict[pnr]:
            assignment_list = assignment_2_dict[pnr]
            temp_var = assignment_list[1].split(',')
            inventory_id = temp_var[0][8:].split(':')[1].strip()
            flight_number = all_flights[inventory_id].flight_number
            alt_flight2_string += 'Alternate Flight Choice - \n'
            alt_flight2_string += (temp_var[0][8:] + '\n' + temp_var[1].strip() + '\n' + temp_var[2].strip() + '\n')
            alt_flight2_string += 'Flight Number: ' + str(flight_number) + '\n'
            alt_flight2_string += ('Cabin : ' + assignment_list[2] + '\n' )
            alt_flight2_string += ('Class : ' + assignment_list[3] + '\n' )
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
    


#send_mail('Results/assignments_0.csv','Results/assignments_1.csv','Results/assignments_2.csv')



