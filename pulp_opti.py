import pandas as pd
import pulp
from datetime import datetime



# Function to calculate PNR ranking based on ruleset
def calculate_pnr_ranking(row):
    # Simplified scoring based on cabin class and special requirements
    score = 0
    if row['Cabin']=='F':
      score+=1500
    else:
      score +=500
    if row['Special Requirements']:
        score += 200

    score+=row['PAX']*50

    if row['Passenger Loyalty']:
      score+= 200

    return score

# Function to calculate flight quality score
def calculate_flight_quality_score(flight_row, pnr_row):
    # # Simplified scoring based on remaining capacity and flight status
    # score = flight_row['Remaining Capacity A'] + flight_row['Remaining Capacity F']
    # if flight_row['Status'] == 'On Time':
    #     score += 100  # Bonus points for on-time flights


    score = 0
    init_flight = pnr_row['Flight Number']
    fin_flight = flight_row.name

    init_arr = flight_schedule_df['Arrival Time'][flight_schedule_df['Flight Number']==init_flight].iloc[0]
    fin_arr =  flight_schedule_df['Arrival Time'][flight_schedule_df['Flight Number']==fin_flight].iloc[0]
    start_time = datetime.strptime(init_arr, '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(fin_arr, '%Y-%m-%d %H:%M')  
    arr_delay = abs(start_time - end_time).total_seconds()/3600
    if arr_delay<=6:
      score+=70
    elif arr_delay<=12:
      score+=50
    elif arr_delay<=24:
      score+=40
    elif arr_delay<=48:
      score+=30

    init_arr_city = flight_schedule_df['Arrival City'][flight_schedule_df['Flight Number']==init_flight].iloc[0]
    fin_arr_city = flight_schedule_df['Arrival City'][flight_schedule_df['Flight Number']==fin_flight].iloc[0]

    init_dep_city = flight_schedule_df['Departure City'][flight_schedule_df['Flight Number']==init_flight].iloc[0]
    fin_dep_city = flight_schedule_df['Departure City'][flight_schedule_df['Flight Number']==fin_flight].iloc[0]

    if init_arr_city==fin_arr_city and init_dep_city==fin_dep_city:
      score+=70
    else:
      score+=10

    init_dep = flight_schedule_df['Departure Time'][flight_schedule_df['Flight Number']==init_flight].iloc[0]
    fin_dep =  flight_schedule_df['Departure Time'][flight_schedule_df['Flight Number']==fin_flight].iloc[0]
    start_time = datetime.strptime(init_dep, '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(fin_dep, '%Y-%m-%d %H:%M') 

    dep_delay = abs(start_time - end_time).total_seconds()/3600

    if dep_delay<=6:
      score+=70
    elif dep_delay<=12:
      score+=50
    elif dep_delay<=24:
      score+=40
    elif dep_delay<=48:
      score+=30
    return score
# # Read the datasets
# flight_schedule_df = pd.read_csv('/mnt/data/flight_schedule_dataset.csv')
# passenger_pnr_df = pd.read_csv('/mnt/data/passenger_pnr_dataset.csv')

# Apply the scoring functions
passenger_pnr_df['PNR_Ranking'] = passenger_pnr_df.apply(calculate_pnr_ranking, axis=1)

# Create the PuLP optimization model
model = pulp.LpProblem("Passenger_Recovery", pulp.LpMaximize)

# Decision variables: Assign passengers to alternative flights
assign_vars = pulp.LpVariable.dicts("Assign",
                                    [(pnr, flight) for pnr in passenger_pnr_df['PNR Number']
                                     for flight in flight_schedule_df['Flight Number']],
                                    cat='Binary')

# Objective Function
# Maximize the total score of reassigned passengers considering PNR ranking and flight quality score
model += pulp.lpSum([assign_vars[pnr, flight] * passenger_pnr_df.set_index('PNR Number').loc[pnr, 'PNR_Ranking'] * 
                     calculate_flight_quality_score(flight_schedule_df.set_index('Flight Number').loc[flight], 
                                                    passenger_pnr_df.set_index('PNR Number').loc[pnr])
                     for pnr in passenger_pnr_df['PNR Number']
                     for flight in flight_schedule_df['Flight Number']])

# Constraints
# Each passenger can be assigned to at most one flight
for pnr in passenger_pnr_df['PNR Number']:
    model += pulp.lpSum([assign_vars[pnr, flight] for flight in flight_schedule_df['Flight Number']]) <= 1

# Capacity constraints for each flight
for flight in flight_schedule_df['Flight Number']:
    model += pulp.lpSum([assign_vars[pnr, flight] * passenger_pnr_df.set_index('PNR Number').loc[pnr, 'PAX']
                         for pnr in passenger_pnr_df['PNR Number']]) <= \
             flight_schedule_df.set_index('Flight Number').loc[flight, 'Remaining Capacity A'] + \
             flight_schedule_df.set_index('Flight Number').loc[flight, 'Remaining Capacity F']

# Solve the model
model.solve()

# Output results
reassignment_results = []
for var in assign_vars:
    if assign_vars[var].varValue > 0:
        reassignment_results.append((var, assign_vars[var].varValue))

reassignment_results

