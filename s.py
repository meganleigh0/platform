import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import simpy  # Ensure simpy is installed

# Import or define your Simulation, Schedule, and other classes here

simulation = Simulation()  # Create a simulation instance

def generate_calendar_style_schedule_table(schedule):
    # Your existing function code here

# Streamlit layout
st.title("Production Schedule Simulator")

# Sidebar
with st.sidebar:
    selected_month = st.selectbox("Select Month", options=simulation.schedule.months)
    duration = st.radio("Select Duration", options=['Day', 'Week', 'Month'], index=0)
    rate = st.number_input("Enter Rate", min_value=1, value=5)
    if st.button("Run Simulation"):
        # Run simulation logic
    if st.button("Clear Simulation"):
        # Clear simulation logic

# Main area
schedule_data = generate_calendar_style_schedule_table(simulation.schedule)
st.dataframe(schedule_data.style.applymap(lambda x: 'background-color: lightblue'))

# Gantt Chart
if 'gantt_chart' in st.session_state:
    st.plotly_chart(st.session_state.gantt_chart)

# Additional enhancements can be added as per the above suggestions
