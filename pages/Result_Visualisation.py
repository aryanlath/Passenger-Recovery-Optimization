import streamlit as st
import pandas as pd
from constants_immutable import *
from collections import defaultdict

def string_to_dict(string_dict):
    # Remove curly braces and split by commas
    pairs = string_dict[1:-1].split(', ')

    # Create a dictionary from key-value pairs
    actual_dict = {}
    for pair in pairs:
        key, value = pair.split(': ')
        actual_dict[key.strip("'")] = int(value)

    return actual_dict

def visualize_results(result):
    """
    Visualize the results of the optimization.
    """
    # Read the CSV files
    pnrs = pd.read_csv(result)

    # Display PNRs and Inventory IDs
    st.title("PNRs and Inventory IDs")
    st.write("Click on the PNR ID to display the flight details.")

    for _, pnr in pnrs.iterrows():
        with st.expander(f"PNR: {pnr['PNR_Number']}"):
            Assigned_flight = pnr['Flight']
            Cabin = pnr['Cabin']
            Class = pnr['Class']
            Cancelled_flight = pnr['Cancelled Flights']
            st.write(f"Cancelled Flights: {Cancelled_flight}")
            st.write("Flight Details: ")
            st.write(f"Assigned Flight: {Assigned_flight}")
            st.write(f"Cabin: {pnr['Cabin']}")
            st.write(f"Class: {pnr['Class']}")

if __name__ == "__main__":
    visualize_results("Results/assignments_0.csv")