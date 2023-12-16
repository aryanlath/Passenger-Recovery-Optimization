import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
#from .. import stats
from stats import *
import numpy as np
import pandas as pd
# Your list of values


list1=[same_city_count[0],diff_city_count[0],total_non_assigned[0]]
# Color scheme
colors = ['#FFC154', '#EC6B56', '#47B39C']

# Create a donut chart
fig = make_subplots(rows=1, cols=1, specs=[[{'type':'pie'}]])

st.header("City Pair Distribution")
fig.add_trace(go.Pie(labels=['PNRs with same city pairs', 'PNRs with different city pairs', 'Unassigned PNRs'], values=list1, hole=0.4, marker=dict(colors=colors)), 1, 1)


# Set the background color to black
fig.update_layout(
    # paper_bgcolor='white',  # background color of the entire plot
    # plot_bgcolor='white',   # background color of the plot area
    font=dict(color='white')  # text color
)



# Add hoverinfo to display values on hover
fig.update_traces(hoverinfo='label+value', textinfo='value', textposition='inside', marker=dict(line=dict(color='black', width=2)))

# Display the chart using st.plotly_chart
st.plotly_chart(fig)

l1=[upgrade_count[0],downgrade_count[0],total_assigned[0]-downgrade_count[0]-upgrade_count[0]]
l2=[upgrade_count[1],downgrade_count[1],total_assigned[1]-downgrade_count[1]-upgrade_count[1]]
l3=[upgrade_count[2],downgrade_count[2],total_assigned[2]-downgrade_count[2]-upgrade_count[2]]

# Color scheme
colors = ['#FFC154', '#EC6B56', '#47B39C']

st.header("Class Changes for each solution")
# Create a donut chart for all three sets of values
fig = make_subplots(rows=1, cols=3, specs=[[{'type':'pie'}, {'type':'pie'}, {'type':'pie'}]],subplot_titles=('Solution 1', 'Solution 2','Solution 3'))

fig.add_trace(go.Pie(labels=['Class Upgrade', 'Class Downgrade', 'Same Class'], values=l1, hole=0.4, marker=dict(colors=colors)), 1, 1)
fig.add_trace(go.Pie(labels=['Class Upgrade', 'Class Downgrade', 'Same Class'], values=l2, hole=0.4, marker=dict(colors=colors)), 1, 2)
fig.add_trace(go.Pie(labels=['Class Upgrade', 'Class Downgrade', 'Same Class'], values=l3, hole=0.4, marker=dict(colors=colors)), 1, 3)



# Set the background color to black
fig.update_layout(
    # paper_bgcolor='white',  # background color of the entire plot
    # plot_bgcolor='white',   # background color of the plot area
    font=dict(color='white')  # text color
)


# Add hoverinfo to display values on hover
fig.update_traces(hoverinfo='label+value', textinfo='value', textposition='inside', marker=dict(line=dict(color='black', width=2)))

# Display all three charts using st.plotly_chart
st.plotly_chart(fig)

st.header("Distribution of PNR Scores")

pnr_score_assigned_dict = {
    1: pnr_score_assigned[0],
    2: pnr_score_assigned[1],
    3: pnr_score_assigned[2]
}

pnr_score_non_assigned_dict = {
    1: pnr_score_non_assigned[0],
    2: pnr_score_non_assigned[1],
    3: pnr_score_non_assigned[2]
}

colors = ['blue', 'orange']  # Assigned and Non-Assigned PNRs colors

fig = make_subplots(rows=1, cols=3, subplot_titles=("Solution 1", "Solution 2", "Solution 3"))

for i in range(1, 4):
    data = [pnr_score_assigned_dict[i], pnr_score_non_assigned_dict[i]]
    labels = ['Assigned PNRs', 'Non-Assigned PNRs']

    for j in range(len(data)):
        if i==1:
            show_legend=True
        else:
            show_legend=False
        fig.add_trace(go.Box(y=data[j], name=labels[j], marker_color=colors[j],showlegend=show_legend), row=1, col=i)

fig.update_layout(
    height=400,
    width=900
)

st.plotly_chart(fig)

# st.header("Solver Time(ms) vs Impacted PNR")



# # Sample data
# data = {
#     'Category': ['87', '518', '490', '1233'],
#     'Values': [16.03, 16.04, 21.37, 16.05]
# }

# # Create a DataFrame from the sample data
# df = pd.DataFrame(data)


# # Create a bar graph using Plotly Go
# fig = go.Figure(data=[go.Bar(
#     x=df['Category'],
#     y=df['Values'],
#     marker=dict(color='royalblue')  # Set color for bars
# )])

# fig.update_layout(
#     xaxis=dict(title='Impacted PNR'),  # X-axis label
#     yaxis=dict(title='Solver Time(ms)'),      # Y-axis label
#     plot_bgcolor='rgba(0,0,0,0)',    # Background color
#     bargap=0.1,                      # Gap between bars
# )

# # Display the bar graph in Streamlit
# st.plotly_chart(fig)

