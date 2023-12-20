import streamlit as st
import pandas as pd
import datetime
import simpy  # Ensure simpy is installed
from your_module import Scheduler, Schedule  # Replace with actual import

# Initialize the Scheduler and Schedule
env = simpy.Environment()  # Replace with actual environment setup
schedule = Schedule(env)  # Replace with actual schedule loading method
scheduler = Scheduler(env, schedule, datetime.date(2024, 1, 1))

# Function to aggregate data for a selected month and filter by program
def aggregate_data_for_month(month, program_filter=None, vehicle_filter=None):
    scheduler.set_month_requirements(month)
    data = []

    for program_key, program_obj in schedule.programs.items():
        if program_filter and program_obj.name not in program_filter:
            continue

        quantity = program_obj.get_quantity_for_month(month)
        if quantity > 0:
            for dept_id, hours in program_obj.product_department_req.items():
                for station_name, hours_station in program_obj.product_station_req.items():
                    data.append({
                        'Program': program_obj.name,
                        'Department': dept_id,
                        'Station': station_name,
                        'Department Hours': hours * quantity,
                        'Station Hours': hours_station * quantity
                    })

    df = pd.DataFrame(data)
    if vehicle_filter:
        df = df[df['Vehicle'].isin(vehicle_filter)]
    return df

# Streamlit layout
st.title("Production Schedule Overview")

# Display months in the schedule
months = schedule.months  # Assuming this is a list of months
selected_month = st.selectbox("Select a month", months)

# Filters
st.sidebar.header("Filter Options")
program_filter = st.sidebar.multiselect("Select Programs", [p.name for p in schedule.programs.values()])
vehicle_filter = st.sidebar.multiselect("Select Vehicles", [v.name for v in schedule.vehicles.values()])  # Assuming you have a list of vehicles

# Display and visualize data
if selected_month:
    aggregated_data = aggregate_data_for_month(selected_month, program_filter, vehicle_filter)
    
    # Visualizations - Department Hours
    st.header(f"Department Hours for {selected_month}")
    department_chart_data = aggregated_data.groupby('Department')['Department Hours'].sum()
    st.bar_chart(department_chart_data)

    # Visualizations - Station Hours
    st.header(f"Station Hours for {selected_month}")
    station_chart_data = aggregated_data.groupby('Station')['Station Hours'].sum()
    st.bar_chart(station_chart_data)
