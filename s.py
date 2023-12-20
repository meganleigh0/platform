import streamlit as st
import pandas as pd
import datetime
import simpy  # Ensure simpy is installed
from your_module import Scheduler, Schedule  # Replace with actual import

# Initialize the Scheduler and Schedule
env = simpy.Environment()  # Replace with actual environment setup
schedule = Schedule(env)  # Replace with actual schedule loading method
scheduler = Scheduler(env, schedule, datetime.date(2024, 1, 1))

# Function to aggregate data for a selected month
def aggregate_data_for_month(month):
    scheduler.set_month_requirements(month)
    department_data = {}
    station_data = {}

    for program_obj in schedule.programs.values():
        quantity = program_obj.get_quantity_for_month(month)
        for dept_id, hours in program_obj.product_department_req.items():
            department_data[dept_id] = department_data.get(dept_id, 0) + hours * quantity
        for station_name, hours in program_obj.product_station_req.items():
            station_data[station_name] = station_data.get(station_name, 0) + hours * quantity

    return department_data, station_data

# Streamlit layout
st.title("Production Schedule Overview")

# Display months in the schedule
months = schedule.months  # Assuming this is a list of months
selected_month = st.selectbox("Select a month", months)

# Aggregated data display and visualization
if selected_month:
    department_hours, station_hours = aggregate_data_for_month(selected_month)
    
    # Display department data
    st.header(f"Department Hours for {selected_month}")
    st.dataframe(pd.DataFrame.from_dict(department_hours, orient='index', columns=['Hours']))

    # Display station data
    st.header(f"Station Hours for {selected_month}")
    st.dataframe(pd.DataFrame.from_dict(station_hours, orient='index', columns=['Hours']))

    # Visualizations
    st.bar_chart(pd.DataFrame.from_dict(department_hours, orient='index', columns=['Hours']))
    st.bar_chart(pd.DataFrame.from_dict(station_hours, orient='index', columns=['Hours']))

    # Filtering options
    st.sidebar.header("Filter Options")
    # Example: Filter by Department
    department_filter = st.sidebar.multiselect("Select Departments", list(department_hours.keys()))
    if department_filter:
        filtered_dept_hours = {dept: hours for dept, hours in department_hours.items() if dept in department_filter}
        st.dataframe(pd.DataFrame.from_dict(filtered_dept_hours, orient='index', columns=['Hours']))
