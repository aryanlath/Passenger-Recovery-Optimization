# mail the PNRs from assignments.csv to the respective passengers

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import pandas as pd
import smtplib
import time

# create a function for sending emails
def send_mail(filepath):
    '''
    This function sends an email to the passengers whose flight has been cancelled.
    '''

    print("Do you want to send emails to the passengers whose flight has been cancelled? (y/n)")
    choice = input()
    if choice == 'n':
        return
    
    # Define the content of the email
    name = "Mock Airlines"
    email = "shivamtestmail321@gmail.com"
    pwd = "avvf oink uqyi iebw"

    # Read the csv file
    data = pd.read_csv(filepath)
    rows = data.shape[0]

    # Connect to the Gmail SMTP server
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(email,pwd)
    print('Connected to Gmail SMTP server of ', email)
    for i in range(rows):
        msg = """
    <html>
    <body>
    <div>

    <p>Dear Sir/Ma'am,</p>
    <p>Thank you for choosing """+name+""".</p>
    <br>
    <p>Unfortunately, your flight has been cancelled, please find alternate flight details below.</p>
    <br>
    <p>Flight Details:</p>
    <p>Your PNR is """+data['PNR_Number'][i]+""".</p>
    <p>Your rescheduled flight is \n"""+data['Flight'][i]+""".</p>
    <p>Your cabin is """+data['Cabin'][i]+""".</p>
    <br>
    <p>Have a safe journey.</p>
    <br>
    <p>Regards,</p>
    <p>"""+name+"""</p>

    </div>
    </body>
    </html>
        """.format(data['PNR_Number'][i],data['Flight'][i],data['Cabin'][i],name)

        email_message = MIMEMultipart()
        email_message['From'] = name
        email_message['To'] = data['PNR_Email'][i]
        email_message['Subject'] = f"Flight Cancellation - {data['PNR_Number'][i]}"

        # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
        email_message.attach(MIMEText(msg, "html"))
        # Convert it as a string
        email_string = email_message.as_string()

        # Connect to the Gmail SMTP server and Send Email
        context = ssl.create_default_context()

        server.sendmail(email, data['PNR_Email'][i], email_string)

        print("Mail sent to ",data['PNR_Email'][i])
        time.sleep(2)

    server.quit()