import streamlit as st
import pandas as pd

# Read the data from CSV files
station_data = pd.read_csv('station_requirements.csv')
department_data = pd.read_csv('department_requirements.csv')

# Calculate total hours for all programs
total_station_hours = station_data['Station Hours'].sum()
total_department_hours = department_data['Department Hours'].sum()

# Streamlit layout
st.title("Production Schedule Analysis")

st.header("Total Hours Required for All Programs")
st.write(f"Total Station Hours: {total_station_hours}")
st.write(f"Total Department Hours: {total_department_hours}")

# Dropdown for selecting a program
st.header("Individual Program Analysis")
selected_program = st.selectbox("Select a Program", station_data['Program'].unique())

# Filter data based on the selected program
program_station_data = station_data[station_data['Program'] == selected_program]
program_department_data = department_data[department_data['Program'] == selected_program]

# Display program-specific data
st.subheader(f"Station Requirements for {selected_program}")
st.dataframe(program_station_data)

st.subheader(f"Department Requirements for {selected_program}")
st.dataframe(program_department_data)

# Visualization (if required)
# For example, bar charts for station hours
st.bar_chart(program_station_data.groupby('Station Name')['Station Hours'].sum())

# Similarly, you can visualize department hours
st.bar_chart(program_department_data.groupby('Department ID')['Department Hours'].sum())
