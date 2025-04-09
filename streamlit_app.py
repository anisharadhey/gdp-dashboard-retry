# Imports
import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Climate Change Impacts on Farmed and Wild Oysters',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

@st.cache_data

def read_data(filename):
    """Grab temperature data from a CSV file.

    This uses caching to avoid having to read the file every time.
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    # DATA_FILENAME = Path(__file__).parent/'data/'
    path = 'data/'
    temp_df = pd.read_csv(path + filename)

    # Convert times from string to datetime objects
    temp_df['Time'] = pd.to_datetime(temp_df['Time'], format = 'mixed')
    
    # Make colymns for month, day and time
    # temp_df['Month'] = [dt.month for dt in temp_df['Time']]
    # temp_df['Day'] = [dt.day for dt in temp_df['Time']]
    # temp_df['Hour'] = [dt.hour for dt in temp_df['Time']]

    # Get only rows for data in May
    # temp_df = temp_df[(temp_df['Month'] == 5)]

    # Get only rows for May 14
    # temp_df = temp_df[(temp_df['Day'] == 14)]

    return temp_df

# gdp_df = get_gdp_data()
temp_df = read_data('AverageCMASTtemp.csv')

# temp_df

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: Climate Change Impacts on Farmed and Wild Oysters

Explore our data using the tabs on the left.
'''

''

# # Make a slider based on times
# min_time = temp_df['Time'].min().to_pydatetime()
# max_time = temp_df['Time'].max().to_pydatetime()

# from_time, to_time = st.slider(
#     'Which hours are you interested in?',
#     min_value = min_time,
#     max_value = max_time,
#     value=[min_time, max_time],
#     key = 2)

# ''

# sensors = temp_df['Location'].unique()

# if not len(sensors):
#     st.warning("Select at least one sensor")

# selected_sensors = st.multiselect(
#     'Which sensors would you like to view?',
#     sensors,
#     ['Array', 'Line 1A', 'Line 1B'],
#     key = 3
#     )

# ''

# # Filter the data
# filtered_temp_df = temp_df[
#     (temp_df['Location'].isin(selected_sensors))
#     & (temp_df['Time'] <= to_time)
#     & (from_time <= temp_df['Time'])
# ]

# st.header('Water temperature over time', divider='gray')

# ''

# st.line_chart(
#     filtered_temp_df,
#     x='Time',
#     y='TempC',
#     color='Location',
# )
