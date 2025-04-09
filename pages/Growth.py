# Imports
import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

@st.cache_data

def get_survivor_data(file_name):
    """Grab survivorship data from a CSV file.

    This uses caching to avoid having to read the file every time.
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    file = pd.read_csv(file_name)
    
    return file

growth_data = get_survivor_data("data/growth_rates.csv")


'''
## :tulip: Oyster Growth

'''
''

import pandas as pd
import altair as alt
import streamlit as st

# Filter data for CMAST and DUML
cmast_data = growth_data[growth_data['site'] == 'CMAST']
duml_data = growth_data[growth_data['site'] == 'DUML']

# Define the custom order for the groups
group_order = ['100', '150', '200', 'BS', 'CN', 'CS', 'SJ', 'EveryOther', 'OnceAWeek', 'TwiceAWeek']

# Plot for CMAST
cmast_plot = alt.Chart(cmast_data).mark_point(size=100, filled=True).encode(
    x=alt.X('Group', sort=group_order),  # X-axis: Group with custom order
    y='growth_rate',  # Y-axis: Growth rate
    color=alt.Color('color_map', scale=None),  # Color points based on color_map column
    tooltip=['Group', 'growth_rate', 'ci_difference']  # Tooltip to show details on hover
).properties(
    title='Growth Rate by Strain and Treatment at CMAST (Combined Dot Plot)'  # Plot title
)

# Add error bars to the plot
cmast_errorbars = cmast_plot.mark_errorbar(color='white').encode(
    y='growth_rate',  # Y-axis: Growth rate
    yError='ci_difference',  # Error bars based on ci_difference
    color=alt.value('white')  # Error bars color
)

# Add horizontal line at y=0
cmast_hline = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(strokeDash=[5, 5], color='white', strokeWidth=2).encode(
    y='y'  # Y-axis: Horizontal line at 0
)

# Combine the point plot, error bars, and horizontal line
cmast_final_plot = alt.layer(cmast_errorbars, cmast_plot, cmast_hline).configure_axis(
    labelAngle=45  # Rotate x-axis labels for readability
).configure_legend(
    orient='right'  # Place legend to the right
).configure_view(
    strokeWidth=0  # Remove border around the plot
).configure_title(
    fontSize=20  # Title font size
).configure_axis(
    labelFontSize=12,  # Axis label font size
    titleFontSize=14  # Axis title font size
)

# Plot for DUML
duml_plot = alt.Chart(duml_data).mark_point(size=100, filled=True).encode(
    x=alt.X('Group', sort=group_order),  # X-axis: Group with custom order
    y='growth_rate',  # Y-axis: Growth rate
    color=alt.Color('color_map', scale=None),  # Color points based on color_map column
    tooltip=['Group', 'growth_rate', 'ci_difference']  # Tooltip to show details on hover
).properties(
    title='Growth Rate by Strain and Treatment at DUML (Combined Dot Plot)'  # Plot title
)

# Add error bars to the plot
duml_errorbars = duml_plot.mark_errorbar(color='white').encode(
    y='growth_rate',  # Y-axis: Growth rate
    yError='ci_difference',  # Error bars based on ci_difference
    color=alt.value('white')  # Error bars color
)

# Add horizontal line at y=0
duml_hline = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(strokeDash=[5, 5], color='white', strokeWidth=2).encode(
    y='y'  # Y-axis: Horizontal line at 0
)

# Combine the point plot, error bars, and horizontal line
duml_final_plot = alt.layer(duml_errorbars, duml_plot, duml_hline).configure_axis(
    labelAngle=45  # Rotate x-axis labels for readability
).configure_legend(
    orient='right'  # Place legend to the right
).configure_view(
    strokeWidth=0  # Remove border around the plot
).configure_title(
    fontSize=20  # Title font size
).configure_axis(
    labelFontSize=12,  # Axis label font size
    titleFontSize=14  # Axis title font size
)

# Display the plots in Streamlit
st.altair_chart(cmast_final_plot, use_container_width=True)
st.altair_chart(duml_final_plot, use_container_width=True)

growth_data

'''
Percent of oysters surviving in each bag, measured bimonthly (transparent points) and the 
average survivorship at each site (opaque points; error bars show ± standard deviation). 
**More mortality was observed at CMAST than DUML, particularly during and after August, but overall, 
mass mortality was not observed.**
'''
'''
CMAST = Center for Marine Sciences and Technology, North Carolina State Univeristy
\n DUML = Duke University Marine Laboratory
'''
