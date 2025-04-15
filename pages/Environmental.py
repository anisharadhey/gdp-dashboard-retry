# Imports
import streamlit as st
import pandas as pd
import math
from pathlib import Path
import altair as alt

@st.cache_data

def read_data(filename):
    """Grab temperature data from a CSV file.

    This uses caching to avoid having to read the file every time.
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    # DATA_FILENAME = Path(__file__).parent/'data/'
    path = 'data/'
    temp_df = pd.read_csv(path + filename)

    return temp_df


'''
## :ocean: Environmental Conditions

'''
''

# ---- Begin prototype ---- 

import pandas as pd
import altair as alt
import streamlit as st

df_daily = read_data('environmental_data_daily.csv')
df_hourly = read_data('environmental_data_hourly.csv')
df_5min = read_data('environmental_data_5minute.csv')

# Function to create the plot
def create_plot(df, selected_types):
    # Multiply all precipitation accumulation values by 70/40
    df.loc[df['Type'] == 'Precipitation Accumulation (mm)', 'Measurement'] *= (70 / 40)

    # Create a new column that concatenates the values in the Site and Type columns without a space
    df['Site_Type'] = df['Site'].fillna('') + " " + df['Type']

    # Rename the 'rounded_time' column to 'Time'
    df.rename(columns={'rounded_time': 'Time'}, inplace=True)

    # Define the color palette
    color_palette = {
        "DUML Salinity (ppt)": "#729ECEFF", 
        "CMAST Salinity (ppt)": "#ED665DFF", 
        "DUML Temperature (C)": "#67BF5CFF", 
        "CMAST Temperature (C)": "#ED97CAFF", 
        "DUML pH": "#AD8BC9FF", 
        "CMAST pH": "#CDCC5DFF", 
        "DUML DO (mg/L)": "#A8786EFF", 
        "CMAST DO (mg/L)": "#FF9E4AFF", 
        " Precipitation Accumulation (mm)": "#6DCCDAFF"
    }

    # Filter the dataframe based on selected types
    df_filtered = df[df['Type'].isin(selected_types)]

    # Create the base chart
    base = alt.Chart(df_filtered).encode(
        x='Time:T',
        color=alt.Color('Site_Type:N', scale=alt.Scale(domain=list(color_palette.keys()), range=list(color_palette.values())))
    )

    # Create the line chart for Precipitation Accumulation
    precip_line = base.mark_line(size=2).encode(
        y=alt.Y('Measurement:Q', axis=alt.Axis(title='Precipitation Accumulation (mm)', 
                                               values=[0, 10, 20, 30, 40, 50, 60, 70])),
        tooltip=['Time:T', 'Measurement:Q', 'Type:N', 'Site:N', 'Site_Type:N']
    ).transform_filter(
        (alt.datum.Type == 'Precipitation Accumulation (mm)')
    )

    # Create the line chart for other measurements
    other_lines = base.mark_line(size=2).encode(
        y=alt.Y('Measurement:Q', axis=alt.Axis(title='Salinity (ppt), Temp (°C), pH, DO (mg/L)')),
        tooltip=['Time:T', 'Measurement:Q', 'Type:N', 'Site:N', 'Site_Type:N']
    ).transform_filter(
        (alt.datum.Type != 'Precipitation Accumulation (mm)')
    )

    # Create a secondary axis for Precipitation Accumulation
    precip_axis = base.mark_line(size=2).encode(
        y=alt.Y('Measurement:Q', axis=alt.Axis(title='Precipitation Accumulation (mm)', 
                                               orient='right')),
        tooltip=['Time:T', 'Measurement:Q', 'Type:N', 'Site:N', 'Site_Type:N']
    ).transform_filter(
        (alt.datum.Type == 'Precipitation Accumulation (mm)')
    )

    # Combine the plots
    final_plot = alt.layer(other_lines, precip_axis).resolve_scale(
        y='independent'
    ).properties(
        height=600  # Make the plot taller
    ).interactive()

    return final_plot

# Implement an interactive button/slider in Streamlit to allow users to select the data resolution
resolution = st.selectbox('Select data resolution:', ['Daily', 'Hourly', '5 minutes'])

if resolution == 'Daily':
    df_selected = df_daily
elif resolution == 'Hourly':
    df_selected = df_hourly
else:
    df_selected = df_5min

# Get unique types from the dataframe for multiselect options
unique_types = df_selected['Type'].unique()

# Implement an interactive multiselect option to allow users to select which types of data to display on the graph
selected_types = st.multiselect('Select data types to display:', unique_types, default=unique_types)

# Create and display the plot in Streamlit with updated data and selected types
final_plot = create_plot(df_selected, selected_types)
st.altair_chart(final_plot, use_container_width=True)

'''
Graph of environmental parameters across entire experiment duration. 
**All environmental variables differed significantly between the two experimental sites (p < 0.01).** Data with 
daily resolution shows measurements from 12:05 PM each day. Data with hourly resolution shows measurements from 5 
minutes after the hour.
'''
'''
CMAST = Center for Marine Sciences and Technology, North Carolina State University
\nDUML = Duke University Marine Laboratory
\nDO = Dissolved Oxygen
'''