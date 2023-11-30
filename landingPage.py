import streamlit as st
#import streamlit library

#add title
st.title("Business Rules Modification Engine")
st.title("Default Level Solution")

#for spacing
st.write("")

#heading
st.write("Business class passengers may be reallocated to-")


#create two columns to align checkboxes
col1,col2=st.columns(2)
with col1: 
    #variable value 1 if business to first class change allowed, 0 otherwise
    business_to_first=st.checkbox("First Class",key="1")    
with col2:
    #variable value 1 if business to economy class change allowed, 0 otherwise
    business_to_economy=st.checkbox("Economy Class",key="2")    
    
#add empty spacing
st.write("")
st.write("")  
    

st.write("First class passengers may be reallocated to-")
#create two columns to align checkboxes
col1,col2=st.columns(2)
with col1:
    #variable value 1 if first to business class change allowed, 0 otherwise
    first_to_business=st.checkbox("Business Class",key="3")    
with col2:
    #variable value 1 if first to economy class change allowed, 0 otherwise
    first_to_economy=st.checkbox("Economy Class",key="4")    
    
#add empty spacing
st.write("")
st.write("")

st.write("Economy class passengers may be reallocated to-")

col1,col2=st.columns(2)
with col1:
    #variable value 1 if economy to first class change allowed, 0 otherwise
    economy_to_first=st.checkbox("First Class",key="5")    
with col2:
    #variable value 1 if economy to business class change allowed, 0 otherwise
    economy_to_business=st.checkbox("Business Class",key="6")    
    
    
#add empty space
st.write("")    
st.write("")

#variable value denotes maximum departure delay allowed with default value 20
maxDepartDelay=st.number_input("Maximum departure delay",value=20,min_value=0)

#columns made to bring button to center
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
        #when button is pressed
        f=open("default.py","w")
        #overwrites file each time its run
        
        #writes class change permissions for business class
        f.write("business_to_first="+str(business_to_first)+"\n")
        f.write("business_to_economy="+str(business_to_economy)+"\n")
        
        #writes class change permissions for first class
        f.write("first_to_economy="+str(first_to_economy)+"\n")
        f.write("first_to_business="+str(first_to_business)+"\n")
        
        #writes class change permissions for economy class
        f.write("economy_to_business="+str(economy_to_business)+"\n")
        f.write("economy_to_first="+str(economy_to_first)+"\n")
        
        f.write("maxDepartDelay="+str(maxDepartDelay)+"\n")
        #write variable nameed maxDepartDelay 
        
        f.close()
        #closes file
        