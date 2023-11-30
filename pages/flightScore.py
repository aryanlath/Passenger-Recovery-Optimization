import streamlit as st

st.title("Flight Scores")
st.write("")

st.subheader("Arrival Delay")
col1,col2=st.columns(2)
with col1:
    arrDelay6h=st.number_input("Less than 6 hours",value=70,min_value=0)
    arrDelay12h=st.number_input("Less than 12 hours",value=50,min_value=0)
with col2:
    arrDelay24h=st.number_input("Less than 24 hours",value=40,min_value=0)
    arrDelay48h=st.number_input("Less than 48 hours",value=30,min_value=0)

st.subheader("STD of proposed flight")
col1,col2=st.columns(2)
with col1:
    STD6h=st.number_input("Less than 6 hours",value=70,min_value=0,key=1)
    STD12h=st.number_input("Less than 12 hours",value=50,min_value=0,key=2)
with col2:
    STD24h=st.number_input("Less than 24 hours",value=40,min_value=0,key=3)
    STD48h=st.number_input("Less than 48 hours",value=30,min_value=0,key=4)


st.subheader("City Pairs")
col1,col2,col3=st.columns(3)
with col1:
    citypairsSame=st.number_input("Same citypairs",value=40,min_value=0)
with col2:
    citypairsSameCity=st.number_input("Different citypairs in same city",value=30,min_value=0)
with col3:
    citypairsDifferent=st.number_input("Different citypairs",value=20,min_value=0)


st.subheader("Quality Score Grade")
col1,col2,col3=st.columns(3)
with col1:
    gradeA=st.number_input("Minimum score for grade A",value=200,min_value=0)
with col2:
    gradeB=st.number_input("Minimum score for grade B",value=180,min_value=0)
with col3:
    gradeC=st.number_input("Minimum score for grade C",value=150,min_value=0)

st.subheader("Others")
col1,col2=st.columns(2)
with col1:
    stopOver=st.number_input("Stopover",value=-20)
with col2:
    equipmentScore=st.number_input("Matching Equipment number",value=50)

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
        #writing all variables to file when button is pressed
        f=open("flightScores.py","w")
        f.write("arrDelay6h="+str(arrDelay6h)+"\n")
        f.write("arrDelay12h="+str(arrDelay12h)+"\n")
        f.write("arrDelay24h="+str(arrDelay24h)+"\n")
        f.write("arrDelay48h="+str(arrDelay48h)+"\n")
        f.write("STD6h="+str(STD6h)+"\n")
        f.write("STD12h="+str(STD12h)+"\n")
        f.write("STD24h="+str(STD24h)+"\n")
        f.write("STD48h="+str(STD48h)+"\n")
        f.write("citypairsSame="+str(citypairsSame)+"\n")
        f.write("citypairsSameCity="+str(citypairsSameCity)+"\n")
        f.write("citypairsDifferent="+str(citypairsDifferent)+"\n")
        f.write("gradeA="+str(gradeA)+"\n")
        f.write("gradeB="+str(gradeB)+"\n")
        f.write("gradeC="+str(gradeC)+"\n")
        f.write("stopOver="+str(stopOver)+"\n")
        f.write("equipmentScore="+str(equipmentScore)+"\n")
        f.close()