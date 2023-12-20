import streamlit as st
import pandas as pd
import datetime
import simpy  # Make sure simpy is installed
from your_module import Scheduler, Schedule  # Replace with actual import

# Initialize the Scheduler and Schedule
env = simpy.Environment()  # Replace with actual environment setup
schedule = Schedule(env)  # Replace with actual schedule loading method
scheduler = Scheduler(env, schedule, datetime.date(2024, 1, 1))

# Function to aggregate data for a selected month
def aggregate_data_for_month(month):
    scheduler.set_month_requirements(month)
    data = []
    for program_obj in schedule.programs.values():
        data.append({
            'Program': program_obj.name,
            'Department Hours': program_obj.product_department_req,
            'Station Hours': program_obj.product_station_req
        })
    return pd.DataFrame(data)

# Streamlit layout
st.title("Production Schedule Overview")

# Display months in the schedule
months = schedule.months  # Assuming this is a list of months
selected_month = st.selectbox("Select a month", months)

# Show aggregated data when a month is selected
if selected_month:
    aggregated_data = aggregate_data_for_month(selected_month)
    st.header(f"Requirements for {selected_month}")
    st.dataframe(aggregated_data)

# Additional Visualization (if required)
# st.bar_chart(aggregated_data[['Department Hours', 'Station Hours']])
