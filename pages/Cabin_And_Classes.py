import streamlit as st
#importing streamlit library

#add title for page
st.title("Class to Class Mapping")

#add empty space
st.write("")

#list of all possible classes
flightClassOptions=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

#dictionary to store class as key and list of alternate classes as value
classChange={}


st.subheader("First Class")

#columns to align widgets
col1,col2=st.columns(2)
with col1:
    
    #list of classes where passengers of class F can be allocated to
    classChange['F'] = st.multiselect('Proposed Class for Class F',[subclass for subclass in flightClassOptions if subclass!='F'],default=['P','C'])
with col2:
    #list of classes where passengers of class P can be allocated to
    classChange['P'] = st.multiselect('Proposed Class for Class P',[subclass for subclass in flightClassOptions if subclass!='P'],default=['C','F'])
    

st.subheader("Business Class")
col1,col2=st.columns(2)
with col1:
    #list of classes where passengers of class C can be allocated to
    classChange['C'] = st.multiselect('Proposed Class for Class C',[subclass for subclass in flightClassOptions if subclass!='C'],default=['Z','J','P'])
    
    #list of classes where passengers of class Z can be allocated to
    classChange['Z'] = st.multiselect('Proposed Class for Class Z',[subclass for subclass in flightClassOptions if subclass!='Z'],default=['C','J','P'])
with col2:
    #list of classes where passengers of class J can be allocated to
    classChange['J'] = st.multiselect('Proposed Class for Class J',[subclass for subclass in flightClassOptions if subclass!='J'],default=['Z','C','P'])
    

st.subheader("Premium Economy Class")

col1,col2=st.columns(2)
with col1:
    
    #list of classes where passengers of class R can be allocated to
    classChange['R'] = st.multiselect('Proposed Class for Class R',[subclass for subclass in flightClassOptions if subclass!='R'],default=['Q','M','T'])

    
    #list of classes where passengers of class T can be allocated to
    classChange['T'] = st.multiselect('Proposed Class for Class T',[subclass for subclass in flightClassOptions if subclass!='T'],default=['Q','M','R'])


    #list of classes where passengers of class M can be allocated to
    classChange['M'] = st.multiselect('Proposed Class for Class M',[subclass for subclass in flightClassOptions if subclass!='M'],default=['Q','R','T'])
with col2:
    
    #list of classes where passengers of class Q can be allocated to
    classChange['Q'] = st.multiselect('Proposed Class for Class Q',[subclass for subclass in flightClassOptions if subclass!='Q'],default=['R','M','T'])
    
    
    #list of classes where passengers of class S can be allocated to
    classChange['S'] = st.multiselect('Proposed Class for Class S',[subclass for subclass in flightClassOptions if subclass!='S'],default=['Q','M','T'])

    #list of classes where passengers of class H can be allocated to
    classChange['H'] = st.multiselect('Proposed Class for Class H',[subclass for subclass in flightClassOptions if subclass!='H'],default=['Q','M','T'])



st.subheader("Economy Class")
col1,col2=st.columns(2)
with col1:
    
    
    #list of classes where passengers of class A can be allocated to
    classChange['A'] = st.multiselect('Proposed Class for Class A',[subclass for subclass in flightClassOptions if subclass!='A'],default=['D','L','X'])

    #list of classes where passengers of class D can be allocated to
    classChange['D'] = st.multiselect('Proposed Class for Class D',[subclass for subclass in flightClassOptions if subclass!='D'],default=['A','X'])

    #list of classes where passengers of class L can be allocated to
    classChange['L'] = st.multiselect('Proposed Class for Class L',[subclass for subclass in flightClassOptions if subclass!='L'],default=['O','V','X'])

    #list of classes where passengers of class O can be allocated to
    classChange['O'] = st.multiselect('Proposed Class for Class O',[subclass for subclass in flightClassOptions if subclass!='O'],default=['A','D','X'])
    
    #list of classes where passengers of class V can be allocated to
    classChange['V'] = st.multiselect('Proposed Class for Class V',[subclass for subclass in flightClassOptions if subclass!='V'],default=['A','D','O','X'])
    
    #list of classes where passengers of class X can be allocated to
    classChange['X'] = st.multiselect('Proposed Class for Class X',[subclass for subclass in flightClassOptions if subclass!='X'],default=['A','D','V'])
    
    #list of classes where passengers of class G can be allocated to
    classChange['G'] = st.multiselect('Proposed Class for Class G',[subclass for subclass in flightClassOptions if subclass!='G'],default=['A','O'])
    

    #list of classes where passengers of class K can be allocated to
    classChange['K'] = st.multiselect('Proposed Class for Class K',[subclass for subclass in flightClassOptions if subclass!='K'],default=['A','O'])
        

    
    
with col2:

    #list of classes where passengers of class Y can be allocated to
    classChange['Y'] = st.multiselect('Proposed Class for Class Y',[subclass for subclass in flightClassOptions if subclass!='Y'],default=['A','V','X'])
    
    #list of classes where passengers of class B can be allocated to
    classChange['B'] = st.multiselect('Proposed Class for Class B',[subclass for subclass in flightClassOptions if subclass!='B'],default=['O','V','X'])

    #list of classes where passengers of class E can be allocated to
    classChange['E'] = st.multiselect('Proposed Class for Class E',[subclass for subclass in flightClassOptions if subclass!='E'],default=['A','D','L'])


    #list of classes where passengers of class N can be allocated to
    classChange['N'] = st.multiselect('Proposed Class for Class N',[subclass for subclass in flightClassOptions if subclass!='N'],default=['A','D','L','O'])

    
    #list of classes where passengers of class U can be allocated to
    classChange['U'] = st.multiselect('Proposed Class for Class U',[subclass for subclass in flightClassOptions if subclass!='U'],default=['A','D','L','X'])
    
    
    #list of classes where passengers of class W can be allocated to
    classChange['W'] = st.multiselect('Proposed Class for Class W',[subclass for subclass in flightClassOptions if subclass!='W'],default=['L','O'])
        
    #list of classes where passengers of class I can be allocated to
    classChange['I'] = st.multiselect('Proposed Class for Class I',[subclass for subclass in flightClassOptions if subclass!='I'],default=['A','D'])
        

    
    
    
    
#add empty space
st.write("")
st.write("")

#variable value true if upgrade allowed
col1,col2=st.columns(2)
with col1:    
    upgrade=st.toggle("Upgrade Allowed",value="True")
with col2:
    downgrade=st.toggle("Downgrade Allowed",value="True")
   
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
        
        #writing classChange dictionary to file
        f.write("classChange={")
        for key,value in classChange.items():
            
            if (key!=list(classChange.keys())[-1]):    
                #separate each entry
                f.write("'"+(key)+"':"+str(value)+",")
            else:
                #add closing brace
                f.write("'"+(key)+"':"+str(value)+"}")

        f.close()
        #close file