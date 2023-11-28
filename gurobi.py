import gurobipy as gp
from gurobipy import GRB
import pandas as pd
from datetime import datetime
env = gp.Env(params=params)
#gp.setParam("LicenseFile", "/gurobi.lic")
# Function to calculate PNR ranking based on ruleset
def calculate_pnr_ranking(row):
    score = 0
    if row['Cabin'] == 'F':
        score += 1500
    else:
        score += 500
    if row['Special Requirements']:
        score += 200

    score += row['PAX'] * 50

    if row['Passenger Loyalty'] == "Platinum":
        score += 500
    elif row['Passenger Loyalty'] == "Gold":
        score += 300
    elif row['Passenger Loyalty'] == "Silver":
        score += 200

    return score

# Function to calculate flight quality score
def calculate_flight_quality_score(flight_row, pnr_row):
    score = 0
    init_flight = pnr_row['Flight Number']
    fin_flight = flight_row.name

    init_arr = flight_schedule_df['Arrival Time'][flight_schedule_df['Flight Number'] == init_flight].iloc[0]
    fin_arr = flight_schedule_df['Arrival Time'][flight_schedule_df['Flight Number'] == fin_flight].iloc[0]
    start_time = datetime.strptime(init_arr, '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(fin_arr, '%Y-%m-%d %H:%M')
    arr_delay = abs(start_time - end_time).total_seconds() / 3600
    if arr_delay <= 6:
        score += 70
    elif arr_delay <= 12:
        score += 50
    elif arr_delay <= 24:
        score += 40
    elif arr_delay <= 48:
        score += 30

    init_arr_city = flight_schedule_df['Arrival City'][flight_schedule_df['Flight Number'] == init_flight].iloc[0]
    fin_arr_city = flight_schedule_df['Arrival City'][flight_schedule_df['Flight Number'] == fin_flight].iloc[0]

    init_dep_city = flight_schedule_df['Departure City'][flight_schedule_df['Flight Number'] == init_flight].iloc[0]
    fin_dep_city = flight_schedule_df['Departure City'][flight_schedule_df['Flight Number'] == fin_flight].iloc[0]

    if init_arr_city == fin_arr_city and init_dep_city == fin_dep_city:
        score += 70
    elif init_arr_city == fin_arr_city or init_dep_city == fin_dep_city:
        score += 40
    else:
        score += 10

    init_dep = flight_schedule_df['Departure Time'][flight_schedule_df['Flight Number'] == init_flight].iloc[0]
    fin_dep = flight_schedule_df['Departure Time'][flight_schedule_df['Flight Number'] == fin_flight].iloc[0]
    start_time = datetime.strptime(init_dep, '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(fin_dep, '%Y-%m-%d %H:%M')

    dep_delay = abs(start_time - end_time).total_seconds() / 3600

    if dep_delay <= 6:
        score += 70
    elif dep_delay <= 12:
        score += 50
    elif dep_delay <= 24:
        score += 40
    elif dep_delay <= 48:
        score += 30

    init_arr = flight_schedule_df['Arrival Time'][flight_schedule_df['Flight Number'] == init_flight].iloc[0]
    fin_arr = flight_schedule_df['Arrival Time'][flight_schedule_df['Flight Number'] == fin_flight].iloc[0]
    start_time = datetime.strptime(init_arr, '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(fin_arr, '%Y-%m-%d %H:%M')

    arr_delay = abs(start_time - end_time).total_seconds() / 3600

    if arr_delay <= 6:
        score += 70
    elif arr_delay <= 12:
        score += 50
    elif arr_delay <= 24:
        score += 40
    elif arr_delay <= 48:
        score += 30

    if pnr_row['Cabin']=='A':
      if pnr_row['PAX']<=flight_row['Remaining Capacity A']:
        score+=50
    if pnr_row['Cabin'] == 'F':
      if pnr_row['PAX']<=flight_row['Remaining Capacity F']:
        score+=50
    if flight_row['Status'] == 'Cancelled':
      score=-99999
    return score

flight_schedule_df = pd.read_csv('/content/sample_data/flight_schedule_dataset.csv')
passenger_pnr_df = pd.read_csv('/content/sample_data/passenger_pnr_dataset.csv')

# Apply the scoring functions
passenger_pnr_df['PNR_Ranking'] = passenger_pnr_df.apply(calculate_pnr_ranking, axis=1)


# Create the Gurobi model
model = gp.Model(env=env)

# Decision variables: Assign passengers to alternative flights
assign_vars = {}
for pnr in passenger_pnr_df['PNR Number']:
    for flight in flight_schedule_df['Flight Number']:
        assign_vars[pnr, flight] = model.addVar(vtype=GRB.BINARY, name=f"Assign_{pnr}_{flight}")


# Objective Function
# Maximize the total score of reassigned passengers considering PNR ranking and flight quality score
model.setObjective(
    gp.quicksum(assign_vars[pnr, flight] * passenger_pnr_df.set_index('PNR Number').loc[pnr, 'PNR_Ranking'] *calculate_flight_quality_score(flight_schedule_df.set_index('Flight Number').loc[flight],
                                               passenger_pnr_df.set_index('PNR Number').loc[pnr])
                for pnr in passenger_pnr_df['PNR Number']
                for flight in flight_schedule_df['Flight Number']),
    sense=GRB.MAXIMIZE
)

# Constraints
# Each passenger can be assigned to at most one flight
for pnr in passenger_pnr_df['PNR Number']:
    model.addConstr(gp.quicksum(assign_vars[pnr, flight] for flight in flight_schedule_df['Flight Number']) <= 1,
                    f"assign_{pnr}")

# Capacity constraints for each flight
for flight in flight_schedule_df['Flight Number']:
    model.addConstr(
        gp.quicksum(assign_vars[pnr, flight] * passenger_pnr_df.set_index('PNR Number').loc[pnr, 'PAX']
                    for pnr in passenger_pnr_df['PNR Number']) <=
        flight_schedule_df.set_index('Flight Number').loc[flight, 'Remaining Capacity A'] +
        flight_schedule_df.set_index('Flight Number').loc[flight, 'Remaining Capacity F'],
        f"capacity_{flight}"
    )

# Solve the model
model.optimize()

# Output results
reassignment_results = [(pnr, flight) for pnr in passenger_pnr_df['PNR Number']
                        for flight in flight_schedule_df['Flight Number'] if assign_vars[pnr, flight].x > 0.5]

reassignment_results
