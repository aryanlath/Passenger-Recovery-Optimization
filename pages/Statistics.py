import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.offline import plot
#from .. import stats
from stats import *
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
    paper_bgcolor='black',  # background color of the entire plot
    plot_bgcolor='black',   # background color of the plot area
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
    paper_bgcolor='black',  # background color of the entire plot
    plot_bgcolor='black',   # background color of the plot area
    font=dict(color='white')  # text color
)


# Add hoverinfo to display values on hover
fig.update_traces(hoverinfo='label+value', textinfo='value', textposition='inside', marker=dict(line=dict(color='black', width=2)))

# Display all three charts using st.plotly_chart
st.plotly_chart(fig)