import streamlit as st

#data
pnr_data_file = "Dataset/passenger_pnr_dataset.csv"
flight_data_file = "Dataset/flight_schedule_dataset.csv"
n_cabin = 2
ETD = 72
MCT = 1
MAXCT = 12
upgrade=True
downgrade=True


st.header("PNR Level Score Modifications")
st.write("")

st.subheader("Cabin Score")
st.write("")
st.write("")

cabinScoreF=st.slider("F",1500,2000,value=1700)
cabinScoreY=st.slider("Y",1500,2000,value=1500)
cabinScoreJ=st.slider("J",1500,2000,value=2000)
st.write("")
st.subheader("Class Score")

st.write("")

col1, col2, col3 = st.columns(3)
with col1:
    classScoreA = st.number_input("Enter Score for Class A",value=700,min_value=500,max_value=1000)
with col2:
    classScoreB = st.number_input("Enter Score for Class B",value=700,min_value=500,max_value=1000)
with col3 :
    classScoreC = st.number_input("Enter Score for Class C",value=700,min_value=500,max_value=1000)


st.write("")
st.subheader("Loyalty")
st.write("")
col1,col2=st.columns(2)
with col1:
    CM=st.slider("CM Presidential Platinum",1500,2000,value=2000)
    gold=st.slider("Gold",1500,2000,value=1600)
with col2:
    platinum=st.slider("Platinum",1500,2000,value=1800)
    silver=st.slider("Silver",1500,2000,value=1500)

st.write("")
st.subheader("Other Scores")
st.write("")

col1,col2,col3=st.columns(3)
with col1:
    PNR_SSR=st.number_input("SSR",value=200,min_value=0)
    PNR_connection=st.number_input("Connection Downline",value=100,min_value=0)
with col2:
    PNR_paidservice=st.number_input("Paid Service",value=200,min_value=0)
    PNR_bookingtype=st.number_input("Booking Type",value=500,min_value=0)
with col3:
    PNR_pax=st.number_input("PAX",value=50,min_value=0)

st.write("")

st.header("Other Modifications")

st.write("")
col1,col2,col3=st.columns(3)
with col1:
    ETD = st.number_input("Enter Maximum ETD Allowed",value=ETD,min_value=0)
with col2:
    MAXCT= st.number_input("Enter Maximum Connecting Time",min_value=0,value=MAXCT)
with col3:
    MCT= st.number_input("Enter Minimun Connecting Time",min_value=0,value=MCT)

st.write("")
st.write("")

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
        #writing PNR button to file when button is pressed
        f = open("constants.py", "w")
        f.write("pnr_data_file = 'Dataset/passenger_pnr_dataset.csv'\n")
        f.write("flight_data_file = 'Dataset/flight_schedule_dataset.csv'\n")
        f.write("n_cabin="+str(n_cabin)+"\n")
        f.write("ETD="+str(ETD)+"\n")
        f.write("MCT="+str(MCT)+"\n")
        f.write("MAXCT="+str(MAXCT)+"\n")
        f.write("PNR_SSR="+str(PNR_SSR)+"\n")
        f.write("PNR_connection="+str(PNR_connection)+"\n")
        f.write("PNR_paidservice="+str(PNR_paidservice)+"\n")
        f.write("PNR_bookingtype="+str(PNR_bookingtype)+"\n")
        f.write("PNR_pax="+str(PNR_pax)+"\n")
        f.write("Loyalty_CM="+str(CM)+"\n")
        f.write("Loyalty_platinum="+str(platinum)+"\n")
        f.write("Loyalty_gold="+str(gold)+"\n")
        f.write("Loyalty_silver="+str(silver)+"\n")
        f.close()

