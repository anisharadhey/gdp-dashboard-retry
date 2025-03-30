# Imports
import streamlit as st
import pandas as pd
import math
from pathlib import Path

@st.cache_data

def get_survivor_data():
    """Grab survivorship data from a CSV file.

    This uses caching to avoid having to read the file every time.
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = 'data/OysterMortalityData_Processed.csv'
    surv_df = pd.read_csv(DATA_FILENAME)

    # Remove empty columns and rows from the read-in CSV file
    surv_df = surv_df.dropna(axis = 1, how = 'all').dropna(axis = 0, how = 'all')

    # Convert times from string to datetime objects
    surv_df['Date'] = pd.to_datetime(surv_df['Date'], format='%m/%d/%y')
    
    return surv_df

# gdp_df = get_gdp_data()
surv_df = get_survivor_data()

# Looks great!
# surv_df

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :oyster: Survivorship dashboard

Browse water oyster survivorship curves from CMAST and DUML oyster farms between May and October 2024.
'''

''

# Make a slider based on times
min_time = surv_df['Date'].min().to_pydatetime()
max_time = surv_df['Date'].max().to_pydatetime()

from_time, to_time = st.slider(
    'Which days are you interested in?',
    min_value = min_time,
    max_value = max_time,
    value=[min_time, max_time],
    key = 2)

''

strains = surv_df['Strain'].unique()

if not len(strains):
    st.warning("Select at least one genetic strain")

selected_strains = st.multiselect(
    'Which genetic strains would you like to view?',
    strains,
   ['CS', 'SJ'],
    key = 3
    )

# Filter the data
filtered_surv_df = surv_df[
    (surv_df['Strain'].isin(selected_strains))
    & (surv_df['Date'] <= to_time)
    & (from_time <= surv_df['Date'])
]

# Set up to columns for displaying line graphs
col1, col2 = st.columns([0.5, 0.5])

#SELECTION 1 COLUMN
with col1:

    st.header('Survivorship fraction at DUML', divider='gray')

    ''

    # Get just DUML data
    DUML_data = filtered_surv_df[(filtered_surv_df['Site'] == 'DUML')]

    # DUML_data

    st.line_chart(
        DUML_data,
        x = 'Date',
        y = 'Survivorship_ActualStartingDensityBase_PreventFranken',
        color = 'BagNumber',
        y_label = 'Survivorship fraction'
        )
   

#SELECTION 2 COLUMN
with col2:

    st.header('Survivorship fraction at CMAST', divider='gray')

    ''

    # Get just CMAST data
    CMAST_data = filtered_surv_df[(filtered_surv_df['Site'] == 'CMAST')]
    
    # CMAST_data

    st.line_chart(
        CMAST_data,
        x = 'Date',
        y = 'Survivorship_ActualStartingDensityBase_PreventFranken',
        color = 'BagNumber',
        y_label = 'Survivorship fraction'
        )