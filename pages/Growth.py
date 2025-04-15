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


## Will's original formatting:
# import pandas as pd
# import altair as alt
# import streamlit as st

# # Filter data for CMAST and DUML
# cmast_data = growth_data[growth_data['site'] == 'CMAST']
# duml_data = growth_data[growth_data['site'] == 'DUML']

# # Define the custom order for the groups
# group_order = ['50', '100', '150', '200', 'BS', 'CN', 'CS', 'SJ', 'EveryOther', 'OnceAWeek', 'TwiceAWeek']

# # Plot for CMAST
# cmast_plot = alt.Chart(cmast_data).mark_point(size=300, filled=True, opacity=1).encode(
#     x=alt.X('Group', sort=group_order),  # X-axis: Group with custom order
#     y='growth_rate',  # Y-axis: Growth rate
#     color=alt.Color('color_map', scale=None),  # Color points based on color_map column
#     tooltip=['Group', 'growth_rate', 'ci_difference']  # Tooltip to show details on hover
# ).properties(
#     title='Growth Rate by Strain and Treatment at CMAST (Combined Dot Plot)'  # Plot title
# )

# # Add error bars to the plot
# cmast_errorbars = cmast_plot.mark_errorbar(color='white').encode(
#     y='growth_rate',  # Y-axis: Growth rate
#     yError='ci_difference',  # Error bars based on ci_difference
#     color=alt.value('white')  # Error bars color
# )

# # Add horizontal line at y=0
# cmast_hline = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(strokeDash=[5, 5], color='white', strokeWidth=2).encode(
#     y='y'  # Y-axis: Horizontal line at 0
# )

# # Combine the point plot, error bars, and horizontal line
# cmast_final_plot = alt.layer(cmast_hline, cmast_errorbars, cmast_plot).configure_axis(
#     labelAngle=45  # Rotate x-axis labels for readability
# ).configure_legend(
#     orient='right'  # Place legend to the right
# ).configure_view(
#     strokeWidth=0  # Remove border around the plot
# ).configure_title(
#     fontSize=20  # Title font size
# ).configure_axis(
#     labelFontSize=12,  # Axis label font size
#     titleFontSize=14  # Axis title font size
# )

# # Plot for DUML
# duml_plot = alt.Chart(duml_data).mark_point(size=300, filled=True, opacity=1).encode(
#     x=alt.X('Group', sort=group_order),  # X-axis: Group with custom order
#     y='growth_rate',  # Y-axis: Growth rate
#     color=alt.Color('color_map', scale=None),  # Color points based on color_map column
#     tooltip=['Group', 'growth_rate', 'ci_difference']  # Tooltip to show details on hover
# ).properties(
#     title='Growth Rate by Strain and Treatment at DUML (Combined Dot Plot)'  # Plot title
# )

# # Add error bars to the plot
# duml_errorbars = duml_plot.mark_errorbar(color='white').encode(
#     y='growth_rate',  # Y-axis: Growth rate
#     yError='ci_difference',  # Error bars based on ci_difference
#     color=alt.value('white')  # Error bars color
# )

# # Add horizontal line at y=0
# duml_hline = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(strokeDash=[5, 5], color='white', strokeWidth=2).encode(
#     y='y'  # Y-axis: Horizontal line at 0
# )

# # Combine the point plot, error bars, and horizontal line
# duml_final_plot = alt.layer(duml_hline, duml_errorbars, duml_plot).configure_axis(
#     labelAngle=45  # Rotate x-axis labels for readability
# ).configure_legend(
#     orient='right'  # Place legend to the right
# ).configure_view(
#     strokeWidth=0  # Remove border around the plot
# ).configure_title(
#     fontSize=20  # Title font size
# ).configure_axis(
#     labelFontSize=12,  # Axis label font size
#     titleFontSize=14  # Axis title font size
# )

# # Display the plots in Streamlit
# st.altair_chart(cmast_final_plot, use_container_width=True)
# st.altair_chart(duml_final_plot, use_container_width=True)

# ''

## Using Anish's Formatting:

import pandas as pd
import altair as alt
import streamlit as st

# Filter data for CMAST and DUML
cmast_data = growth_data[growth_data['site'] == 'CMAST']
duml_data = growth_data[growth_data['site'] == 'DUML']

# Combine CMAST and DUML data
combined_data = pd.concat([cmast_data, duml_data])

# Define the custom order for the groups
group_order_density = ['50', '100', '150', '200']
group_order_strain = ['BS', 'CN', 'CS', 'SJ']
group_order_flipping = ['Every other week', 'Once a week', 'Twice a week']

# Define a function to create each subplot
def create_subplot(data, group_order, x_label):
    plot = alt.Chart(data).mark_point(size=300, filled=True, opacity=1).encode(
        x=alt.X('Group', sort=group_order, axis=alt.Axis(title=x_label)),  # X-axis: Group with custom order, no title
        y=alt.Y('growth_rate', axis=alt.Axis(title='Growth rate (mm/month)')),  # Y-axis: Growth rate
        color=alt.Color('site', scale=alt.Scale(domain=['CMAST', 'DUML'], range=['#DC3220', '#005AB5'])),  # Color points based on site
        tooltip=['Group', 'growth_rate', 'ci_difference']  # Tooltip to show details on hover
    )

    # Add error bars to the plot
    errorbars = plot.mark_errorbar(color='white').encode(
        y=alt.Y('growth_rate', axis=alt.Axis(title='Growth rate (mm/month)')),  # Y-axis: Growth rate
        yError='ci_difference',  # Error bars based on ci_difference
        color=alt.value('white')  # Error bars color
    )

    # Add horizontal line at y=0
    hline = alt.Chart(pd.DataFrame({'y': [0]})).mark_rule(strokeDash=[5, 5], color='white', strokeWidth=2).encode(
        y='y'  # Y-axis: Horizontal line at 0
    )

    # Combine the point plot, error bars, horizontal line, and vertical line
    final_plot = alt.layer(hline, errorbars, plot)
    
    return final_plot

# Create subplots
density_plot = create_subplot(combined_data[combined_data['Group'].isin(group_order_density)], group_order_density, 'Bag density')
strain_plot = create_subplot(combined_data[combined_data['Group'].isin(group_order_strain)], group_order_strain, 'Genetic strain')
flipping_plot = create_subplot(combined_data[combined_data['Group'].isin(group_order_flipping)], group_order_flipping, 'Flipping frequency')

# Combine subplots into a single plot
final_plot = alt.vconcat(
    density_plot.properties(title='Bag density'),
    strain_plot.properties(title='Genetic strain'),
    flipping_plot.properties(title='Flipping frequency')
).resolve_scale(
    y='shared'  # Share the y-axis scale across subplots
).configure_axis(
    labelAngle=45,  # Rotate x-axis labels for readability
    grid=False  # Remove grid lines
).configure_legend(
    orient='right'  # Place legend to the right
).configure_view(
    strokeWidth=0  # Remove border around the plot
).configure_title(
    fontSize=20  # Title font size
).configure_axis(
    labelFontSize=12,  # Axis label font size
    titleFontSize=14  # Axis title font size
).interactive()

# Display the plot in Streamlit
st.altair_chart(final_plot, use_container_width=True)


'''
Growth rates of living oysters separated by number of oysters per bag (bag density), oyster
genetic strain, and bag flipping frequency. Growth rates were obtained from the slope of linear regression of 
length measurements over time. The error bars show the 95% confidence interval of regression.
**Oysters at DUML had significantly higher growth rates than oysters at CMAST. We find no significant
differences between growth rates at an individual site based on bag density, genetic strain, or flipping frequency.**
'''
'''
CMAST = Center for Marine Sciences and Technology, North Carolina State Univeristy
\n DUML = Duke University Marine Laboratory
'''
