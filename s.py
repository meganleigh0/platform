import streamlit as st
import pandas as pd

# Assuming these are your dataframes (replace with actual data loading)
# station_requirements = pd.DataFrame([...])
# department_requirements = pd.DataFrame([...])
# schedule = pd.DataFrame([...])

# Function to calculate the total hours
def calculate_total_hours(schedule, requirements, month=None, program=None):
    filtered_schedule = schedule.copy()
    if month:
        filtered_schedule = filtered_schedule[['Program', month]]
    if program:
        filtered_schedule = filtered_schedule[filtered_schedule['Program'] == program]

    # Merging schedule with requirements and calculating total hours
    merged_data = pd.merge(filtered_schedule, requirements, on='Program')
    for month in schedule.columns[2:]:
        if month in merged_data:
            merged_data[month] *= merged_data['Hours']

    return merged_data.groupby('Program')[schedule.columns[2:]].sum()

# Streamlit layout
st.set_page_config(layout="wide")
st.title("Production Schedule Analysis")

# Month and Program selection
months = ['All'] + list(schedule.columns[2:])
programs = ['All'] + list(schedule['Program'].unique())
selected_month = st.sidebar.selectbox("Select a Month", months)
selected_program = st.sidebar.selectbox("Select a Program", programs)

# Filter by selected options
month_filter = None if selected_month == 'All' else selected_month
program_filter = None if selected_program == 'All' else selected_program

# Calculate total hours for station and department
total_station_hours = calculate_total_hours(schedule, station_requirements, month_filter, program_filter)
total_department_hours = calculate_total_hours(schedule, department_requirements, month_filter, program_filter)

# Display results
col1, col2 = st.columns(2)
with col1:
    st.header("Station Requirements")
    st.dataframe(total_station_hours)
    st.bar_chart(total_station_hours.sum())

with col2:
    st.header("Department Requirements")
    st.dataframe(total_department_hours)
    st.bar_chart(total_department_hours.sum())
