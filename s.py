import streamlit as st
import pandas as pd
from your_module import Simulation, Scheduler, Program

# Initialize the Simulation
simulation = Simulation()

# Function to aggregate required hours by department and station
def aggregate_data(simulation):
    data = {
        'program': [],
        'month': [],
        'hours_by_department': [],
        'hours_by_station': []
    }

    for (program_key, program) in simulation.schedule.programs.items():
        for month in simulation.schedule.months:
            quantity = program.get_quantity_for_month(month)
            if quantity > 0:
                data['program'].append(program.name)
                data['month'].append(month)
                data['hours_by_department'].append(program.product_department_req * quantity)
                data['hours_by_station'].append(program.product_station_req * quantity)

    return pd.DataFrame(data)

# Aggregate the data
aggregated_data = aggregate_data(simulation)

# Streamlit layout
st.title("Production Schedule Overview")

# Display the aggregated data in a table
st.header("Program Requirements by Month")
st.dataframe(aggregated_data)

# Additional Visualization (if required)
# st.bar_chart(aggregated_data['hours_by_department'])
