import streamlit as st
import pandas as pd

# Example dataframes (replace with actual data)
# station_requirements = pd.DataFrame([...])
# department_requirements = pd.DataFrame([...])
# schedule = pd.DataFrame([...])

# Streamlit layout
st.title("Production Schedule Analysis")

# Month selection
months = schedule.columns[2:]  # Assuming first two columns are 'Program' and 'mbom'
selected_month = st.selectbox("Select a Month", months)

# Calculate requirements
def calculate_requirements(selected_month):
    # Filter the schedule for the selected month
    month_schedule = schedule[['Program', selected_month]]

    # Merge with station and department requirements
    station_req = pd.merge(month_schedule, station_requirements, on='Program')
    department_req = pd.merge(month_schedule, department_requirements, on='Program')

    # Calculate total hours
    station_req['Total Station Hours'] = station_req[selected_month] * station_req['Hours']
    department_req['Total Department Hours'] = department_req[selected_month] * department_req['Hours']

    return station_req, department_req

station_req, department_req = calculate_requirements(selected_month)

# Display results
st.header(f"Station Requirements for {selected_month}")
st.dataframe(station_req[['Program', 'Station', 'Total Station Hours']])

st.header(f"Department Requirements for {selected_month}")
st.dataframe(department_req[['Program', 'DepartmentID', 'Total Department Hours']])

# Visualization (if required)
# Bar charts or other visualizations can be added here based on the aggregated data
