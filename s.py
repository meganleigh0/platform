import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import simpy  # Ensure simpy is installed

# Import or define your Simulation, Schedule, and other classes here

simulation = Simulation()  # Create a simulation instance

def generate_calendar_style_schedule_table(schedule):
    data = []
    for program_key, program_obj in schedule.programs.items():
        program_name = program_key[0]
        for month, quantity in program_obj.production_plan.items():
            data.append({'Program': program_name, 'Month': month, 'Quantity': quantity})

    df = pd.DataFrame(data)
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    pivot_df = df.pivot(index='Program', columns='Month', values='Quantity').fillna(0).reset_index()
    pivot_df = pivot_df[['Program'] + month_order]  # Ensure months are in correct order
    return pivot_df

# Streamlit layout
st.title("Production Schedule Simulator")

# Display the schedule table
schedule_data = generate_calendar_style_schedule_table(simulation.schedule)
st.dataframe(schedule_data)

# Month selector
selected_month = st.selectbox("Select Month", options=simulation.schedule.months)

# Duration selector
duration = st.radio("Select Duration", options=['Day', 'Week', 'Month'], index=0)
duration_values = {'Day': 1, 'Week': 7, 'Month': 30}

# Rate input
rate = st.number_input("Enter Rate", min_value=1, value=5)

# Run simulation button
if st.button("Run Simulation"):
    simulation.run_simulation(rate, duration_values[duration], selected_month)
    gantt_chart = viz.gantt()  # Replace with actual function to generate Gantt chart
    st.plotly_chart(gantt_chart)

# Clear simulation button
if st.button("Clear Simulation"):
    simulation.clear_simulation()
    st.plotly_chart(go.Figure())
