# # Imports
# import streamlit as st
# import pandas as pd
# import math
# from pathlib import Path
# import altair as alt

# @st.cache_data

# def read_data(filename):
#     """Grab temperature data from a CSV file.

#     This uses caching to avoid having to read the file every time.
#     """

#     # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
#     # DATA_FILENAME = Path(__file__).parent/'data/'
#     path = 'data/'
#     temp_df = pd.read_csv(path + filename)

#     # Convert times from string to datetime objects
#     temp_df['Time'] = pd.to_datetime(temp_df['Time'], format = 'mixed')

#     return temp_df


# # ---- Begin prototype ---- 

# # Read data
# df_CMAST = read_data('AverageCMASTtemp.csv')
# df_DUML = read_data('AverageDUMLtemp.csv')

# # Filter and select relevant columns
# df_CMAST = df_CMAST[df_CMAST['Location'] == 'Array'][['Time', 'DOmgL', 'TempC', 'Site']]
# df_DUML = df_DUML[df_DUML['Location'] == 'Array'][['Time', 'DOmgL', 'TempC', 'Site']]

# # Split the files into DO and Temp, and then concatenate! Make a column that tracks the 
# # measurement type, then rename all measurements into a single column name and concatenate!
# temp_CMAST = df_CMAST[['Time', 'TempC', 'Site']].rename(columns={'TempC': 'Value'})
# temp_CMAST['Measurement'] = 'Temperature (°C)'

# do_CMAST = df_CMAST[['Time', 'DOmgL', 'Site']].rename(columns={'DOmgL': 'Value'})
# do_CMAST['Measurement'] = 'DO (mg/L)'

# temp_DUML = df_DUML[['Time', 'TempC', 'Site']].rename(columns={'TempC': 'Value'})
# temp_DUML['Measurement'] = 'Temperature (°C)'

# do_DUML = df_DUML[['Time', 'DOmgL', 'Site']].rename(columns={'DOmgL': 'Value'})
# do_DUML['Measurement'] = 'DO (mg/L)'

# # Combine dataframes
# df = pd.concat([do_CMAST, do_DUML, temp_CMAST, temp_DUML])

# # Ensure 'Time' column is in datetime format
# df['Time'] = pd.to_datetime(df['Time'])

# # Create a combined column for Site and Measurement
# df['Site_Measurement'] = df['Site'] + ' ' + df['Measurement']

# # Define custom color scale
# color_scale = alt.Scale(
#     domain=['CMAST Temperature (°C)', 'CMAST DO (mg/L)', 'DUML Temperature (°C)', 'DUML DO (mg/L)'],
#     range=['red', 'pink', 'blue', 'lightblue']
# )

# # Streamlit widgets for user input
# st.sidebar.header('Filter Data')
# start_date, end_date = st.sidebar.slider(
#     'Select time range',
#     min_value=df['Time'].min().date(),
#     max_value=df['Time'].max().date(),
#     value=(df['Time'].min().date(), df['Time'].max().date())
# )

# selected_sites = st.sidebar.multiselect(
#     'Select sites',
#     options=df['Site'].unique(),
#     default=df['Site'].unique()
# )

# selected_measurements = st.sidebar.multiselect(
#     'Select measurements',
#     options=df['Measurement'].unique(),
#     default=df['Measurement'].unique()
# )

# # Filter data based on user input
# filtered_df = df[
#     (df['Time'].dt.date >= start_date) &
#     (df['Time'].dt.date <= end_date) &
#     (df['Site'].isin(selected_sites)) &
#     (df['Measurement'].isin(selected_measurements))
# ]

# # Create the chart
# base = alt.Chart(filtered_df).encode(
#     x='Time:T',
#     color=alt.Color('Site_Measurement:N', scale=color_scale, legend=alt.Legend(title="Site and Measurement", orient='bottom')),
#     tooltip=['Time:T', 'Value:Q', 'Measurement:N', 'Site:N']
# )

# # Create the temperature line
# temp_line = base.transform_filter(
#     alt.datum.Measurement == 'Temperature (°C)'
# ).mark_line().encode(
#     y=alt.Y('Value:Q', axis=alt.Axis(title='Temperature (°C)'))
# )

# # Create the dissolved oxygen line
# do_line = base.transform_filter(
#     alt.datum.Measurement == 'DO (mg/L)'
# ).mark_line().encode(
#     y=alt.Y('Value:Q', axis=alt.Axis(title='DO (mg/L)', orient='right'))
# )

# # Layer the lines
# chart = alt.layer(temp_line, do_line).resolve_scale(
#     y='independent'
# ).properties(
#     width=1000,  # Adjust width to maximize size
#     height=600,  # Adjust height to maximize size
#     title='Temperature and Dissolved Oxygen Over Time at CMAST and DUML'
# )

# # Display the chart in Streamlit
# st.altair_chart(chart, use_container_width=True)

# # -----------------------------------------------------------------------------
# # Draw the actual page

# # # Set the title that appears at the top of the page.
# # '''
# # # :fire: Temperature dashboard

# # Browse water temperature data collected at the CMAST oyster farm between May and October 2024.
# # '''

# # ''

# # # Make a slider based on times
# # min_time = temp_df['Time'].min().to_pydatetime()
# # max_time = temp_df['Time'].max().to_pydatetime()

# # from_time, to_time = st.slider(
# #     'Which hours are you interested in?',
# #     min_value = min_time,
# #     max_value = max_time,
# #     value=[min_time, max_time],
# #     key = 2)

# # ''

# # sensors = temp_df['Location'].unique()

# # if not len(sensors):
# #     st.warning("Select at least one sensor")

# # selected_sensors = st.multiselect(
# #     'Which sensors would you like to view?',
# #     sensors,
# #     ['Array', 'Line 1A', 'Line 1B'],
# #     key = 3
# #     )

# # ''

# # # Filter the data
# # filtered_temp_df = temp_df[
# #     (temp_df['Location'].isin(selected_sensors))
# #     & (temp_df['Time'] <= to_time)
# #     & (from_time <= temp_df['Time'])
# # ]

# # st.header('Water temperature over time', divider='gray')

# # ''

# # st.line_chart(
# #     filtered_temp_df,
# #     x='Time',
# #     y='TempC',
# #     color='Location',
# # )
