import requests
from bs4 import BeautifulSoup
import pandas as pd
schema0_spreadsheet = 'https://docs.google.com/spreadsheets/d/1W1HSq7Ee5NfQe25ZIKfoGvg7fnXr5J9XDuBbtUf81Uk/edit?usp=sharing'
schema1_spreadsheet = 'https://docs.google.com/spreadsheets/d/1HEp47TJ1rAeLa-1J5Chrs3ZW-FR4WsnvzW7iA2ftQTY/edit?usp=sharing'
schema2_spreadsheet = 'https://docs.google.com/spreadsheets/d/137O9b-uzkqAbHnyF937AEcLeU3P76HAJ4VgNTSMBi3A/edit?usp=sharing'
cancellation_spreadsheet = 'https://docs.google.com/spreadsheets/d/1e9cy0pX1wj1Gju41nRHBpi5xSDyJW44LzYy7mFojXWc/edit?usp=sharing'
def extract_responses(url):

    
    # Fetch the HTML content of the Google Sheet
    response = requests.get(url)
    html_content = response.text
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find the table element containing the data
    table = soup.find('table')
    
    # Extract the data rows
    data_rows = []
    for tr in table.find_all('tr'):
        # Extract only the first two columns (td or th elements)
        row = [td.text.strip() for td in tr.find_all(['td', 'th'])[1:3]]
        data_rows.append(row)
    
    # Create a pandas DataFrame
    df = pd.DataFrame(data_rows, columns=['Column1', 'Column2'])  # Replace with your actual column names
    
    # Convert each column to a list
    column1_list = df['Column1'].tolist()
    column2_list = df['Column2'].tolist()
    

    l1 = []
    l2 = []
    
    for x in column1_list:
        if x != '':
            l1.append(x)
    for y in column2_list:
        if y != '':
            l2.append(y)
            
    return list(zip(l1[2:],l2[2:]))

def pnr_choices(schema0_spreadsheet,schema1_spreadsheet,schema2_spreadsheet,cancellation_spreadsheet):
    schema0 = extract_responses(schema0_spreadsheet)
    schema1 = extract_responses(schema1_spreadsheet)
    schema2 = extract_responses(schema2_spreadsheet)
    cancellation = extract_responses(cancellation_spreadsheet)
    
    pnr_dict = {}
    for x in schema0:
        pnr_dict[x[1]] = [x[0],'Schema 0']
    for x in schema1:
        pnr_dict[x[1]] = [x[0],'Schema 1']
    for x in schema2:
        pnr_dict[x[1]] = [x[0],'Schema 2']
    for x in cancellation:
        pnr_dict[x[1]] = [x[0],'Cancelled']    
    return pnr_dict



print(pnr_choices(schema0_spreadsheet, schema1_spreadsheet, schema2_spreadsheet,cancellation_spreadsheet))
