import streamlit as st
import json
from constants_immutable import all_flights

# Function to parse and organize data
def parse_data(data):
    organized_data = {}
    for pnr, details in data.items():
        organized_data[pnr] = {
            'Original': details['Original'],
            'Proposed': details['Proposed'],
            'Email': details['Email']
        }
    return organized_data

# Function to format cabin information
def format_cabins(cabin_list):
    return ', '.join(cabin_list)  # Adjust formatting as needed


def display_data():
    # Parse the data
    with open('result_quantum_2.json', 'r') as file:
        data = json.load(file)
    if len(data)==0 or len(all_flights)==0:
        st.info('Run the code to get the Solution!', icon="🚨")

    else:
        organized_data = parse_data(data)

        # Streamlit app
        st.title(f'Solution File - 3')
        st.write("This displays the third quantum solution generated")

        # PNR selection
        selected_pnr = st.selectbox('Select a PNR:', list(organized_data.keys()))

        # Display details
        if selected_pnr:
            st.write(f"Email: {organized_data[selected_pnr]['Email']}")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader('Original Flights')
                for flight in organized_data[selected_pnr]['Original']:
                    st.markdown(f"**Inventory ID:** {flight[0]}")
                    st.markdown(f"**Cabin:** {flight[1]}")
                    st.markdown(f"**PAX Classes:** {format_cabins(flight[2])}")
                    st.markdown(f"**Departure Time:** {flight[3]}")
                    st.markdown(f"**Arrival Time:** {flight[4]}")
                    st.markdown(f"**Departure Airport:** {all_flights[flight[0]].departure_city}")
                    st.markdown(f"**Arrival Airport:** {all_flights[flight[0]].arrival_city}")
                    st.markdown("---")
            with col2:
                st.subheader('Proposed Flights')
                for flight in organized_data[selected_pnr]['Proposed']:
                    st.markdown(f"**Inventory ID:** {flight[0]}")
                    st.markdown(f"**Cabin:** {flight[1]}")
                    st.markdown(f"**PAX Classes:** {format_cabins(flight[2])}")
                    st.markdown(f"**Departure Time:** {flight[3]}")
                    st.markdown(f"**Arrival Time:** {flight[4]}")
                    st.markdown(f"**Departure Airport:** {all_flights[flight[0]].departure_city}")
                    st.markdown(f"**Arrival Airport:** {all_flights[flight[0]].arrival_city}")
                    st.markdown("---")




display_data()