import streamlit as st
#importing streamlit library

#function to write list to file taking list, name of list 
#to write and file to write to as arguments
def writeToList(list,listname,file):
    #start with <listname>=
    file.write(listname+"=[")
    for item in list:
        #add each item and add a comma at the end
        if (item!=list[-1]):
            file.write("'"+str(item)+"',")
        else:
            file.write("'"+str(item)+"'")
        
    file.write("]\n")
    #add closing bracket 

#add title for page
st.title("Class to Class Mapping for Exception List")

#add empty space
st.write("")

#list of all possible classes
flightClassOptions=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

#columns to align widgets
col1,col2=st.columns(2)
with col1:
    #list of classes where passengers of class A can be allocated to
    classChangeA = st.multiselect('Proposed Class for Class A',flightClassOptions,default=['F','S'],key=1)

    #list of classes where passengers of class S can be allocated to
    classChangeS = st.multiselect('Proposed Class for Class S',flightClassOptions,default=['F','A'],key=2)
    
    #list of classes where passengers of class F can be allocated to
    classChangeF = st.multiselect('Proposed Class for Class F',flightClassOptions,default=['S','A'],key=3)
    
    #list of classes where passengers of class J can be allocated to
    classChangeJ = st.multiselect('Proposed Class for Class J',flightClassOptions,default=['O','C','I'],key=4)
    
    #list of classes where passengers of class C can be allocated to
    classChangeC = st.multiselect('Proposed Class for Class C',flightClassOptions,default=['O','J','I'],key=5)
with col2:
    #list of classes where passengers of class I can be allocated to
    classChangeI = st.multiselect('Proposed Class for Class I',flightClassOptions,default=['J','C','O'],key=6)
    
    #list of classes where passengers of class O can be allocated to
    classChangeO = st.multiselect('Proposed Class for Class O',flightClassOptions,default=['J','C','I'],key=7)
    
    #list of classes where passengers of class Y can be allocated to
    classChangeY = st.multiselect('Proposed Class for Class Y',flightClassOptions,default=['B','P','Z'],key=8)
    
    #list of classes where passengers of class B can be allocated to
    classChangeB = st.multiselect('Proposed Class for Class B',flightClassOptions,default=['Y','P','Z'],key=9)

#add empty space
st.write("")
st.write("")

#add columns 
col1,col2=st.columns(2)
with col1:
    #variable value true if upgrade allowed
    upgrade=st.toggle("Upgrade Allowed",value="True",key=10)
    
with col2:
    #variable value true if downgrade allowed
    downgrade=st.toggle("Downgrade Allowed",value="True",key=11)
   
 #add empty space   
st.write("")
st.write("")
st.write("")
    
#allowed cabins
st.write("Cabins Allowed")
col1,col2,col3=st.columns(3)
with col1:
    first=st.checkbox("First Class")
    if first:
        if upgrade:
            #option visible if first class and upgrade option chosen
            #contains classes to allocate when upgraded
            firstClassUpgrade = st.multiselect('Class for upgrade',flightClassOptions,default=['J'],key=12)
            
        if downgrade:
            
            #option visible if first class and downgrade option chosen
            #contains classes to allocate when downgraded
            firstClassDowngrade = st.multiselect('Class for downgrade',flightClassOptions,default=['J'],key=13)
with col2:
    business=st.checkbox("Business Class")  
    if business:
        if upgrade:    
            #option visible if business class and upgrade option chosen
            #contains classes to allocate when upgraded
            businessClassUpgrade = st.multiselect('Class for upgrade',flightClassOptions,default=['F'],key=14)
            
        if downgrade:
            #option visible if business class and downgrade option chosen
            #contains classes to allocate when downgraded
            businessClassDowngrade = st.multiselect('Class for downgrade',flightClassOptions,key=15)
with col3:   
    economy=st.checkbox("Economy Class")   
    if economy:
        if upgrade:
            #option visible if economy class and upgrade option chosen
            #contains classes to allocate when upgraded
            economyClassUpgrade = st.multiselect('Class for upgrade',flightClassOptions,key=16)
            
        if downgrade:
            #option visible if economy class and downgrade option chosen
            #contains classes to allocate when downgraded
            economyClassDowngrade = st.multiselect('Class for downgrade',flightClassOptions,key=17)

#add empty space
st.write("")
st.write("")

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
        #writing to file when button is pressed
        f=open("classRules.py","w")
        
        #truth value for upgrade and downgrade
        f.write("upgrade="+str(upgrade)+"\n")
        f.write("downgrade="+str(downgrade)+"\n")
        
        #creating lists in the file
        #contains which other classes the original class can be changed to 
        writeToList(classChangeA,"classChangeA",f)
        writeToList(classChangeS,"classChangeS",f)
        writeToList(classChangeF,"classChangeF",f)
        writeToList(classChangeJ,"classChangeJ",f)
        writeToList(classChangeC,"classChangeC",f)
        writeToList(classChangeI,"classChangeI",f)
        writeToList(classChangeO,"classChangeO",f)
        writeToList(classChangeY,"classChangeY",f)
        writeToList(classChangeB,"classChangeB",f)
        
        #true if first class present
        f.write("first="+str(first)+"\n")
        
        #true if business class present
        f.write("business="+str(business)+"\n")
        
        ##true if economy class present
        f.write("economy="+str(economy)+"\n")
        if upgrade:
            if first:
                #when upgrade allowed and first class present
                #writes list of classes allocated when upgraded
                writeToList(firstClassUpgrade,"firstClassUpgrade",f)
                
            if business:
                #when upgrade allowed and business class present
                #writes list of classes allocated when upgraded
                writeToList(businessClassUpgrade,"businessClassUpgrade",f)
                
            if economy:
                #when upgrade allowed and economy class present
                #writes list of classes allocated when upgraded
                writeToList(economyClassUpgrade,"economyClassUpgrade",f)
            
        if downgrade:
            if first:
                #when downgrade allowed and first class present
                #writes list of classes allocated when downgraded
                writeToList(firstClassDowngrade,"firstClassDowngrade",f)
                
            if business:
                #when downgrade allowed and business class present
                #writes list of classes allocated when downgraded
                writeToList(businessClassDowngrade,"businessClassDowngrade",f)
                
            if economy:
                #when downgrade allowed and economy class present
                #writes list of classes allocated when downgraded
                writeToList(economyClassDowngrade,"economyClassDowngrade",f)
                
        f.close()
        #close file