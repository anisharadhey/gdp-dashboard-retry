# Imports
import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

@st.cache_data

def get_survivor_data():
    """Grab survivorship data from a CSV file.

    This uses caching to avoid having to read the file every time.
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    surv_df = pd.read_csv('data/MortalityBySiteBinned.csv')

    # Convert times from string to datetime objects
    surv_df['Date'] = pd.to_datetime(surv_df['Date'], format='mixed')

     # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    continuous = pd.read_csv('data/MortalityContinuous.csv')

    # Convert times from string to datetime objects
    continuous['Date'] = pd.to_datetime(continuous['Date'], format='mixed')
    
    return surv_df, continuous

# gdp_df = get_gdp_data()
surv_df = get_survivor_data()

# Looks great!
# surv_df[0]

# surv_df[1]

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
## :oyster: Oyster Mortality

'''
''

# # Make a slider based on times
# min_time = surv_df['Date'].min().to_pydatetime()
# max_time = surv_df['Date'].max().to_pydatetime()

# from_time, to_time = st.slider(
#     'Which days are you interested in?',
#     min_value = min_time,
#     max_value = max_time,
#     value=[min_time, max_time],
#     key = 2)

# ''

# strains = surv_df['Strain'].unique()

# if not len(strains):
#     st.warning("Select at least one genetic strain")

# selected_strains = st.multiselect(
#     'Which genetic strains would you like to view?',
#     strains,
#    ['CS', 'SJ'],
#     key = 3
#     )

# # Filter the data
# filtered_surv_df = surv_df[
#     (surv_df['Strain'].isin(selected_strains))
#     & (surv_df['Date'] <= to_time)
#     & (from_time <= surv_df['Date'])
# ]

# # Set up to columns for displaying line graphs
# col1, col2 = st.columns([0.5, 0.5])

filtered_df = surv_df[0]
MortalityContinuous = surv_df[1]

import streamlit as st
import altair as alt

# Define custom color scale
color_scale = alt.Scale(
    domain=['CMAST', 'DUML'],
    range=['#DC3220', '#005AB5']  # Using color-blind friendly red-blue constrast from: https://davidmathlogic.com/colorblind/#%23005AB5-%23DC3220
)

# Create the base chart for the first dataframe
base = alt.Chart(filtered_df).encode(
    x=alt.X('Date:T', axis=alt.Axis(title='Date')),  # Add x-axis label
    y=alt.Y('Survivorship_StartingDensityBase_Impute100_Percent:Q', scale=alt.Scale(domain=[48, 102]), axis=alt.Axis(title='Survivorship per bag (%)')),  # Add y-axis label
    color=alt.Color('Site:N', scale=color_scale, legend=alt.Legend(title="Site", orient='bottom')),
    tooltip=[alt.Tooltip('Date:T', title='Date'), 
             alt.Tooltip('Site:N', title='Site'), 
             alt.Tooltip('Survivorship_StartingDensityBase_Impute100_Percent:Q', title='Mean % Survivorship', format='.1f'), 
             alt.Tooltip('sd:Q', title='Error (SD)', format='.1f')]  # Custom tooltip for solid points
).mark_point(
    filled=True,
    size=300,  # Update point size to 300
    opacity=1  # Set opacity to 100%
)

# Create the error bars for the first dataframe with custom tooltip
error_bars = alt.Chart(filtered_df).transform_calculate(
    mean_value='datum.Survivorship_StartingDensityBase_Impute100_Percent',
    mean_plus_sd='datum.Survivorship_StartingDensityBase_Impute100_Percent + datum.sd',
    mean_minus_sd='datum.Survivorship_StartingDensityBase_Impute100_Percent - datum.sd'
).mark_errorbar(
    size=10,  # Increase the width of the error bars
    opacity=1  # Set opacity to 100%
).encode(
    x='Date:T',
    y=alt.Y('Survivorship_StartingDensityBase_Impute100_Percent:Q', scale=alt.Scale(domain=[55, 100]), axis=alt.Axis(title='Survivorship per bag (%)')),  # Add y-axis label
    yError='sd:Q',
    color=alt.Color('Site:N', scale=color_scale),  # Match color of error bars to points
    tooltip=[alt.Tooltip('Date:T', title='Date'),
        alt.Tooltip('mean_value:Q', title='Mean Value', format='.1f'),
             alt.Tooltip('mean_plus_sd:Q', title='Mean + SD', format='.1f'),
             alt.Tooltip('mean_minus_sd:Q', title='Mean - SD', format='.1f')]  # Custom tooltip for error bars
)

# Create the scatter points for the second dataframe
mortality_points = alt.Chart(MortalityContinuous).encode(
    x='Date:T',
    y=alt.Y('Survivorship_StartingDensityBase_Impute100_Percent:Q', scale=alt.Scale(domain=[55, 100]), axis=alt.Axis(title='Survivorship per bag (%)')),  # Add y-axis label
    color=alt.Color('Site:N', scale=color_scale),  # Use the same color scale
    tooltip=[alt.Tooltip('Date:T', title='Date'), 
             alt.Tooltip('Site:N', title='Site'), 
             alt.Tooltip('Survivorship_StartingDensityBase_Impute100_Percent:Q', title='% Survivorship')]  # Custom tooltip for faint points
).mark_point(
    filled=True,
    size=200,  # Set point size to 300
    opacity=0.15  # Set slightly higher opacity for the second dataframe points
)

# Layer the points and error bars
# chart = alt.layer(base, error_bars, mortality_points).properties(
chart = alt.layer(base, mortality_points, error_bars, base).properties(
    width=1000,
    height=600
).interactive()

# Display the chart in Streamlit
st.altair_chart(chart, use_container_width=True)
   
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

# #SELECTION 2 COLUMN
# with col2:

#     st.header('Survivorship fraction at CMAST', divider='gray')

#     ''

#     # Get just CMAST data
#     CMAST_data = filtered_surv_df[(filtered_surv_df['Site'] == 'CMAST')]
    
#     # CMAST_data

#     st.line_chart(
#         CMAST_data,
#         x = 'Date',
#         y = 'Survivorship_ActualStartingDensityBase_PreventFranken',
#         color = 'BagNumber',
#         y_label = 'Survivorship fraction'
#         )