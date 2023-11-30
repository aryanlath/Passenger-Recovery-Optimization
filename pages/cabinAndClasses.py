import streamlit as st


#function to write list to file
def writeToList(list,listname,file):
    file.write(listname+"=[")
    for item in list:
        if (item!=list[-1]):
            file.write("'"+str(item)+"',")
        else:
            file.write("'"+str(item)+"'")
    file.write("]\n")

st.title("Class to Class Mapping for Exception List")
st.write("")


flightClassOptions=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
col1,col2=st.columns(2)
with col1:
    classChangeA = st.multiselect('Proposed Class for Class A',flightClassOptions,default=['F','S'],key=1)
    classChangeS = st.multiselect('Proposed Class for Class S',flightClassOptions,default=['F','A'],key=2)
    classChangeF = st.multiselect('Proposed Class for Class F',flightClassOptions,default=['S','A'],key=3)
    classChangeJ = st.multiselect('Proposed Class for Class J',flightClassOptions,default=['O','C','I'],key=4)
    classChangeC = st.multiselect('Proposed Class for Class C',flightClassOptions,default=['O','J','I'],key=5)
with col2:
    classChangeI = st.multiselect('Proposed Class for Class I',flightClassOptions,default=['J','C','O'],key=6)
    classChangeO = st.multiselect('Proposed Class for Class O',flightClassOptions,default=['J','C','I'],key=7)
    classChangeY = st.multiselect('Proposed Class for Class Y',flightClassOptions,default=['B','P','Z'],key=8)
    classChangeB = st.multiselect('Proposed Class for Class B',flightClassOptions,default=['Y','P','Z'],key=9)
st.write("")
st.write("")

col1,col2=st.columns(2)
with col1:
    upgrade=st.toggle("Upgrade Allowed",value="True",key=10)
with col2:
    downgrade=st.toggle("Downgrade Allowed",value="True",key=11)
st.write("")
st.write("")
st.write("")
    
st.write("Cabins Allowed")
col1,col2,col3=st.columns(3)
with col1:
    first=st.checkbox("First Class")
    if first:
        if upgrade:
            firstClassUpgrade = st.multiselect('Class for upgrade',flightClassOptions,default=['J'],key=12)
        if downgrade:
            firstClassDowngrade = st.multiselect('Class for downgrade',flightClassOptions,default=['J'],key=13)
with col2:
    business=st.checkbox("Business Class")  
    if business:
        if upgrade:    
            businessClassUpgrade = st.multiselect('Class for upgrade',flightClassOptions,default=['F'],key=14)
        if downgrade:
            businessClassDowngrade = st.multiselect('Class for downgrade',flightClassOptions,key=15)
with col3:   
    economy=st.checkbox("Economy Class")   
    if economy:
        if upgrade:
            economyClassUpgrade = st.multiselect('Class for upgrade',flightClassOptions,key=16)
        if downgrade:
            economyClassDowngrade = st.multiselect('Class for downgrade',flightClassOptions,key=17)

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
        #writing to file when button is pressed
        f=open("classRules.py","w")
        f.write("upgrade="+str(upgrade)+"\n")
        f.write("downgrade="+str(downgrade)+"\n")
        writeToList(classChangeA,"classChangeA",f)
        writeToList(classChangeS,"classChangeS",f)
        writeToList(classChangeF,"classChangeF",f)
        writeToList(classChangeJ,"classChangeJ",f)
        writeToList(classChangeC,"classChangeC",f)
        writeToList(classChangeI,"classChangeI",f)
        writeToList(classChangeO,"classChangeO",f)
        writeToList(classChangeY,"classChangeY",f)
        writeToList(classChangeB,"classChangeB",f)
        f.write("first="+str(first)+"\n")
        f.write("business="+str(business)+"\n")
        f.write("economy="+str(economy)+"\n")
        if upgrade:
            if first:
                writeToList(firstClassUpgrade,"firstClassUpgrade",f)
            if business:
                writeToList(businessClassUpgrade,"businessClassUpgrade",f)
            if economy:
                writeToList(economyClassUpgrade,"economyClassUpgrade",f)
            
        if downgrade:
            if first:
                writeToList(firstClassDowngrade,"firstClassDowngrade",f)
            if business:
                writeToList(businessClassDowngrade,"businessClassDowngrade",f)
            if economy:
                writeToList(economyClassDowngrade,"economyClassDowngrade",f)
        f.close()