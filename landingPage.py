import streamlit as st
#import streamlit library

st.title("Business Rules Modification Engine")
st.title("Default Level Solution")
st.write("")
st.write("Business class passengers may be reallocated to-")


col1,col2=st.columns(2)
with col1:
    business_to_first=st.checkbox("First Class",key="1")    
with col2:
    business_to_economy=st.checkbox("Economy Class",key="2")    
    
st.write("")
st.write("")  
    
st.write("First class passengers may be reallocated to-")
col1,col2=st.columns(2)
with col1:
    first_to_business=st.checkbox("Business Class",key="3")    
with col2:
    first_to_economy=st.checkbox("Economy Class",key="4")    
    
st.write("")
st.write("")

st.write("Economy class passengers may be reallocated to-")

col1,col2=st.columns(2)
with col1:
    economy_to_first=st.checkbox("First Class",key="5")    
with col2:
    economy_to_business=st.checkbox("Business Class",key="6")    
    
st.write("")    
st.write("")

maxDepartDelay=st.number_input("Maximum departure delay",value=20,min_value=0)

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
        #write all variables to file when button is pressed
        f=open("default.py","w")
        f.write("business_to_first="+str(business_to_first)+"\n")
        f.write("business_to_economy="+str(business_to_economy)+"\n")
        f.write("first_to_economy="+str(first_to_economy)+"\n")
        f.write("first_to_business="+str(first_to_business)+"\n")
        f.write("economy_to_business="+str(economy_to_business)+"\n")
        f.write("economy_to_first="+str(economy_to_first)+"\n")
        f.write("maxDepartDelay="+str(maxDepartDelay)+"\n")
        f.close()
        