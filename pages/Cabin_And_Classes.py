import streamlit as st
#importing streamlit library

#add title for page
st.title("Class to Class Mapping")

#add empty space
st.write("")


#dictionary to store class as key and list of alternate classes as value
classChange={}
global_class=['Y','A','B','D','E','G','I','K','L','N','O','U','V','W','X','F','P','C','J','Z','Q','R','S','T','H','M']
subClassFirst=global_class

st.subheader("First Class")

#columns to align widgets
col1,col2=st.columns(2)
with col1:
    
    #list of classes where passengers of class F can be allocated to
    classChange['F'] = st.multiselect('Proposed Class for Class F',subClassFirst,default=['F'])
with col2:
    #list of classes where passengers of class P can be allocated to
    classChange['P'] = st.multiselect('Proposed Class for Class P',subClassFirst,default=['P'])
    
subClassBusiness=global_class

st.subheader("Business Class")
col1,col2=st.columns(2)
with col1:
    #list of classes where passengers of class C can be allocated to
    classChange['C'] = st.multiselect('Proposed Class for Class C',subClassBusiness,default=['C'])
    
    #list of classes where passengers of class Z can be allocated to
    classChange['Z'] = st.multiselect('Proposed Class for Class Z',subClassBusiness,default=['Z'])
with col2:
    #list of classes where passengers of class J can be allocated to
    classChange['J'] = st.multiselect('Proposed Class for Class J',subClassBusiness,default=['J'])
    
subClassPremium=global_class

st.subheader("Premium Economy Class")

col1,col2=st.columns(2)
with col1:
    
    #list of classes where passengers of class R can be allocated to
    classChange['R'] = st.multiselect('Proposed Class for Class R',subClassPremium,default=['Q','R','H','M'])

    
    #list of classes where passengers of class T can be allocated to
    classChange['T'] = st.multiselect('Proposed Class for Class T',subClassPremium,default=['Q'])


    #list of classes where passengers of class M can be allocated to
    classChange['M'] = st.multiselect('Proposed Class for Class M',subClassPremium,default=['Q','H','M'])
with col2:
    
    #list of classes where passengers of class Q can be allocated to
    classChange['Q'] = st.multiselect('Proposed Class for Class Q',subClassPremium,default=['Q'])
    
    
    #list of classes where passengers of class S can be allocated to
    classChange['S'] = st.multiselect('Proposed Class for Class S',subClassPremium,default=['S','T','H'])

    #list of classes where passengers of class H can be allocated to
    classChange['H'] = st.multiselect('Proposed Class for Class H',subClassPremium,default=['Q','M'])

subClassEconomy=global_class

st.subheader("Economy Class")
col1,col2=st.columns(2)
with col1:
    
    
    #list of classes where passengers of class A can be allocated to
    classChange['A'] = st.multiselect('Proposed Class for Class A',subClassEconomy,default=['Y','A'])

    #list of classes where passengers of class D can be allocated to
    classChange['D'] = st.multiselect('Proposed Class for Class D',subClassEconomy,default=['D','E','G'])

    #list of classes where passengers of class L can be allocated to
    classChange['L'] = st.multiselect('Proposed Class for Class L',subClassEconomy,default=['W','X'])

    #list of classes where passengers of class O can be allocated to
    classChange['O'] = st.multiselect('Proposed Class for Class O',subClassEconomy,default=['K','L'])
    
    #list of classes where passengers of class V can be allocated to
    classChange['V'] = st.multiselect('Proposed Class for Class V',subClassEconomy,default=['O'])
    
    #list of classes where passengers of class X can be allocated to
    classChange['X'] = st.multiselect('Proposed Class for Class X',subClassEconomy,default=['D','E'])
    
    #list of classes where passengers of class G can be allocated to
    classChange['G'] = st.multiselect('Proposed Class for Class G',subClassEconomy,default=['V','W','X'])
    

    #list of classes where passengers of class K can be allocated to
    classChange['K'] = st.multiselect('Proposed Class for Class K',subClassEconomy,default=['K'])
        

    
    
with col2:

    #list of classes where passengers of class Y can be allocated to
    classChange['Y'] = st.multiselect('Proposed Class for Class Y',subClassEconomy,default=['K','E'])
    
    #list of classes where passengers of class B can be allocated to
    classChange['B'] = st.multiselect('Proposed Class for Class B',subClassEconomy,default=['G','Y'])

    #list of classes where passengers of class E can be allocated to
    classChange['E'] = st.multiselect('Proposed Class for Class E',subClassEconomy,default=['U','I','W'])


    #list of classes where passengers of class N can be allocated to
    classChange['N'] = st.multiselect('Proposed Class for Class N',subClassEconomy,default=['V','W'])

    
    #list of classes where passengers of class U can be allocated to
    classChange['U'] = st.multiselect('Proposed Class for Class U',subClassEconomy,default=['I'])
    
    
    #list of classes where passengers of class W can be allocated to
    classChange['W'] = st.multiselect('Proposed Class for Class W',subClassEconomy,default=['I'])
        
    #list of classes where passengers of class I can be allocated to
    classChange['I'] = st.multiselect('Proposed Class for Class I',subClassEconomy,default=['U','D'])
        

    
    
    
    
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