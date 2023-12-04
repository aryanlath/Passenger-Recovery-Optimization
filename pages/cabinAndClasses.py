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

#variable value true if upgrade allowed
col1,col2=st.columns(2)
with col1:    
    upgrade=st.toggle("Upgrade Allowed",value="True",key=10)
with col2:
    downgrade=st.toggle("Downgrade Allowed",value="True",key=11)
   
 #add empty space   
st.write("")
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
        f.write("classChange={'A':"+str(classChangeA)+",'S':"+str(classChangeS)+
                ",'F':"+str(classChangeF)+",'J':"+str(classChangeJ) +",'C':"+
                str(classChangeC)+",'I':"+str(classChangeI)+",'O':"+str(classChangeO)
                +",'Y':"+str(classChangeY)+",'B':"+str(classChangeB)+"}")
        
        
        #true if first class present
     #   f.write("first="+str(first)+"\n")
        
        #true if business class present
      #  f.write("business="+str(business)+"\n")
        
        ##true if economy class present
       # f.write("economy="+str(economy)+"\n")
              
        f.close()
        #close file