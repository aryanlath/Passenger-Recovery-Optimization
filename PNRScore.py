import streamlit as st
#import streamlit library

#from flight_assignment_optimization import *
#to import function that returns alternate flights

#default values of data
pnr_data_file = 'Dataset/passenger_pnr_dataset.csv'
flight_data_file = 'Dataset/flight_schedule_dataset.csv'
test_PNR_data_file = 'Dataset/Mphasis_Processed/Mock_PNR_Booking.csv'
test_flight_data_file = 'Dataset/Mphasis_Processed/Mock_Flight_Inv.csv'
airport_code_location_data_file = 'Dataset/airport-code-to-location.csv'
# test_PNR_data_file = 'Dataset/test_data/PNR_Test.csv'
# test_flight_data_file = 'Dataset/test_data/flight_test.csv'

n_cabin = 2
ETD = 72
MCT = 1
MAXCT = 12
upgrade=True
downgrade=True
st.title("Business Rules Modification Engine")
#heading
st.header("PNR Level Score Modifications")
st.write("")

#heading
st.subheader("Cabin Score")

#to add empty space
st.write("")
st.write("")

#score for cabin F
cabinScoreFirst=st.slider("First Class",1500,2000,value=1950)

#score for cabin Y
cabinScoreBusiness=st.slider("Business Class",1500,2000,value=1800)

#
cabinScorePremium=st.slider("Premium Economy",1500,2000,value=1700)

#score for cabin J
cabinScoreEconomy=st.slider("Economy",1500,2000,value=1500)
st.write("")

st.write("")

#loyalty scores
st.subheader("Loyalty")

st.write("")
col1,col2=st.columns(2)
with col1:
    #score for CM Presidential Platinum class
    CM=st.slider("CM Presidential Platinum",1500,2000,value=2000)
    
    #score for gold class
    gold=st.slider("Gold",1500,2000,value=1600)
with col2:
    #score for platinum class
    platinum=st.slider("Platinum",1500,2000,value=1800)
    
    #score for silver class
    silver=st.slider("Silver",1500,2000,value=1500)

st.write("")
#heading
st.subheader("Other Scores")
st.write("")

col1,col2,col3=st.columns(3)
with col1:
    #score for SSR
    col1a,col1b=st.columns(2)
    with col1a:
        #SSR grade 1
        grade1=st.number_input("SSR Grade 1",value=250,min_value=0)
    with col1b:
        #SSR grade 2
        grade2=st.number_input("SSR Grade 2",value=150,min_value=0)
    
    #score for connection downline
    PNR_connection=st.number_input("Connection Downline",value=100,min_value=0)
    
with col2:
    #score for paid service
    PNR_paidservice=st.number_input("Paid Service",value=200,min_value=0)
    
    #score for group booking 
    PNR_bookingtype=st.number_input("Booking Type",value=500,min_value=0)
    
with col3:
    #score for PAX
    PNR_pax=st.number_input("PAX",value=50,min_value=0)
    
    #score for no allocation penalty
    PNR_penalty=st.number_input("Penalty for no allocation",value=100,min_value=0)

st.write("")

st.subheader("Weightage")


#divide into 3 columns
col1,col2,col3=st.columns(3)
with col1:
    #score when stopover is present
    weight_flight_map=st.number_input("Enter weightage of flight score",value=100,min_value=0)
with col2:
    #score to add when equipment number matches
    weight_pnr_map=st.number_input("Enter weightage of PNR score",value=100,min_value=0)
with col3:
    #score for maximum departure delay
    weight_cabin_map=st.number_input("Enter weightage of cabin score",value=100,min_value=0)



#add empty space
st.write("")
st.write("")


#other modifications
st.header("Other Modifications")

st.write("")
col1,col2,col3=st.columns(3)
with col1:
    #constraint for max ETD
    ETD = st.number_input("Enter Maximum ETD Allowed",value=ETD,min_value=0)
    
with col2:
    #constraint for maximum connecting time
    MAXCT= st.number_input("Enter Maximum Connecting Time",min_value=0,value=MAXCT)
    
with col3:
    #constraint for minimum connecting time
    MCT= st.number_input("Enter Minimum Connecting Time",min_value=0,value=MCT)

CITY_PAIR_THRESHOLD=st.number_input("Enter maximum allowed travel time between original and new airport",min_value=0,value=8)
#add empty space
st.write("")
st.write("")

#columns added to bring button to center
col1, col2, col3,col4,col5 = st.columns(5)
with col1:
    pass
with col2 :
    pass
with col4 :
    pass
with col5 :
    pass
with col3:
    if (st.button("Proceed")):
        #writing to file when button is pressed
        f = open("constants.py", "w")
        
        #pnr data source
        f.write("pnr_data_file = 'Dataset/passenger_pnr_dataset.csv'\n")
        
        #important datasets
        f.write("flight_data_file = 'Dataset/flight_schedule_dataset.csv'\n")
        f.write("test_PNR_data_file = 'Dataset/Mphasis_Processed/Mock_PNR_Booking.csv'\n")
        f.write("test_flight_data_file = 'Dataset/Mphasis_Processed/Mock_Flight_Inv.csv'\n")
        f.write("airport_code_location_data_file = 'Dataset/airport-code-to-location.csv'\n")
        f.write("# test_PNR_data_file = 'Dataset/test_data/PNR_Test.csv'\n")
        f.write("# test_flight_data_file = 'Dataset/test_data/flight_test.csv'\n")
        
        #writing number of cabins
        f.write("n_cabin="+str(n_cabin)+"\n")
        
        #writing ETD 
        f.write("ETD="+str(ETD)+"\n")
        
        #CabinScore
        #First
        f.write("cabinScoreFirst="+str(cabinScoreFirst)+"\n")
        #Business
        f.write("cabinScoreBusiness="+str(cabinScoreBusiness)+"\n")
        #Premium Economy
        f.write("cabinScorePremium="+str(cabinScorePremium)+"\n")
        #Economy
        f.write("cabinScoreEconomy="+str(cabinScoreEconomy)+"\n")
        
        
        #writing MCT
        f.write("MCT="+str(MCT)+"\n")
        
        #writing MAXCT
        f.write("MAXCT="+str(MAXCT)+"\n")
        
        #writing PNR scores
        
        #SSR score dictionary
        f.write("PNR_SSR={'grade1':"+str(grade1)+",'grade2':"+str(grade2)+"}\n")
        
        #writing loyalty dictionary
        f.write("loyalty={'CM':"+str(CM)+",'platinum':"+str(platinum)+",'gold':"+str(gold)+",'silver':"+str(silver)+"}\n")
        
        #connection score
        f.write("PNR_connection="+str(PNR_connection)+"\n")
        
        #paid service score
        f.write("PNR_paidservice="+str(PNR_paidservice)+"\n")
        
        #group booking score
        f.write("PNR_bookingtype="+str(PNR_bookingtype)+"\n")
        
        #PAX score
        f.write("PNR_pax="+str(PNR_pax)+"\n")
        
        #penalty score
        f.write("NON_ASSIGNMENT_COST="+str(-PNR_penalty)+"\n")
        
        #writing city pair thershold score
        f.write("CITY_PAIR_THRESHOLD="+str(CITY_PAIR_THRESHOLD)+"\n")
        
        #writing weightage
        f.write("weight_flight_map="+str(weight_flight_map)+"\n")
        f.write("weight_pnr_map="+str(weight_pnr_map)+"\n")
        f.write("weight_cabin_map="+str(weight_cabin_map)+"\n")
        
        
        #close file
        f.close()
       
        

