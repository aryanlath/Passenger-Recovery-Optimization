import streamlit as st
#import library 

#write page title
st.title("Flight Scores")

#add empty space
st.write("")

#add heading
st.subheader("Arrival Delay")

#add columns for proper alignment 
col1,col2=st.columns(2)
with col1:
    #score for arrival delay of less than 6 hours
    arrDelay6h=st.number_input("Less than 6 hours",value=70,min_value=0)
    
    #score for arrival delay of less than 12 hours
    arrDelay12h=st.number_input("Less than 12 hours",value=50,min_value=0)
with col2:
    #score for arrival delay of less than 24 hours
    arrDelay24h=st.number_input("Less than 24 hours",value=40,min_value=0)
    
    #score for arrival delay of less than 48 hours
    arrDelay48h=st.number_input("Less than 48 hours",value=30,min_value=0)

#heading for next section
st.subheader("STD of proposed flight")

#divide into columns
col1,col2=st.columns(2)
with col1:
    #score for departure delay of less than 6 hours
    STD6h=st.number_input("Less than 6 hours",value=70,min_value=0,key=1)
   
    #score for departure delay of less than 12 hours
    STD12h=st.number_input("Less than 12 hours",value=50,min_value=0,key=2)
with col2:
    #score for departure delay of less than 24 hours
    STD24h=st.number_input("Less than 24 hours",value=40,min_value=0,key=3)
    
    #score for departure delay of less than 48 hours
    STD48h=st.number_input("Less than 48 hours",value=30,min_value=0,key=4)

#score for citypairs
st.subheader("City Pairs")

#divide into columns for alignment 
col1,col2,col3=st.columns(3)
with col1:
    #score when citypairs same
    citypairsSame=st.number_input("Same citypairs",value=40,min_value=0)
    
with col2:
    #score when citypairs different in same city
    citypairsSameCity=st.number_input("Different citypairs in same city",value=30,min_value=0)
    
with col3:
    #score when citypairs different
    citypairsDifferent=st.number_input("Different citypairs",value=20,min_value=0)

#cutoff for each grade
st.subheader("Quality Score Grade")

col1,col2,col3=st.columns(3)
with col1:
    #flight score for grade A
    gradeA=st.number_input("Minimum score for grade A",value=200,min_value=0)
    
with col2:
    #flight score for grade B
    gradeB=st.number_input("Minimum score for grade B",value=180,min_value=0)
    
with col3:
    #flight score for grade C
    gradeC=st.number_input("Minimum score for grade C",value=150,min_value=0)

#other modifications
st.subheader("Others")

#divide into 3 columns
col1,col2,col3=st.columns(3)
with col1:
    #score when stopover is present
    stopOver=st.number_input("Stopover",value=-20)
    
with col2:
    #score to add when equipment number matches
    equipmentScore=st.number_input("Matching Equipment number",value=50)
with col3:
    #score for maximum departure delay
    maxDepartDelay=st.number_input("Maximum departure delay",value=20,min_value=0)

#add empty space
st.write("")
st.write("")



#columns created to bring button to center
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
        #writing to file
        f=open("flightScores.py","w")
        
        #adding all arrival delay scores
        f.write("arrDelay6h="+str(arrDelay6h)+"\n")
        f.write("arrDelay12h="+str(arrDelay12h)+"\n")
        f.write("arrDelay24h="+str(arrDelay24h)+"\n")
        f.write("arrDelay48h="+str(arrDelay48h)+"\n")
        
        #adding all departure time scores
        f.write("STD6h="+str(STD6h)+"\n")
        f.write("STD12h="+str(STD12h)+"\n")
        f.write("STD24h="+str(STD24h)+"\n")
        f.write("STD48h="+str(STD48h)+"\n")
        
        #adding citypair scors
        f.write("citypairsSame="+str(citypairsSame)+"\n")
        f.write("citypairsSameCity="+str(citypairsSameCity)+"\n")
        f.write("citypairsDifferent="+str(citypairsDifferent)+"\n")
        
        #adding flight grade scores
        f.write("gradeA="+str(gradeA)+"\n")
        f.write("gradeB="+str(gradeB)+"\n")
        f.write("gradeC="+str(gradeC)+"\n")
        
        #adding score for stopover
        f.write("stopOver="+str(stopOver)+"\n")
        
        #adding score for equipment match
        f.write("equipmentScore="+str(equipmentScore)+"\n")
        
        #maximum departure delay
        f.write("maxDepartDelay="+str(maxDepartDelay)+"\n")
        
        
        #closing file
        f.close()