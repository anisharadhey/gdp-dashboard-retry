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


# ---- Begin prototype ---- 

# Read data
combined_df = read_data('environmental_data_daily.csv')

import altair as alt
import streamlit as st

# Create the base chart
base = alt.Chart(combined_df).encode(
    x='rounded_time:T',
    color='Type:N'
)

# Create the line chart for Precipitation Accumulation
precip_line = base.mark_line(size=2).encode(
    y=alt.Y('Measurement:Q', axis=alt.Axis(title='Precipitation Accumulation (mm)', 
                                           values=[0, 10, 20, 30, 40, 50, 60, 70])),
    tooltip=['rounded_time:T', 'Measurement:Q', 'Type:N']
).transform_filter(
    alt.datum.Type == 'Precipitation Accum'
)

# Create the line chart for other measurements
other_lines = base.mark_line(size=2).encode(
    y=alt.Y('Measurement:Q', axis=alt.Axis(title='Salinity (ppt), Temp (°C), pH, DO (mg/L)')),
    tooltip=['rounded_time:T', 'Measurement:Q', 'Type:N']
).transform_filter(
    alt.datum.Type != 'Precipitation Accum'
)

# Create a secondary axis for Precipitation Accumulation
precip_axis = base.mark_line(size=2).encode(
    y=alt.Y('Measurement:Q', axis=alt.Axis(title='Precipitation Accumulation (mm)', 
                                           # values=[0, 10, 20, 30, 40, 50, 60, 70], 
                                           orient='right')),
    tooltip=['rounded_time:T', 'Measurement:Q', 'Type:N']
).transform_filter(
    alt.datum.Type == 'Precipitation Accum'
)

# Combine the plots
final_plot = alt.layer(other_lines, precip_axis).resolve_scale(
    y='independent'
).properties(
    title='Full Summer 2024 Environmental Data',
    height=600  # Make the plot taller
)

# Display the plot in Streamlit
st.altair_chart(final_plot, use_container_width=True)





import pandas as pd
import altair as alt
import streamlit as st

# Create a new column that concatenates the values in the Site and Type columns without a space
combined_df['Site_Type'] = combined_df['Site'] + " " + combined_df['Type']

# Create the base chart
base = alt.Chart(combined_df).encode(
    x='rounded_time:T',
    color='Site_Type:N'
)

# Create the line chart for Precipitation Accumulation
precip_line = base.mark_line(size=2).encode(
    y=alt.Y('Measurement:Q', axis=alt.Axis(title='Precipitation Accumulation (mm)', 
                                           values=[0, 10, 20, 30, 40, 50, 60, 70])),
    tooltip=['rounded_time:T', 'Measurement:Q', 'Type:N', 'Site:N', 'Site_Type:N']
).transform_filter(
    (alt.datum.Type == 'Precipitation Accum')
)

# Create the line chart for other measurements
other_lines = base.mark_line(size=2).encode(
    y=alt.Y('Measurement:Q', axis=alt.Axis(title='Salinity (ppt), Temp (°C), pH, DO (mg/L)')),
    tooltip=['rounded_time:T', 'Measurement:Q', 'Type:N', 'Site:N', 'Site_Type:N']
).transform_filter(
    (alt.datum.Type != 'Precipitation Accum')
)

# Create a secondary axis for Precipitation Accumulation
precip_axis = base.mark_line(size=2).encode(
    y=alt.Y('Measurement:Q', axis=alt.Axis(title='Precipitation Accumulation (mm)', 
                                           orient='right')),
    tooltip=['rounded_time:T', 'Measurement:Q', 'Type:N', 'Site:N', 'Site_Type:N']
).transform_filter(
    (alt.datum.Type == 'Precipitation Accum')
)

# Combine the plots
final_plot = alt.layer(other_lines, precip_axis).resolve_scale(
    y='independent'
).properties(
    title='Full Summer 2024 Environmental Data',
    height=600  # Make the plot taller
)

# Display the plot in Streamlit
st.altair_chart(final_plot, use_container_width=True)